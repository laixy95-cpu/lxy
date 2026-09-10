"""
Counterfactual specification module (Table 3 of the manuscript).

This is the component named in the manuscript's Data Availability statement and
absent from `asean6_reproducible.py`, which fits a single linear trend to
already-standardised dimension scores. Section 3.4 states that fitting on
standardised scores "is equivalent for affine forms alone and is inadmissible for
the log and logit forms", so the specifications below are fitted on RAW indicator
values and standardised afterwards, per Eq. (1) and Eq. (3).

Forms, per Table 3:

    TDLoss           linear      2010-2019   trending, far from bounds
    AccessElec       logit       2010-2019   share bounded at 100%
    Inflation        mean        2015-2019   stationary, mean-reverting
    RenTFEC          linear      2010-2019   trending, far from bounds
    CO2IntElec       linear      2010-2019   secular decline
    EnergyIntensity  linear      2010-2019   secular decline
    RenCap           log-linear  2010-2019   multiplicative growth
    RenElec          linear      2010-2019   trending, far from bounds

Each spec carries a `window_len` so that a rolling-origin backtest can refit it at
any origin using the same trailing-window rule that produces the main
specification at origin 2019 (10 years for most indicators, 5 for Inflation).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Access shares are published as exactly 100.0 once electrification completes, and
# logit(1.0) is undefined. Values are clamped into (EPS_SHARE, 1 - EPS_SHARE)
# before the logit transform. The clamp is reported in the fit diagnostics because
# it materially affects the fitted slope for countries already at the ceiling.
EPS_SHARE = 1e-4
MIN_TRAIN = 5


class InfeasibleCounterfactual(RuntimeError):
    """Raised when a fitted path leaves the indicator's admissible region."""


# --------------------------------------------------------------------- forms
def _fit_linear(years, values):
    slope, intercept = np.polyfit(years, values, 1)
    return lambda t: intercept + slope * np.asarray(t, dtype=float)


def _fit_mean(years, values):
    m = float(np.mean(values))
    return lambda t: np.full(np.shape(t), m, dtype=float)


def _fit_loglinear(years, values):
    if np.any(np.asarray(values) <= 0):
        raise InfeasibleCounterfactual("log-linear form requires strictly positive values")
    slope, intercept = np.polyfit(years, np.log(values), 1)
    return lambda t: np.exp(intercept + slope * np.asarray(t, dtype=float))


def _fit_logit(years, values, ceiling=100.0):
    p = np.clip(np.asarray(values, dtype=float) / ceiling, EPS_SHARE, 1 - EPS_SHARE)
    slope, intercept = np.polyfit(years, np.log(p / (1 - p)), 1)

    def predict(t):
        lin = intercept + slope * np.asarray(t, dtype=float)
        return ceiling / (1.0 + np.exp(-lin))

    return predict


FORMS = {"linear": _fit_linear, "mean": _fit_mean,
         "loglinear": _fit_loglinear, "logit": _fit_logit}


# --------------------------------------------------------------------- specs
@dataclass(frozen=True)
class Spec:
    indicator: str
    form: str
    direction: int          # +1 if higher raw value supports the outcome
    window_len: int         # trailing training-window length in years
    dimension: str
    rationale: str
    ceiling: float | None = None
    feasible: tuple[float | None, float | None] = (None, None)  # (low, high)
    # An exact 0.0 is outside the observed range of every indicator here except
    # Inflation, so a zero denotes a missing observation rather than a measured
    # one. The workbook codes unavailable crisis-year cells as 0 rather than
    # blank, which `isna()`-based audits do not catch.
    zero_is_missing: bool = True

    def fit(self, years, values, min_train: int = MIN_TRAIN):
        years = np.asarray(years, dtype=float)
        values = np.asarray(values, dtype=float)
        if len(years) < min_train:
            raise InfeasibleCounterfactual(
                f"{self.indicator}: {len(years)} training points, need >= {min_train}")
        if self.form == "logit":
            clamped = int(np.sum((values / self.ceiling >= 1 - EPS_SHARE)
                                 | (values / self.ceiling <= EPS_SHARE)))
            fn = _fit_logit(years, values, self.ceiling)
            fn.clamped = clamped                      # noqa: B010  (diagnostic)
        else:
            fn = FORMS[self.form](years, values)
            fn.clamped = 0                            # noqa: B010
        return fn

    def check(self, predicted):
        """Feasibility gate from the Table 3 notes."""
        lo, hi = self.feasible
        pred = np.asarray(predicted, dtype=float)
        if lo is not None and np.any(pred < lo):
            raise InfeasibleCounterfactual(
                f"{self.indicator}: expected value {pred.min():.4g} below admissible floor {lo}")
        if hi is not None and np.any(pred > hi):
            raise InfeasibleCounterfactual(
                f"{self.indicator}: expected value {pred.max():.4g} above admissible ceiling {hi}")
        return pred


