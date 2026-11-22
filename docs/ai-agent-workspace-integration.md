# AI Agent Workspace integration plan

Status: approved architecture; implementation pending.

## Goal
Use Agent Reach as the shared, read-only research layer for the AI Agent Workspace. Preserve upstream Agent Reach behavior and keep research separate from publishing or outreach.

## Agent connections
| Agent | Research input | Output |
| --- | --- | --- |
| Jade Sales | Public prospect websites, competitor profiles, relevant social conversations | Cited prospect briefs and outreach research |
| Aaron Campaign Advisor | Competitor promotions, customer discussions, video trends | Campaign opportunities and creative briefs |
| Adley Reporting Analyst | Public market and competitor context | Clearly labeled qualitative context, never fabricated campaign metrics |
| Furniture Intel / Furniture Brain | Furniture retailers, products, trends, discussions | Source-linked intelligence for review before ingestion |
| AI Learning Brain | Creator videos, transcripts, repositories | Dated creator insights and content ideas |
| Content Agent | Approved research briefs | Scripts, posts and carousel concepts for approval |

## Integration contract
- Implement a separate workspace adapter that calls the supported `agent-reach` CLI. Do not modify upstream channel internals.
- Normalize outputs to `{query, platform, source_url, title, author, published_at, retrieved_at, excerpt, summary, evidence, status}`.
- Keep source URLs, retrieval timestamps, and provenance. Label unavailable, login-required, and experimental channels.
- Deduplicate by canonical source URL and content hash; store research separately from approved knowledge.
- Apply request timeouts, per-channel rate limits, retries with bounded backoff, and a clear error status.
- Run channel availability checks before assigning research tasks. Never claim a platform is operational without a successful test.
- Do not copy browser sessions or enable authenticated channels without explicit user approval. Store credentials locally outside git.
- Do not allow research results to trigger publishing, messaging, account changes, or automatic permanent memory ingestion.

## First delivery
1. Inspect current CLI commands and installation documentation.
2. Build a typed adapter and normalized research schema.
3. Add channel health/status and failure reporting.
4. Connect Jade, Aaron, and AI Learning Brain through a shared research interface.
5. Add furniture competitor research workflow and source-linked briefs.
6. Add unit tests using mocked CLI responses and an opt-in live smoke test.
7. Document setup, permissions, costs, and rollback.

## Acceptance criteria
- A single research request returns consistent structured data across supported channels.
- Each finding has a traceable source and timestamp.
- Unavailable or login-required channels fail gracefully.
- Jade and Aaron receive research without direct access to credentials.
- Brain ingestion requires review.
- No outbound social actions occur through Agent Reach.

This file records the approved implementation plan. It does not claim that the adapter, deployment, or tests already exist.
