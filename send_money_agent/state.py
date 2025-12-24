from typing import Literal
from typing import TypedDict


class TransferState(TypedDict):
    recipient: str | None
    amount: float | None
    country: str | None
    delivery_method: str | None
    is_confirmed: bool
    status: Literal["COLLECTING", "AWAITING_CONFIRMATION", "COMPLETED"]


def get_initial_state() -> TransferState:
    return {
        "recipient": None,
        "amount": None,
        "country": None,
        "delivery_method": None,
        "is_confirmed": False,
        "status": "COLLECTING",
    }
