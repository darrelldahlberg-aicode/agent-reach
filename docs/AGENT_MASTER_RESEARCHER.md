# Agent Master Researcher

Product identity: **Agent Master Researcher**

Planned repository name: `agent-master-researcher` (GitHub repository rename pending).

## Mission
Shared, read-only research agent for advertising reconnaissance and client intelligence. Collect cited public information on competitors, customer demand, creative trends, retail promotions, and relevant industry developments. Return evidence-linked briefs to downstream agents.

## Consumers
- Ad Spy and Furniture Intel: competitor intelligence
- Aaron: campaign strategy and ad research
- Jade: prospect and client research
- AI Learning Brain: creator and technology trends
- Social Sales Floor: approved research inputs for marketing workflows

## Guardrails
- Preserve source URLs, retrieval dates, and uncertainty.
- Keep research separate from publishing and customer outreach.
- Do not represent estimates as verified advertising performance.
- Require review before permanent knowledge ingestion.
- Never auto-enable authenticated channels or copy browser sessions.

## Migration checklist
1. Rename GitHub repository from `agent-reach` to `agent-master-researcher` in repository Settings.
2. Update local clone remotes, CI references, deployment settings, and any cross-repository references.
3. Keep the underlying upstream Agent Reach CLI and package naming unchanged until dependent code is migrated and tested.
4. Run the workspace unit tests and live channel smoke tests after migration.
