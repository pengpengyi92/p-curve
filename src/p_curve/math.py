"""Deterministic research mathematics on caller-supplied synthetic inputs.

Copyright (c) 2026 Pengyi Peng. Released under the MIT license.
Adapted from selected proprietary PFICC / P-Curve research code.

Rates are annual decimal rates (0.04 is 4%), with continuous compounding.
Times are caller-supplied year fractions, not calendar dates. No calendar,
day-count, bootstrap, calibration, market-data or settlement convention is
inferred. Fixed cash flows are supplied by the caller, not generated from an
instrument. Interpolation is linear in zero rates, with no extrapolation.
"""

from __future__ import annotations

from math import exp, expm1, fsum, isfinite, isinf, log
from typing import Sequence

Curve = Sequence[tuple[float, float]]
Cashflows = Sequence[tuple[float, float]]
BP = 0.0001


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number, not a boolean")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _curve(points: Curve) -> tuple[tuple[float, float], ...]:
    result = tuple((_finite(t, "node maturity"), _finite(y, "zero rate"))
                   for t, y in points)
    if not result or any(t <= 0 for t, _ in result):
        raise ValueError("curve nodes must have positive finite maturities")
    if any(b[0] <= a[0] for a, b in zip(result, result[1:])):
        raise ValueError("curve maturities must be strictly increasing")
    return result


def _cashflows(cashflows: Cashflows) -> tuple[tuple[float, float], ...]:
    result = tuple((_finite(t, "cashflow time"), _finite(a, "cashflow amount"))
                   for t, a in cashflows)
    if any(t <= 0 for t, _ in result):
        raise ValueError("cashflows must occur strictly after valuation time")
    return result


def _loading(x: float) -> float:
    # t/tau can overflow to +inf even for finite positive inputs: its limit is 0.
    if isinf(x):
        return 0.0
    if x < 1e-6:
        return 1 - x / 2 + x * x / 6 - x**3 / 24
    return -expm1(-x) / x


def nelson_siegel(t: float, beta0: float, beta1: float,
                  beta2: float, tau: float) -> float:
    """Given-parameter NS continuous zero rate; this function does not fit data.

    t >= 0 and tau > 0 are year fractions; beta parameters are decimal rates.
    At t=0 the analytic limit is beta0+beta1. No parameters are estimated.
    """
    t, tau = _finite(t, "t"), _finite(tau, "tau")
    betas = [_finite(b, name) for b, name in
             [(beta0, "beta0"), (beta1, "beta1"), (beta2, "beta2")]]
    if t < 0 or tau <= 0:
        raise ValueError("t must be nonnegative and tau positive")
    x = t / tau
    loading = _loading(x)
    return _finite(betas[0] + betas[1] * loading
                   + betas[2] * (loading - exp(-x)), "NS zero rate")


def nelson_siegel_svensson(t: float, beta0: float, beta1: float,
                            beta2: float, beta3: float,
                            tau1: float, tau2: float) -> float:
    """Given-parameter NSS continuous zero rate, not a calibrated NSS model."""
    t, tau2, beta3 = _finite(t, "t"), _finite(tau2, "tau2"), _finite(beta3, "beta3")
    if t < 0 or tau2 <= 0:
        raise ValueError("t must be nonnegative and tau2 positive")
    base = nelson_siegel(t, beta0, beta1, beta2, tau1)
    x = t / tau2
    return _finite(base + beta3 * (_loading(x) - exp(-x)), "NSS zero rate")


def _linear_zero(curve: Curve, t: float) -> float:
    if t < curve[0][0] or t > curve[-1][0]:
        raise ValueError("maturity outside curve nodes; extrapolation is not supported")
    for node_t, node_y in curve:
        if t == node_t:
            return node_y
    for (t0, y0), (t1, y1) in zip(curve, curve[1:]):
        if t0 < t < t1:
            w = (t - t0) / (t1 - t0)
            return _finite(y0 * (1 - w) + y1 * w, "interpolated zero rate")
    raise AssertionError("unreachable interpolation state")


def linear_zero(points: Curve, maturity: float) -> float:
    """Piecewise-linear continuous zero rate, including nodes, never extrapolated."""
    return _linear_zero(_curve(points), _finite(maturity, "maturity"))


