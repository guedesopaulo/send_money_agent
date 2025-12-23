from typing import TypedDict, Optional, List

class TransferState(TypedDict):
    recipient: Optional[str]
    amount: Optional[float]
    country: Optional[str]
    delivery_method: Optional[str]
    is_confirmed: bool

def get_initial_state() -> TransferState:
    return {
        "recipient": None,
        "amount": None,
        "country": None,
        "delivery_method": None,
        "is_confirmed": False
    }