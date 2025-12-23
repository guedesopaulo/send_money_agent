import difflib
import json
from typing import Any

from .state import get_initial_state

# Internal "Database" for the session
current_state = get_initial_state()

SUPPORTED_COUNTRIES = [
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Cuba",
    "Dominican Republic",
    "Ecuador",
    "El Salvador",
    "Guatemala",
    "Haiti",
    "Honduras",
    "Mexico",
    "Nicaragua",
    "Panama",
    "Paraguay",
    "Peru",
    "Puerto Rico",
    "Uruguay",
    "Venezuela",
]
SUPPORTED_METHODS = ["Bank Transfer", "Cash Pickup", "Mobile Wallet"]

MOCK_CONTACTS = {
    "john": ["John Smith (ending in 1234)", "John Doe (ending in 5678)"],
    "sarah": ["Sarah Connor"],
    "bob": ["Bob Builder"],
}


def _update_country(country: str | None, feedback: list[str]) -> str | None:
    if not country:
        return None
    matches = difflib.get_close_matches(
        country.title(), SUPPORTED_COUNTRIES, n=1, cutoff=0.5
    )
    if matches:
        current_state["country"] = matches[0]
        feedback.append(f"Destination: {matches[0]}.")
        return None
    return f"Currently, we only support: {', '.join(SUPPORTED_COUNTRIES[:5])}..."


def _update_amount(amount: float | None, feedback: list[str]) -> str | None:
    if amount is None:
        return None
    try:
        val = round(float(amount), 2)
        if val > 0:
            current_state["amount"] = val
            feedback.append(f"Amount: ${val}.")
            return None
        return "Amount must be greater than zero."
    except ValueError:
        return "Please provide a valid numeric amount."


def _update_delivery_method(method: str | None, feedback: list[str]) -> str | None:
    if not method:
        return None
    mapping = {
        "transfer": "Bank Transfer",
        "deposit": "Bank Transfer",
        "wire": "Bank Transfer",
        "bank": "Bank Transfer",
        "cash": "Cash Pickup",
        "pickup": "Cash Pickup",
        "wallet": "Mobile Wallet",
        "walet": "Mobile Wallet",
        "mobile": "Mobile Wallet",
    }
    matched_formal = next(
        (formal for key, formal in mapping.items() if key in method.lower()), None
    )
    if matched_formal:
        current_state["delivery_method"] = matched_formal
        feedback.append(f"Method: {matched_formal}.")
        return None
    return f"Please choose a valid method: {', '.join(SUPPORTED_METHODS)}."


def update_transfer_details(
    recipient: str | None = None,
    amount: float | None = None,
    country: str | None = None,
    delivery_method: str | None = None,
) -> str:
    """Updates the money transfer details and handles normalization."""
    global current_state
    feedback: list[str] = []

    # Run sub-validators
    err = (
        _update_country(country, feedback)
        or _update_amount(amount, feedback)
        or _update_delivery_method(delivery_method, feedback)
    )
    if err:
        return err

    if recipient:
        current_state["recipient"] = recipient
        feedback.append(f"Recipient: {recipient}.")

    required = ["country", "amount", "recipient", "delivery_method"]
    missing = [k for k in required if current_state.get(k) is None]

    if not missing:
        return "Got everything! Let me provide the summary for your confirmation."

    missing_str = ", ".join(missing)
    return f"{' '.join(feedback)} (Still need: {missing_str})"


def lookup_recipient(name: str) -> str:
    """Checks if a name is ambiguous in the contact list."""
    if not name:
        return "Please provide a name to look up."

    search_name = name.lower().split()[0]
    hits = MOCK_CONTACTS.get(search_name, [])

    if len(hits) > 1:
        hits_str = ", ".join(hits)
        return f"AMBIGUOUS: Found {len(hits)} contacts: {hits_str}. Which one?"
    if len(hits) == 1:
        return f"Contact found: {hits[0]}"

    return f"New recipient '{name}' will be added."


def get_transfer_summary() -> str:
    """Provides a structured summary (JSON) and confirmation message."""
    global current_state
    required = ["country", "amount", "recipient", "delivery_method"]
    missing = [k for k in required if current_state.get(k) is None]

    if missing:
        msg = f"Incomplete. Still need: {', '.join(missing)}."
        return msg

    summary_data: dict[str, Any] = {
        "transfer_id": "TRANS-2025-XYZ",
        "recipient": current_state["recipient"],
        "destination_country": current_state["country"],
        "amount_usd": current_state["amount"],
        "method": current_state["delivery_method"],
        "status": "READY_FOR_CONFIRMATION",
    }

    payload = json.dumps(summary_data, indent=2)
    return (
        f"\n### FINAL TRANSFER SUMMARY ###\n"
        f"Recipient: {current_state['recipient']}\n"
        f"Destination: {current_state['country']}\n"
        f"Amount: ${current_state['amount']} USD\n"
        f"Delivery Method: {current_state['delivery_method']}\n"
        f"{'-' * 31}\nJSON DATA PAYLOAD:\n{payload}\n{'-' * 31}\n"
        f"Does everything look correct? Please say 'Confirm' to proceed."
    )


def complete_transfer() -> str:
    """Finalizes the transaction."""
    global current_state
    current_state["is_confirmed"] = True
    return "✅ SUCCESS: The transfer has been initiated. Thank you!"
