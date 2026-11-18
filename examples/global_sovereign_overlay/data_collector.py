"""Load a frozen, normalized snapshot. No network or vendor dependency."""

from datetime import date
from pathlib import Path

from scripts.curve_archive import load_snapshot, validate_snapshot


class DataCollector:
    """The config backend of the collector; future adapters return this schema."""

    def __init__(self, config: Path):
        self.config = config

    def collect(self, *, public: bool = True) -> dict:
        payload = load_snapshot(self.config)
        has_target = isinstance(payload, dict) and "target_market_date" in payload
        target = payload.pop("target_market_date") if has_target else None
        snapshot = validate_snapshot(payload)
        if has_target:
            try:
                if date.fromisoformat(target).isoformat() != target:
                    raise ValueError
            except (TypeError, ValueError):
                raise ValueError("target_market_date must be YYYY-MM-DD") from None
            if target > snapshot["generated_at"][:10]:
                raise ValueError("target market date cannot follow the compilation date")
            if any(m["market_date"] and m["market_date"] > target for m in snapshot["markets"]):
                raise ValueError("market observation cannot be after target_market_date")
            snapshot["target_market_date"] = target
        if public:
            for market in snapshot["markets"]:
                if market["rights"]["status"] == "HOLD" and market["nodes"]:
                    raise ValueError(f"public export blocked: {market['id']} has HOLD data")
        if not any(m["status"] == "AVAILABLE" for m in snapshot["markets"]):
            raise ValueError("snapshot has no available curves")
        return snapshot
