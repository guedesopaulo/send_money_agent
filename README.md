# Send Money Agent (Google ADK Demo)

A conversational Send Money Agent built using Google ADK, designed to guide users through a money transfer flow in a natural, multi-turn conversation.

This project was created as a technical assessment demo, focusing on:

- state tracking across turns
- partial information handling
- ambiguity resolution (e.g. recipient names)
- tool-driven orchestration with an LLM

No real integrations are used — all validations and lookups are mocked.


# Core Concepts

- State (state.py)
    - Stored in memory for the session
    - Tracks collected and missing fields

- Tools (tools.py)
    - update_transfer_details
    - lookup_recipient
    - get_transfer_summary
    - complete_transfer

- Agent (agent.py)
    - Enforces tool usage rules
    - Controls confirmation and repetition behavior
    - Prevents unsafe progression (e.g. new recipient without confirmation)

# Installation

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv --version
```

## Quick Start

```bash
# Run the default setup (creates env, syncs dependencies, installs pre-commit)
make
```

The `make` command creates a virtual environment and installs the project dependencies.

### Available Make Commands

```bash
make              # Default: setup environment, sync deps, install hooks
make deps         # Sync dependencies and install pre-commit hooks (uv sync + pre-commit install)
make check        # Run pre-commit hooks against all files
make clean        # Clean cache and build artifacts
```

# Run

Run the agent in a terminal:

```bash
uv run adk run send_money_agent
```

Or start the web UI (client) on port 8000:

```bash
uv run adk web --port 8000
```

Then open your browser at http://localhost:8000 (or change the `--port` value).

# Next Steps

To further enhance the Send Money Agent, here are some potential improvements and future directions:

1. **Chat History on State**:
   - Extend the state to include a `chat_history` field to track the raw conversation history.
   - In the future, implement a database (e.g., SQLite) to persist chat history across sessions for better context retention.

2. **Dynamic Tool Registration**:
   - Refactor the agent to use a dynamic tool registration system.
   - This will make the agent more modular and extensible, allowing tools to be added or removed without modifying the core agent code.

3. **Simplistic State Representation**:
   - Improve the current flat state structure to support more complex scenarios, such as multi-recipient transfers or nested data.
   - Consider using a class-based state representation for better encapsulation and validation.

4. **Hardcoded Data**:
   - Replace hardcoded data (e.g., supported countries, delivery methods, mock contacts) with external configuration files or a database.
   - This will make the agent easier to maintain and scale.

5. **No Logging or Debugging**:
   - Add logging to capture tool inputs, outputs, and errors for better debugging and monitoring.
   - Use a structured logging library to ensure logs are easy to analyze.

6. **No Unit Tests**:
   - Write unit tests for the agent, tools, and state management to ensure reliability and prevent regressions.
   - Use a testing framework like `pytest` to automate and manage tests.
   - Implement CI on github/gitlab with pipeline test

7. **No Guardrails**:
   - Implement guardrails to handle unexpected inputs or edge cases.
   - For example, validate user inputs, handle ambiguous responses, and provide fallback mechanisms for tool failures.
