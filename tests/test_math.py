"""Public, fictional fixtures and independent mathematical checks; no market data."""

import math
import unittest

from p_curve import (
    BP, discount_factor, key_rate_dv01, linear_zero, nelson_siegel,
    nelson_siegel_svensson, parallel_dv01, period_forward_from_discounts,
    price_cashflows,
)


class CurveMathTests(unittest.TestCase):
    def test_basis_point_unit(self):
        self.assertEqual(BP, 0.0001)

    def test_ns_zero_and_small_time_limits(self):
        for t in [0, 1e-16, 1e-12]:
            self.assertAlmostEqual(nelson_siegel(t, .04, -.01, .02, 1.5), .03, places=12)

    def test_ns_fixed_formula_at_one(self):
        # Direct equation at t/tau=1, independent of internal loading helper.
        e = 1 / math.e
        expected = .04 - .01 * (1 - e) + .02 * (1 - 2 * e)
        self.assertAlmostEqual(nelson_siegel(2, .04, -.01, .02, 2), expected, places=15)

    def test_nss_extra_curvature_and_nested_ns(self):
        ns = nelson_siegel(3, .04, -.01, .02, 1.5)
        self.assertEqual(nelson_siegel_svensson(3, .04, -.01, .02, 0, 1.5, 3), ns)
        expected = ns + .03 * (1 - 2 / math.e)
        self.assertAlmostEqual(nelson_siegel_svensson(3, .04, -.01, .02, .03, 1.5, 3), expected)

    def test_nss_short_limit_and_flat_parameterization(self):
        self.assertAlmostEqual(nelson_siegel_svensson(0, .04, -.01, .02, .03, 1.5, 3), .03)
        for t in [0, .2, 30]:
            self.assertEqual(nelson_siegel_svensson(t, -.01, 0, 0, 0, 1.5, 3), -.01)

    def test_ns_extremely_large_scaled_time_has_long_term_limit(self):
        self.assertEqual(nelson_siegel(1e308, .04, -.01, .02, 1e-308), .04)

    def test_invalid_ns_and_nss_inputs(self):
        for t, tau in [(-1, 2), (1, 0), (1, -2), (math.nan, 2), (1, math.inf)]:
            with self.subTest(t=t, tau=tau), self.assertRaises(ValueError):
                nelson_siegel(t, .04, -.01, .02, tau)
        for beta in [math.inf, math.nan, True, None]:
            with self.subTest(beta=beta), self.assertRaises(ValueError):
                nelson_siegel(1, beta, 0, 0, 2)
        with self.assertRaises(ValueError):
            nelson_siegel_svensson(1, .04, 0, 0, 0, 2, 0)

    def test_discount_zero_and_negative_rates(self):
        self.assertEqual(discount_factor(0, .2), 1)
        self.assertEqual(discount_factor(10, 0), 1)
        self.assertAlmostEqual(discount_factor(2, math.log(1.1) / 2), 1 / 1.1)
        self.assertAlmostEqual(discount_factor(1, -math.log(1.1)), 1.1)

    def test_discount_invalid_and_unrepresentable_values(self):
        for t, rate in [(-1, .02), (1, math.nan), (math.inf, .02), (1000, 1), (1000, -1)]:
            with self.subTest(t=t, rate=rate), self.assertRaises(ValueError):
                discount_factor(t, rate)

    def test_forward_from_rational_discount_factors(self):
        self.assertAlmostEqual(period_forward_from_discounts(.9, .81, 2), math.log(10 / 9) / 2)
        self.assertAlmostEqual(period_forward_from_discounts(1, 1.1, 1), -math.log(1.1))

    def test_forward_does_not_overflow_a_discount_factor_ratio(self):
        self.assertAlmostEqual(period_forward_from_discounts(1e300, 1e-300, 2), 300 * math.log(10))

    def test_forward_rejects_invalid_inputs(self):
        for args in [(0, 1, 1), (1, -1, 1), (1, 1, 0), (1, 1, -1), (math.inf, 1, 1), (1, 1, math.nan)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                period_forward_from_discounts(*args)

    def test_interpolation_nodes_and_midpoint(self):
        curve = [(1, -.01), (3, .03), (7, .05)]
        self.assertEqual(linear_zero(curve, 1), -.01)
        self.assertEqual(linear_zero(curve, 7), .05)
        self.assertAlmostEqual(linear_zero(curve, 2), .01)
        self.assertAlmostEqual(linear_zero(curve, 4), .035)

    def test_single_node_only_prices_at_that_node(self):
        self.assertEqual(linear_zero([(2, .03)], 2), .03)
        with self.assertRaises(ValueError):
            linear_zero([(2, .03)], 1.99)

    def test_no_silent_extrapolation_or_sorting(self):
        for curve, t in [([], 1), ([(0, .02)], 0), ([(2, .02), (1, .03)], 1),
                         ([(1, .02), (1, .03)], 1), ([(1, math.inf)], 1),
                         ([(math.nan, .02)], 1), ([(1, .02), (3, .04)], .9),
                         ([(1, .02), (3, .04)], 3.1), ([(1, .02)], math.nan)]:
            with self.subTest(curve=curve, t=t), self.assertRaises(ValueError):
                linear_zero(curve, t)

    def test_pv_independent_hand_discount_oracle(self):
        # Fictional cashflows; D(1)=1/1.05 and D(2)=1/1.1 by construction.
        cf = [(1, 50), (2, 1050)]
        curve = [(1, math.log(1.05)), (2, math.log(1.1) / 2)]
        self.assertAlmostEqual(price_cashflows(cf, curve), 50 / 1.05 + 1050 / 1.1, places=11)

    def test_pv_signed_flows_and_empty_portfolio(self):
        curve = [(1, 0), (3, 0)]
        self.assertEqual(price_cashflows([(1, -30), (2, 100)], curve), 70)
        self.assertEqual(price_cashflows([], curve), 0)

    def test_pv_off_node_rate_interpolation_is_not_df_interpolation(self):
        # At 2Y the zero rate is log(1.2)/2, so a 120 cashflow has PV=100.
        r = math.log(1.2) / 2
        self.assertAlmostEqual(price_cashflows([(2, 120)], [(1, 0), (3, 2 * r)]), 100)

    def test_pv_cashflow_validation_and_node_bounds(self):
        for cf in [[(0, 100)], [(-1, 100)], [(1, math.nan)], [(math.inf, 100)], [(4, 100)]]:
            with self.subTest(cf=cf), self.assertRaises(ValueError):
                price_cashflows(cf, [(1, .03), (3, .04)])
        with self.assertRaises(ValueError):
            price_cashflows([], [])

    def test_parallel_dv01_matches_independent_zero_coupon_formula(self):
        # Flat zero curve, 2Y zero coupon: central difference = 100*sinh(2*h)/bump_bp.
        self.assertAlmostEqual(parallel_dv01([(2, 100)], [(1, 0), (3, 0)]),
                               100 * math.sinh(2 * BP), places=11)

    def test_risk_sign_for_short_cashflow_and_bump_normalization(self):
        cf, curve = [(2, -100)], [(1, 0), (3, 0)]
        self.assertLess(parallel_dv01(cf, curve), 0)
        self.assertAlmostEqual(parallel_dv01(cf, curve, 5), -100 * math.sinh(2 * 5 * BP) / 5, places=11)

    def test_off_node_key_rate_weights_against_independent_formula(self):
        # 2Y cashflow halfway between 1Y/3Y zero nodes: each loading is 1/2.
        cf, curve = [(2, 100)], [(1, 0), (3, 0)]
        krd = key_rate_dv01(cf, curve)
        expected = 100 * math.sinh(BP)
        self.assertAlmostEqual(krd[1], expected, places=11)
        self.assertAlmostEqual(krd[3], expected, places=11)

    def test_unequal_off_node_key_rate_loadings(self):
        # At 1.5Y, interpolation weights on 1Y/3Y are 0.75/0.25, not 0.5/0.5.
        risk = key_rate_dv01([(1.5, 100)], [(1, 0), (3, 0)])
        self.assertAlmostEqual(risk[1], 100 * math.sinh(1.5 * .75 * BP), places=11)
        self.assertAlmostEqual(risk[3], 100 * math.sinh(1.5 * .25 * BP), places=11)

    def test_amount_scaling_and_short_portfolio_risk(self):
        curve, long_cf = [(1, .02), (3, .04)], [(1.5, 100), (3, 50)]
        short_cf = [(t, -2 * amount) for t, amount in long_cf]
        self.assertAlmostEqual(price_cashflows(short_cf, curve), -2 * price_cashflows(long_cf, curve))
        self.assertAlmostEqual(parallel_dv01(short_cf, curve), -2 * parallel_dv01(long_cf, curve))
        long_risk, short_risk = key_rate_dv01(long_cf, curve), key_rate_dv01(short_cf, curve)
        for t in long_risk:
            self.assertAlmostEqual(short_risk[t], -2 * long_risk[t])

    def test_off_node_key_rate_sum_only_approximates_finite_parallel_bump(self):
        cf, curve, bump = [(2, 100)], [(1, 0), (3, 0)], 100
        actual = sum(key_rate_dv01(cf, curve, bump).values())
        parallel = parallel_dv01(cf, curve, bump)
        self.assertLess(actual, parallel)
        self.assertAlmostEqual(actual, 200 * math.sinh(.01) / 100, places=12)
        self.assertAlmostEqual(parallel, 100 * math.sinh(.02) / 100, places=12)

    def test_key_rate_bucket_locality(self):
        risk = key_rate_dv01([(1, 100)], [(1, 0), (3, 0), (5, 0)])
        self.assertGreater(risk[1], 0)
        self.assertEqual(risk[3], 0)
        self.assertEqual(risk[5], 0)

    def test_empty_portfolio_risk_is_zero(self):
        self.assertEqual(parallel_dv01([], [(1, .03)]), 0)
        self.assertEqual(key_rate_dv01([], [(1, .03)]), {1: 0})

    def test_risk_rejects_invalid_or_unrepresentable_bumps(self):
        for bump in [0, -1, math.nan, math.inf, 1e-320]:
            with self.subTest(bump=bump), self.assertRaises(ValueError):
                parallel_dv01([(1, 100)], [(1, .03)], bump)
            with self.subTest(bump=bump), self.assertRaises(ValueError):
                key_rate_dv01([(1, 100)], [(1, .03)], bump)

    def test_risk_rejects_overflowed_central_difference_denominator(self):
        # The tiny maturity keeps exp finite, but 2*bump_bp would be +inf.
        # Do not turn a representable nonzero risk into a silent zero.
        t, bump = 1e-306, 1e308
        self.assertGreater(100 * math.sinh(t * (bump * BP)) / bump, 0)
        for risk in [parallel_dv01, key_rate_dv01]:
            with self.subTest(risk=risk.__name__), self.assertRaises(ValueError):
                risk([(t, 100)], [(t, 0)], bump)

    def test_unrepresentable_discounted_cashflow_rejected(self):
        with self.assertRaises(ValueError):
            price_cashflows([(1, 1e308)], [(1, -2)])


if __name__ == "__main__":
    unittest.main()
