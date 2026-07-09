"""Helpers for parsing input datetimes and rendering UTC responses."""

from datetime import datetime, timezone


def parse_input_datetime(value: str) -> datetime:
    """
    Parse ISO 8601 datetime.

    Rules:
    - Offset datetime -> convert to UTC
    - Naive datetime -> treat as UTC
    - Stored value remains naive UTC
    """

    dt = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


    if dt.tzinfo is not None:
        dt = dt.astimezone(
            timezone.utc
        ).replace(
            tzinfo=None
        )

    return dt



def iso_utc(dt: datetime) -> str:
    """
    Render stored naive UTC datetime
    with explicit UTC offset.
    """

    return (
        dt.replace(
            tzinfo=timezone.utc
        )
        .isoformat()
    )
