"""Read-only Agent Reach adapter for the AI Agent Workspace.

Requires the installed agent-reach CLI. No credentials are passed to subprocesses.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

ALLOWED = {"youtube", "github", "web", "reddit", "twitter", "facebook", "instagram", "linkedin"}
ROLES = {
    "jade": {"web", "github", "reddit", "linkedin"},
    "aaron": {"web", "youtube", "reddit", "facebook", "instagram"},
    "ai_learning_brain": {"web", "youtube", "github"},
}


def _canonical(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.netloc:
        return ""
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/", "", ""))


def _run(args: list[str], timeout: int = 35) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["agent-reach", *args], capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        payload = json.loads(proc.stdout)
        if not isinstance(payload, dict):
            raise ValueError("expected JSON object")
        if proc.returncode != 0 or not payload.get("ok", False):
            return {"ok": False, "error": payload.get("error") or {"message": "CLI failed"}}
        return payload
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": {"message": str(exc), "type": type(exc).__name__}}


def channels() -> dict[str, Any]:
    """Read declared channel capabilities. Does not imply live availability."""
    return _run(["channels"])


def health(platform: str) -> dict[str, Any]:
    if platform not in ALLOWED:
        return {"ok": False, "error": {"message": "Unsupported platform"}}
    return _run(["check", platform, "--search"], timeout=75)


def research(role: str, platform: str, query: str, *, timeout: int = 35) -> dict[str, Any]:
    """Run a search and normalize source-backed findings. Never runs login or write commands."""
    if role not in ROLES or platform not in ROLES[role]:
        return {"ok": False, "error": {"message": "Role or platform not allowed"}, "findings": []}
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        return {"ok": False, "error": {"message": "Invalid query"}, "findings": []}
    response = _run([platform, "search", query.strip(), "--backend", "public-web"], timeout)
    if not response["ok"]:
        return {"ok": False, "error": response["error"], "findings": []}
    raw = response.get("items", [])
    if not isinstance(raw, list):
        raw = response.get("result", {}).get("items", []) if isinstance(response.get("result"), dict) else []
    findings = []
    seen = set()
    for item in raw if isinstance(raw, list) else []:
        if not isinstance(item, dict):
            continue
        url = _canonical(str(item.get("url") or item.get("link") or item.get("source_url") or ""))
        if not url or url in seen:
            continue
        seen.add(url)
        excerpt = str(item.get("description") or item.get("snippet") or item.get("text") or "")
        findings.append({
            "query": query, "platform": platform, "source_url": url,
            "title": str(item.get("title") or ""), "author": str(item.get("author") or ""),
            "published_at": item.get("published_at") or item.get("published"),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "excerpt": excerpt[:4000], "summary": "", "evidence": excerpt[:4000],
            "status": "needs_review",
            "content_hash": hashlib.sha256((url + excerpt).encode()).hexdigest(),
        })
    return {"ok": True, "role": role, "platform": platform, "findings": findings,
            "raw_count": len(raw) if isinstance(raw, list) else 0}


def jade(query: str) -> dict[str, Any]:
    return research("jade", "web", query)


def aaron(query: str) -> dict[str, Any]:
    return research("aaron", "web", query)


def ai_learning_brain(query: str) -> dict[str, Any]:
    return research("ai_learning_brain", "youtube", query)
