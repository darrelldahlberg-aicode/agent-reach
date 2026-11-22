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
    assert "--timeout" in run.call_args.args[0]


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


def test_native_envelope_text_is_preserved():
    items = [{"url": "https://example.org/article", "title": "Article", "text": "Verified text"}]
    with patch("agent_reach.workspace.subprocess.run", return_value=_result(items)):
        out = research("aaron", "web", "marketing")
    assert out["findings"][0]["evidence"] == "Verified text"


def test_no_source_does_not_create_finding():
    with patch("agent_reach.workspace.subprocess.run", return_value=_result([{"title": "Missing URL"}])):
        assert jade("stores")["findings"] == []


def test_runner_emits_json(capsys):
    from agent_reach import workspace_runner
    with patch("agent_reach.workspace_runner.research", return_value={"ok": True, "findings": []}):
        code = workspace_runner.main(["jade", "web", "furniture stores"])
    assert code == 0
    assert json.loads(capsys.readouterr().out)["ok"]


def test_runner_returns_failure(capsys):
    from agent_reach import workspace_runner
    with patch("agent_reach.workspace_runner.research", return_value={"ok": False, "findings": []}):
        code = workspace_runner.main(["aaron", "web", "test"])
    assert code == 1