# Feasibility bounds encode the Table 3 note: reject any specification producing
# expected access above 100 per cent, negative renewable capacity, or implied
# deflation below -1 per cent.
SPECS: dict[str, Spec] = {
    s.indicator: s for s in [
        # Audit A18: Table 3 assigns a linear trend on the grounds that the series
        # is "far from bounds", but Singapore falls from 4.91% to 1.03% over
        # 2010-2019 and a linear path reaches -0.49% by 2023. Losses are bounded
        # below at zero, so the log-linear form applies for the same reason it
        # applies to RenCap: proportional, not additive, change.
        Spec("TDLoss", "loglinear", -1, 10, "EnergyServiceSecurity",
             "Bounded below at zero; Singapore approaches the bound and a linear path goes negative",
             feasible=(0.0, None)),
        Spec("AccessElec", "logit", +1, 10, "EnergyServiceSecurity",
             "Linear extrapolation yields expected access above the physical ceiling",
             ceiling=100.0, feasible=(0.0, 100.0)),
        Spec("Inflation", "mean", -1, 5, "MacroPricePressure",
             "Linear extrapolation implies deflation; window selected on backtest bias and RMSE",
             feasible=(-1.0, None), zero_is_missing=False),
        Spec("RenTFEC", "linear", +1, 10, "LowCarbonContinuity",
             "Standard specification for a trending, unconstrained series",
             feasible=(0.0, 100.0)),
        Spec("CO2IntElec", "linear", -1, 10, "LowCarbonContinuity",
             "Standard specification for a trending, unconstrained series",
             feasible=(0.0, None)),
        Spec("EnergyIntensity", "linear", -1, 10, "LowCarbonContinuity",
             "Standard specification for a trending, unconstrained series",
             feasible=(0.0, None)),
        Spec("RenCap", "loglinear", +1, 10, "LowCarbonContinuity",
             "Deployment compounds once established, so growth is proportional and not additive",
             feasible=(0.0, None)),
        Spec("RenElec", "linear", +1, 10, "LowCarbonContinuity",
             "Standard specification for a trending, unconstrained series",
             feasible=(0.0, 100.0)),
    ]
}

DIMENSIONS: dict[str, list[str]] = {}
for _s in SPECS.values():
    DIMENSIONS.setdefault(_s.dimension, []).append(_s.indicator)


# ------------------------------------------------------------ variant builders
def uniform_linear_specs() -> dict[str, Spec]:
    """Robustness check promised in section 3.6 but never reported in Table 8.

    Replaces every Table 3 assignment with a linear trend on the raw values and
    drops the feasibility gate, so the inadmissible paths the manuscript cites
    (access above 100 per cent, implied deflation) are actually produced and can
    be quantified rather than asserted.
    """
    return {k: Spec(s.indicator, "linear", s.direction, 10, s.dimension,
                    "Uniform linear form (robustness variant)",
                    ceiling=s.ceiling, feasible=(None, None))
            for k, s in SPECS.items()}


def fixed_window_specs(window_len: int = 5) -> dict[str, Spec]:
    """Every indicator refitted on the same trailing window length."""
    return {k: Spec(s.indicator, s.form, s.direction, window_len, s.dimension,
                    f"{window_len}-year training window (robustness variant)",
                    ceiling=s.ceiling, feasible=s.feasible)
            for k, s in SPECS.items()}


def training_years(origin: int, window_len: int, first_year: int = 2010) -> list[int]:
    """Trailing window ending at `origin`, clipped at the start of the panel.

    At origin 2019 this returns 2010-2019 for the ten-year specs and 2015-2019 for
    Inflation, reproducing the main specification exactly; the same rule then
    defines every rolling-origin refit.
    """
    return list(range(max(first_year, origin - window_len + 1), origin + 1))


# ------------------------------------------------- low-carbon indicator basis
# UN SDG 7.2.1 (RenTFEC) and 7.3.1 (EnergyIntensity) are published only through
# 2022 - confirmed against Tracking SDG7: The Energy Progress Report 2025 - so
# neither can cover 2023. The compound stage spans 2022-2023, so a five-indicator
# low-carbon dimension would average different indicator sets in the two years of
# the same stage, and the stage-to-stage reordering in Eq. (5) would compare a
# five-indicator COVID mean against a mixed compound mean.
#
# The main specification therefore uses the three indicators available in every
# year of the panel. The five-indicator version is retained as a robustness check
# over the years where all five exist.
LOWCARBON_CORE = ["CO2IntElec", "RenCap", "RenElec"]
LOWCARBON_SDG = ["RenTFEC", "EnergyIntensity"]        # coverage ends in 2022


def active_specs(lowcarbon_basis: str = "core") -> dict[str, Spec]:
    """`core` = the three low-carbon indicators with full 2010-2023 coverage;
    `full` = all five, valid only where SDG coverage reaches."""
    if lowcarbon_basis == "full":
        return dict(SPECS)
    if lowcarbon_basis != "core":
        raise ValueError(lowcarbon_basis)
    return {k: v for k, v in SPECS.items()
            if v.dimension != "LowCarbonContinuity" or k in LOWCARBON_CORE}


def dimensions_of(specs: dict[str, Spec]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for s in specs.values():
        out.setdefault(s.dimension, []).append(s.indicator)
    return out
