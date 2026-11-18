"""Load a frozen, normalized snapshot. No network or vendor dependency."""

from pathlib import Path

from scripts.curve_archive import load_snapshot, validate_snapshot


class DataCollector:
    """The config backend of the collector; future adapters return this schema."""

    def __init__(self, config: Path):
        self.config = config

    def collect(self, *, public: bool = True) -> dict:
        snapshot = validate_snapshot(load_snapshot(self.config))
        if public:
            for market in snapshot["markets"]:
                if market["rights"]["status"] == "HOLD" and market["nodes"]:
                    raise ValueError(f"public export blocked: {market['id']} has HOLD data")
        if not any(m["status"] == "AVAILABLE" for m in snapshot["markets"]):
            raise ValueError("snapshot has no available curves")
        return snapshot