def discount_factor(t: float, zero_rate: float) -> float:
    """exp(-zero_rate*t), with negative rates allowed and DF(0)=1.

    Return a strictly positive finite float. Inputs that overflow, or underflow
    to zero, are rejected rather than silently producing invalid discount factors.
    """
    t, rate = _finite(t, "t"), _finite(zero_rate, "zero_rate")
    if t < 0:
        raise ValueError("t must be nonnegative")
    try:
        result = exp(-rate * t)
    except OverflowError as exc:
        raise ValueError("discount factor outside positive finite float range") from exc
    if not isfinite(result) or result <= 0:
        raise ValueError("discount factor outside positive finite float range")
    return result


def period_forward_from_discounts(df1: float, df2: float, dt: float) -> float:
    """Period-average continuously compounded forward, not instantaneous forward.

    Inputs must refer to consistent valuation/discount conventions. The function
    cannot establish that consistency. Log differences avoid forming df2/df1.
    """
    df1, df2, dt = (_finite(df1, "df1"), _finite(df2, "df2"), _finite(dt, "dt"))
    if df1 <= 0 or df2 <= 0 or dt <= 0:
        raise ValueError("discount factors and interval must be positive")
    return _finite((log(df1) - log(df2)) / dt, "period forward")


def _pv(cashflows: Cashflows, nodes: Curve) -> float:
    values = [_finite(amount * discount_factor(t, _linear_zero(nodes, t)), "discounted cashflow")
              for t, amount in cashflows]
    try:
        total = fsum(values)
    except OverflowError as exc:
        raise ValueError("present value outside finite float range") from exc
    return _finite(total, "present value")


def price_cashflows(cashflows: Cashflows, zero_curve: Curve) -> float:
    """PV of supplied fixed cash flows under continuous zeros; no accrued interest.

    Cash-flow times must be positive and within the supplied node interval.
    Signed amounts are allowed; an empty set has PV 0 on a valid curve.
    """
    return _pv(_cashflows(cashflows), _curve(zero_curve))


def _bump(nodes: Curve, bump_bp: float) -> tuple[float, float]:
    bump_bp = _finite(bump_bp, "bump_bp")
    delta = bump_bp * BP
    if bump_bp <= 0 or not isfinite(2 * bump_bp) or not isfinite(delta) or delta <= 0:
        raise ValueError("bump_bp must give a positive finite decimal bump and central-difference denominator")
    if any(not isfinite(y - delta) or not isfinite(y + delta)
           or y - delta == y or y + delta == y for _, y in nodes):
        raise ValueError("bump must change every node within finite float range")
    return bump_bp, delta


def parallel_dv01(cashflows: Cashflows, zero_curve: Curve,
                   bump_bp: float = 1.0) -> float:
    """(PV(-bump)-PV(+bump))/(2*bump_bp), currency per 1bp.

    Every continuous zero node is shifted. Long positive fixed cash flows have
    positive DV01; signed portfolios need not. This is a central finite difference,
    not a production instrument-risk system or a duration percentage.
    """
    nodes, cashflows = _curve(zero_curve), _cashflows(cashflows)
    bump_bp, delta = _bump(nodes, bump_bp)
    down, up = ([(t, y - delta) for t, y in nodes], [(t, y + delta) for t, y in nodes])
    return _finite((_pv(cashflows, down) - _pv(cashflows, up)) / (2 * bump_bp), "parallel DV01")


def key_rate_dv01(cashflows: Cashflows, zero_curve: Curve,
                  bump_bp: float = 1.0) -> dict[float, float]:
    """Node-wise central zero-rate bumps, in currency per 1bp.

    The same linear-zero interpolation is used on each bumped curve. In the
    infinitesimal limit the bucket sum equals parallel risk. For off-node cash
    flows and finite bumps this is only an approximation, not an exact identity.
    """
    nodes, cashflows = _curve(zero_curve), _cashflows(cashflows)
    bump_bp, delta = _bump(nodes, bump_bp)
    result = {}
    for i, (tenor, rate) in enumerate(nodes):
        down, up = list(nodes), list(nodes)
        down[i], up[i] = (tenor, rate - delta), (tenor, rate + delta)
        result[tenor] = _finite((_pv(cashflows, down) - _pv(cashflows, up)) / (2 * bump_bp), "key rate DV01")
    return result
