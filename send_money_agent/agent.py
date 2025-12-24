from google.adk.agents.llm_agent import Agent

from .state import get_initial_state
from .tools import complete_transfer
from .tools import get_transfer_summary
from .tools import lookup_recipient
from .tools import update_transfer_details

AGENT_INSTRUCTION = """
You are a 'Send Money' expert. Your job is to fill the transfer state using tools.

1. EXTRACTION: When users give info, call 'update_transfer_details'.
2. VERBATIM SUMMARY: When you call 'get_transfer_summary', you MUST print the
   tool's response EXACTLY as it is returned.
   - DO NOT summarize it.
   - DO NOT skip the JSON block.
   - Copy-paste the entire text from the tool into the chat.
3. REPETITION: If the user says "send it again" or "show me the summary",
   call 'get_transfer_summary' again and show the full text.
4. CONFIRMATION: Once the summary is shown, wait for a 'Yes' or 'Confirm'
   before calling 'complete_transfer'.
5. CORRECTIONS: If the user wants to change something
   (e.g., 'Change country to Brazil'), call 'update_transfer_details'
   and then show the new summary.
"""

initial_state = get_initial_state()

root_agent = Agent(
    model="gemini-flash-lite-latest",
    name="send_money_agent",
    description=(
        "Professional Send Money Agent with normalization and ambiguity handling."
    ),
    instruction=AGENT_INSTRUCTION,
    tools=[
        update_transfer_details,
        lookup_recipient,
        get_transfer_summary,
        complete_transfer,
    ],
)
