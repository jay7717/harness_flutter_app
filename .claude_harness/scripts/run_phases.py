#!/usr/bin/env python3
"""
5-Phase Development Harness — CLI Orchestrator

외부 자동화용 Python CLI. Claude Code 내부에서는 /harness 스킬을 사용.

Usage:
    python run_phases.py new "기능 설명"
    python run_phases.py resume [session_id]
    python run_phases.py status [session_id]
    python run_phases.py list
    python run_phases.py stop [session_id]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = PROJECT_ROOT / "specs" / "sessions"
LATEST_FILE = PROJECT_ROOT / "specs" / "latest.txt"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:30]


def generate_session_id(feature: str) -> str:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(feature)
    return f"{now}_{slug}"


def init_state(session_id: str, feature: str) -> dict:
    return {
        "session_id": session_id,
        "feature": feature,
        "current_phase": 1,
        "status": "in_progress",
        "loopback_count": 0,
        "max_loopback": 3,
        "phases": {
            "1": {"status": "pending"},
            "2": {"status": "pending"},
            "3": {"status": "pending"},
            "4": {"status": "pending"},
            "5": {"status": "pending"},
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


def load_state(session_id: str) -> dict:
    state_path = SESSIONS_DIR / session_id / "state.json"
    with open(state_path) as f:
        return json.load(f)


def save_state(session_id: str, state: dict):
    state["updated_at"] = datetime.now().isoformat()
    state_path = SESSIONS_DIR / session_id / "state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_latest_session() -> str | None:
    if LATEST_FILE.exists():
        sid = LATEST_FILE.read_text().strip()
        if sid:
            return sid
    return None


def set_latest_session(session_id: str):
    LATEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    LATEST_FILE.write_text(session_id)


def cmd_new(feature: str):
    session_id = generate_session_id(feature)
    state = init_state(session_id, feature)
    save_state(session_id, state)
    set_latest_session(session_id)
    print(f"Created session: {session_id}")
    print(f"Path: specs/sessions/{session_id}/")
    print("Run phases with Claude Code: /harness --resume")


def cmd_status(session_id: str | None = None):
    sid = session_id or get_latest_session()
    if not sid:
        print("No active session.")
        return
    state = load_state(sid)
    phase_names = {
        "1": "Clarify",
        "2": "Context",
        "3": "Plan",
        "4": "Execute",
        "5": "Evaluate",
    }
    print(f"Session: {state['session_id']}")
    print(f"Feature: {state['feature']}")
    print(f"Status:  {state['status']}")
    print(f"Phase:   {state['current_phase']}")
    print(f"Loops:   {state['loopback_count']}/{state['max_loopback']}")
    print()
    for p, name in phase_names.items():
        s = state["phases"][p]["status"]
        icon = {"completed": "✅", "in_progress": "🔄", "skipped": "⏭️", "pending": "⬜", "failed": "❌"}.get(s, "?")
        print(f"  {icon} Phase {p}: {name} — {s}")


def cmd_list():
    if not SESSIONS_DIR.exists():
        print("No sessions.")
        return
    for d in sorted(SESSIONS_DIR.iterdir()):
        state_file = d / "state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text())
            print(f"  {state['session_id']}  Phase {state['current_phase']}  {state['status']}  {state['feature']}")


def cmd_stop(session_id: str | None = None):
    sid = session_id or get_latest_session()
    if not sid:
        print("No active session.")
        return
    state = load_state(sid)
    state["status"] = "stopped"
    save_state(sid, state)
    print(f"Stopped session: {sid}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "new":
        if len(sys.argv) < 3:
            print("Usage: run_phases.py new \"기능 설명\"")
            return
        cmd_new(" ".join(sys.argv[2:]))
    elif cmd == "status":
        cmd_status(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "list":
        cmd_list()
    elif cmd == "stop":
        cmd_stop(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "resume":
        sid = sys.argv[2] if len(sys.argv) > 2 else get_latest_session()
        if sid:
            print(f"Resume session {sid} in Claude Code: /harness --resume")
        else:
            print("No session to resume.")
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
