"""Load a frozen, normalized snapshot. No network or vendor dependency."""

from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from scripts.curve_archive import load_snapshot, validate_snapshot


def _iso_date(value: str, field: str) -> str:
    try:
        if date.fromisoformat(value).isoformat() == value:
            return value
    except (TypeError, ValueError):
        pass
    raise ValueError(f"{field} must be YYYY-MM-DD")


def _validate_points(snapshot: dict, points: dict) -> None:
    markets = {m["id"]: m for m in snapshot["markets"] if m["status"] == "AVAILABLE"}
    if not isinstance(points, dict) or set(points) - markets.keys():
        raise ValueError("point_observations must map available market IDs")
    for key, observations in points.items():
        market = markets[key]
        tenors = {n["tenor"] for n in market["nodes"] if n["yield_pct"] is not None}
        if not isinstance(observations, dict) or set(observations) != tenors:
            raise ValueError("point_observations must cover every plotted tenor")
        days = []
        for observation in observations.values():
            if (not isinstance(observation, dict)
                    or set(observation) != {"market_date", "source_url"}
                    or not isinstance(observation["source_url"], str)):
                raise ValueError("each point requires a market date and source URL")
            days.append(_iso_date(observation["market_date"], "point market date"))
            url = urlsplit(observation["source_url"])
            if url.scheme != "https" or not url.hostname or url.username or url.password:
                raise ValueError("point source must be a public HTTPS URL")
        if max(days) != market["market_date"]:
            raise ValueError("market_date must match the latest point date")


class DataCollector:
    """The config backend of the collector; future adapters return this schema."""

    def __init__(self, config: Path):
        self.config = config

    def collect(self, *, public: bool = True) -> dict:
        payload = load_snapshot(self.config)
        has_target = isinstance(payload, dict) and "target_market_date" in payload
        target = payload.pop("target_market_date") if has_target else None
        has_points = isinstance(payload, dict) and "point_observations" in payload
        points = payload.pop("point_observations") if has_points else None
        snapshot = validate_snapshot(payload)
        if has_target:
            _iso_date(target, "target_market_date")
            if target > snapshot["generated_at"][:10]:
                raise ValueError("target market date cannot follow the compilation date")
            if any(m["market_date"] and m["market_date"] > target for m in snapshot["markets"]):
                raise ValueError("market observation cannot be after target_market_date")
            snapshot["target_market_date"] = target
        if has_points:
            _validate_points(snapshot, points)
            snapshot["point_observations"] = points
        if public:
            for market in snapshot["markets"]:
                if market["rights"]["status"] == "HOLD" and market["nodes"]:
                    raise ValueError(f"public export blocked: {market['id']} has HOLD data")
        if not any(m["status"] == "AVAILABLE" for m in snapshot["markets"]):
            raise ValueError("snapshot has no available curves")
        return snapshot
