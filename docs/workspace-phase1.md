# Phase 1: AI Agent Workspace connector

The adapter lives at `agent_reach/workspace.py`. It is read-only and calls the installed `agent-reach` CLI.

## Usage

```python
from agent_reach.workspace import jade, aaron, ai_learning_brain, health

print(jade("furniture stores in Texas"))
print(aaron("furniture store holiday promotions"))
print(ai_learning_brain("AI agent tutorials"))
print(health("youtube"))
```

The three role entry points return normalized findings with URLs, retrieval timestamps, hashes, and `needs_review` status. They do not publish, message, or write to any brain. Callers must explicitly approve and ingest research.

## Setup and tests

Install the project and its development extras using the repository's installation guidance, then run:

```bash
python -m pytest tests/test_workspace.py -q
agent-reach channels
agent-reach check youtube --search
```

The tests mock the CLI and require no platform credentials. Live channel tests are separate and must be run on the intended host. Experimental or authenticated platforms are not enabled by this phase. Search uses each channel's declared backends. The CLI handles backend selection and reports setup, login, and provider errors.

## Phase 1 boundaries

This repository supplies shared research entry points. Integration with external scheduled Jade/Aaron automations and the persistent AI Learning Brain requires configuring those runtimes to call this module. No deployment or automation configuration is performed by this commit.

## Runtime wiring

The installed module provides three callable entry points: `jade(query)`, `aaron(query)`, and `ai_learning_brain(query)`. To activate them in scheduled agent workflows, install this repository in the execution environment and call these functions from the relevant agent's job. Results are read-only research candidates; do not treat them as verified until reviewed.

## Test report

Nine mocked unit tests are included. GitHub Actions runs them on pushes to the workspace adapter and tests. Live platform access, production agent runtime wiring, and persistent Brain ingestion are separate acceptance checks and are not asserted complete by these tests.
