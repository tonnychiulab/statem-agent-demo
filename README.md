# Markdown Task Board Generator (StateM Governed Project)

[English](README.md) | [繁體中文](README_zh-TW.md)

A complete demonstration of building, verifying, and delivering a Python project governed by **[StateM](https://github.com/henryqin1997/statem)** — a lightweight state machine runtime for reliable AI agent workflows.

---

## 🎯 What is this project?

This project contains:
1. **A Python CLI Application (`task_board`)**: Parses markdown checklists (`- [ ]`, `- [~]`, `- [x]`), detects tags (`#security`) and priorities (`!HIGH`), and renders an ASCII or Markdown Kanban board with completion metrics.
2. **StateM Runbook (`runbook.yaml`)**: A formal procedural state machine that guided the entire lifecycle of this project (setup -> design -> develop -> verify -> complete) with automated transition gates.

---

## 🛡️ StateM Governance Lifecycle

The project workflow followed this state machine:

```text
[setup] ---> [design] ---> [develop] <---> [verify] ---> [complete]
```

### Transition Gates Demonstrated
- **Predicate Check in `design`**: Blocked transition to `develop` if `spec.md` was missing.
- **Automated Command Gate in `verify`**: Executed `python3 -m unittest discover` before allowing the pipeline to complete.
- **Audit History**: State transitions and blocking events are recorded in `.statem/`.

### Verified StateM Run History
```text
Run: taskboard-v1
Current: complete
- 2026-09-10T11:15:06Z start setup
- 2026-09-10T11:15:06Z in_hook setup
- 2026-09-10T11:15:44Z goto setup -> design
- 2026-09-10T11:15:54Z goto_blocked before_transfer (blocked because spec.md was missing!)
- 2026-09-10T11:18:06Z goto design -> develop (passed after spec.md created)
- 2026-09-10T11:28:56Z goto develop -> verify
- 2026-09-10T11:29:03Z goto verify -> complete (automated unittest gate passed: 4/4 tests OK)
```

---

## 🚀 Quick Start

### 1. Run the Task Board CLI

```bash
# Render ASCII Kanban Board
python3 -m task_board example_tasks.md --format ascii

# Render Markdown Summary
python3 -m task_board example_tasks.md --format markdown
```

### 2. Run Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

### 3. Inspect or Re-run the StateM Runbook

```bash
# Validate runbook spec
statem validate runbook.yaml

# Check current run status
statem cur --run-id taskboard-v1

# View execution history
statem history --run-id taskboard-v1
```

---

## 📄 License
MIT
