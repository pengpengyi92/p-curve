"""Selected experimental curve research utilities; not a production pricer.

Copyright (c) 2026 Pengyi Peng. Released under the MIT license.
Adapted from selected proprietary PFICC / P-Curve research code.
"""

from .math import (
    BP,
    Cashflows,
    Curve,
    discount_factor,
    key_rate_dv01,
    linear_zero,
    nelson_siegel,
    nelson_siegel_svensson,
    parallel_dv01,
    period_forward_from_discounts,
    price_cashflows,
)

__version__ = "0.2.0"
__all__ = [
    "BP", "Cashflows", "Curve", "discount_factor", "key_rate_dv01",
    "linear_zero", "nelson_siegel", "nelson_siegel_svensson",
    "parallel_dv01", "period_forward_from_discounts", "price_cashflows",
]
