# Agent Master Researcher

Product identity: **Agent Master Researcher**

Canonical repository: `agent-master-researcher` (rename verified).

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
1. Repository rename completed; original repository identity preserved.
2. Update local clone remotes, CI references, deployment settings, and any cross-repository references.
3. Keep the underlying upstream Agent Reach CLI and package naming unchanged until dependent code is migrated and tested.
4. Run the workspace unit tests and live channel smoke tests after migration.

## Approved architecture decision

Agent Master Researcher belongs under AI Agent Workspace > Advertising Recon. It is a standalone shared research service, not a child of Furniture Intel or Ad Spy. Consumers include Furniture Intel (industry intelligence), Ad Spy (advertising analysis), Price Intel (competitive pricing), Social Sales Floor (social selling trends), Content Creation Engine (creative research), AI Learning Brain (technology trends), Jade (prospect research), and Aaron (campaign strategy). Research collection is centralized; downstream products own analysis and execution. These are intended integration boundaries, not a claim of live connections.

Owner of next implementation step: engineering / workspace integration. Remaining acceptance checks: execute unit tests, verify live public research, wire scheduled agents, and update dependent repository references. Repository visibility was public when checked; keep client-specific or proprietary data out of public commits.
