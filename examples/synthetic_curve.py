"""Offline, explicitly fictional example: no market snapshot or investment signal."""

import json
import math

from p_curve import (
    key_rate_dv01,
    nelson_siegel,
    parallel_dv01,
    price_cashflows,
)


def demo() -> dict:
    """Return a deterministic synthetic report, also checked against a hand oracle."""
    curve = [(0.5, 0.03), (1.0, 0.03), (2.0, 0.04)]
    cashflows = [(1.0, 5.0), (2.0, 105.0)]
    pv = price_cashflows(cashflows, curve)
    expected_pv = 5.0 * math.exp(-0.03) + 105.0 * math.exp(-0.08)
    if not math.isclose(pv, expected_pv, rel_tol=1e-12, abs_tol=1e-12):
        raise AssertionError("synthetic PV differs from independent exponential oracle")
    return {
        "input_kind": "SYNTHETIC_FICTIONAL_NOT_MARKET_DATA",
        "rates": "annual_decimals_continuous_zero",
        "time": "caller_supplied_year_fractions_no_calendar",
        "cashflow_currency": "arbitrary_consistent_currency_units",
        "zero_curve": curve,
        "cashflows": cashflows,
        "present_value": pv,
        "parallel_dv01_currency_per_bp": parallel_dv01(cashflows, curve),
        "key_rate_dv01_currency_per_bp": key_rate_dv01(cashflows, curve),
        "given_parameter_ns_not_calibrated": [
            [t, nelson_siegel(t, 0.04, -0.015, 0.01, 2.0)]
            for t in [0.0, 0.25, 1.0, 2.0, 5.0, 10.0]
        ],
        "production_readiness": "NOT_ESTABLISHED",
        "economic_benefit": "UNMEASURED",
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, allow_nan=False))
