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
