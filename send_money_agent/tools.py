import json
from .state import get_initial_state

# This is our live "Database" for the session
current_state = get_initial_state()

def update_transfer_details(recipient: str = None, amount: float = None, country: str = None, delivery_method: str = None) -> str:
    """Updates the money transfer details with any information provided."""
    global current_state
    
    if recipient: current_state["recipient"] = recipient
    if amount: current_state["amount"] = amount
    if country: current_state["country"] = country
    if delivery_method: current_state["delivery_method"] = delivery_method
    
    # Calculate what is still missing
    missing = [k for k, v in current_state.items() if v is None and k != "is_confirmed"]
    
    if not missing:
        return "All details collected. You can now show the summary and ask for confirmation."
    return f"State updated. Still missing: {', '.join(missing)}"

def get_transfer_summary() -> str:
    """Returns a JSON summary of all gathered information."""
    global current_state
    return json.dumps(current_state, indent=2)

def complete_transfer() -> str:
    """Finalizes the transfer."""
    global current_state
    current_state["is_confirmed"] = True
    return "SUCCESS: Transfer initiated."