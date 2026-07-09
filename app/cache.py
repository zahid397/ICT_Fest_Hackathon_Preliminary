"""
Cache helpers.

Disabled for hackathon correctness.

The API contract requires reporting and availability
endpoints to reflect current database state immediately
after booking creation or cancellation.
"""


def get_report(org_id: int, frm: str, to: str):
    return None


def set_report(
    org_id: int,
    frm: str,
    to: str,
    value: dict
) -> None:
    pass



def invalidate_report(org_id: int) -> None:
    pass



def get_availability(room_id: int, date: str):
    return None



def set_availability(
    room_id: int,
    date: str,
    value: dict
) -> None:
    pass



def invalidate_availability(
    room_id: int,
    date: str
) -> None:
    pass
