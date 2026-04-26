"""Reusable OpenAPI (drf-spectacular) parameters and helpers."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

# JWT security scheme referenced in SPECTACULAR_SETTINGS['APPEND_COMPONENTS'].
JWT_AUTH = [{"jwtAuth": []}]


def param_ordering(description: str) -> OpenApiParameter:
    return OpenApiParameter(
        name="ordering",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description=description,
        required=False,
    )


def param_limit(default: int, maximum: int) -> OpenApiParameter:
    return OpenApiParameter(
        name="limit",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description=f"Maximum number of records returned (1–{maximum}; default {default}).",
        required=False,
    )


def param_is_active_donations() -> OpenApiParameter:
    return OpenApiParameter(
        name="is_active",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="`true` (default): active campaigns only. `false`: inactive. `all`: all campaigns.",
        required=False,
    )
