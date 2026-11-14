# Cross-border settlement FX is not an FX forward curve

**Timestamp:** `2026-11-14T15:18:55+08:00` (Asia/Shanghai). **Status:** Public research note; no curve or dataset added.

[Tencent FiT](https://www.fitgroup.com/home) and [TenPay Global](https://www.tencent.com/products/tenpay-global/) provide the public product context. The upstream contributions below went to the official [WeChat Pay Global Skills repository](https://github.com/wechatpay-apiv3/wechatpay-global-skills); we did not verify a separate open TenPay Global FX-team repository.

The [payment-callback PR](https://github.com/wechatpay-apiv3/wechatpay-global-skills/pull/7) distinguishes order pricing, user payment, and merchant settlement currencies. The [reconciliation PR](https://github.com/wechatpay-apiv3/wechatpay-global-skills/pull/8) treats USD and HKD as separate totals. They are documentation changes tested against public specifications and offline examples; no live rates, payments, or settlements were sampled.

The [WeChat Pay settlement specification](https://pay.wechatpay.cn/doc/global/v3/en/4041899517) describes product-specific rates for converting a transaction or reconciling a statement. The [notification dictionary](https://pay.wechatpay.cn/doc/global/v3/en/4012356834) also specifies a scaled integer rate field. Neither gives a market FX forward curve: they do not supply matched market quotes at multiple maturities. For any future market curve contribution, record the pair and quote direction, observation timestamp, spot/forward tenor, value dates, conventions, sources, and redistribution rights. Keep transaction or statement rates separate from tradable market observations.

See the [P-Finance work log](https://github.com/pengpengyi92/p-finance/blob/main/log/2026-11-14-tencent-fit-cross-border-fx.md) for the upstream checks and examples.

## Validation update — `2026-11-14T15:36:56+08:00` (Asia/Shanghai)

The existing [WeChat Pay Skills #47](https://github.com/wechatpay-apiv3/wechatpay-skills/pull/47) also fixes a Windows PowerShell 5.1 encoding failure (commit `15fa471`). Offline signature verification passed for three synthetic P12 paths on both Windows PowerShell 5.1 and PowerShell 7. This validates a local integration tool only; it adds no market data, exchange-rate observation, or curve.
