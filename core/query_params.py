"""Parsing seguro de query string para listagens (ordenação e limite)."""


def parse_limit(request, default: int, maximum: int) -> int:
    try:
        n = int(request.query_params.get("limit", default))
    except (TypeError, ValueError):
        n = default
    return max(1, min(n, maximum))


def parse_ordering(request, default: str, allowed: frozenset[str]) -> list[str]:
    raw = (request.query_params.get("ordering") or default).strip()
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    validated = [p for p in parts if p in allowed]
    if not validated:
        validated = [default] if default in allowed else []
    return validated
