from state import get_initial_state
from tools import update_transfer_details, validate_transfer, get_final_confirmation

def run_test_scenario():
    state = get_initial_state()
    print("--- Send Money Agent Test ---")
    
    # Turn 1: Partial info
    print("\nUser: I want to send 100 dollars to Mexico.")
    update_transfer_details(state, amount=100, country="Mexico")
    print(f"Agent State: {state}")
    
    # Turn 2: Correction
    print("\nUser: Actually, make it 200 to Spain.")
    # Validation check
    val = validate_transfer({"country": "Spain", "amount": 200})
    print(f"Validation: {val}")
    update_transfer_details(state, amount=200, country="Spain")
    
    # Turn 3: Remaining info
    print("\nUser: To John Doe via Bank Transfer.")
    update_transfer_details(state, recipient="John Doe", delivery_method="Bank Transfer")
    
    # Turn 4: Final Summary
    if not state["missing_fields"]:
        print("\nAgent: All details gathered. Finalizing...")
        print(get_final_confirmation(state))

if __name__ == "__main__":
    run_test_scenario()