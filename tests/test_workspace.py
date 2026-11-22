"""Unit tests for workspace research adapter. All CLI interactions are mocked."""
import json
import subprocess
from unittest.mock import patch

from agent_reach.workspace import research, jade, aaron, ai_learning_brain, channels


def _result(items, ok=True, code=0):
    return subprocess.CompletedProcess([], code, json.dumps({"ok": ok, "items": items}), "")


def test_jade_deduplicates_and_tracks_source():
    items = [{"url": "https://example.com/store?ref=ad", "title": "Store", "snippet": "Sale"},
             {"url": "https://example.com/store?ref=other", "title": "Duplicate"}]
    with patch("agent_reach.workspace.subprocess.run", return_value=_result(items)) as run:
        out = jade("furniture retailer")
    assert out["ok"] and len(out["findings"]) == 1
    assert out["findings"][0]["source_url"] == "https://example.com/store"
    assert out["findings"][0]["status"] == "needs_review"
    assert "--backend" in run.call_args.args[0]
    assert "public-web" in run.call_args.args[0]


def test_aaron_routes_to_web():
    with patch("agent_reach.workspace.subprocess.run", return_value=_result([])):
        assert aaron("furniture promotions")["ok"]


def test_brain_routes_to_youtube():
    with patch("agent_reach.workspace.subprocess.run", return_value=_result([])) as run:
        assert ai_learning_brain("creator videos")["ok"]
    assert run.call_args.args[0][1:3] == ["youtube", "search"]


def test_denies_role_channel_mismatch():
    with patch("agent_reach.workspace.subprocess.run") as run:
        result = research("jade", "instagram", "test")
    assert not result["ok"]
    run.assert_not_called()


def test_cli_failure_is_reported():
    with patch("agent_reach.workspace.subprocess.run", side_effect=subprocess.TimeoutExpired("cli", 35)):
        assert not jade("competitor")["ok"]


def test_channels_metadata():
    with patch("agent_reach.workspace.subprocess.run", return_value=_result([])):
        assert channels()["ok"]


def test_rejects_invalid_urls():
    with patch("agent_reach.workspace.subprocess.run", return_value=_result([{"url": "file:///etc/passwd"}])):
        assert jade("prospect")["findings"] == []
