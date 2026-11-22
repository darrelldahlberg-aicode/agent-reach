"""CLI bridge for scheduled Jade, Aaron, and AI Learning Brain jobs.

Usage: python -m agent_reach.workspace_runner jade web "furniture stores"
       python -m agent_reach.workspace_runner aaron youtube "furniture ads"
       python -m agent_reach.workspace_runner ai_learning_brain youtube "AI trends"
"""
import argparse
import json
import sys

from agent_reach.workspace import ROLES, research


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only AI Agent Workspace research")
    parser.add_argument("role", choices=sorted(ROLES))
    parser.add_argument("platform")
    parser.add_argument("query")
    args = parser.parse_args(argv)
    output = research(args.role, args.platform, args.query)
    print(json.dumps(output, ensure_ascii=False))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
