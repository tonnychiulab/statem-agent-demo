# Markdown 任務看板產生器 (StateM 治理示範專案)

[English](README.md) | [繁體中文](README_zh-TW.md)

本專案是一個完整的實戰範例，展示如何使用 **[StateM](https://github.com/henryqin1997/statem)**（專為可靠 AI Agent 長程任務設計的輕量級狀態機運行環境）來構建、驗證防禦與交付 Python 應用。

---

## 🎯 這是什麼專案？

本專案包含兩大核心部分：
1. **Python CLI 應用程式 (`task_board`)**：
   - 解析 Markdown 待辦清單（支援 `- [ ]` 未完成、`- [~]` 進行中、`- [x]` 已完成）。
   - 自動辨識標籤（如 `#security`）與優先級（如 `!HIGH`）。
   - 渲染成直觀的 ASCII 終端看板或精美的 Markdown 看板，並即時計算完成率指標。
2. **StateM 運作規格書 (`runbook.yaml`)**：
   - 以正式的程序性狀態機（Procedural State Machine）引導專案的完整生命週期（`setup` -> `design` -> `develop` -> `verify` -> `complete`）。
   - 具備自動化狀態轉移守衛（Transition Gates），防止 Agent 過早交付或跳過關鍵驗證。

---

## 🛡️ StateM 治理生命週期

本專案依照嚴謹的狀態機路徑進行推進：

```text
[setup] ---> [design] ---> [develop] <---> [verify] ---> [complete]
  準備         設計         實作開發         驗證測試         完成交付
```

### 實測驗證的核心守衛機制（Transition Gates）
- **條件斷言檢查（Predicate Gate）**：在 `design` 階段設定了 `predicate: spec.md, exists=True`。當規格書 `spec.md` 尚未建立時，執行 `statem goto develop` 會被立即**強制攔截並阻擋**，確保「未經規格定義不得實作」。
- **自動化指令檢驗（Automated Command Gate）**：在 `verify` 階段設定了 `before_transfer` 自動執行 `python3 -m unittest discover`。只有在所有單元測試 100% 通過的情況下，才允許流轉至 `complete` 交付階段。
- **不可篡改的稽核記錄（Audit Trail）**：所有狀態跳躍、條件檢驗與被攔截的事件，皆持久化記錄在 `.statem/` 目錄中。

### 實際 StateM 運行歷史紀錄
```text
Run: taskboard-v1
Current: complete
- 2026-09-10T11:15:06Z start setup
- 2026-09-10T11:15:06Z in_hook setup
- 2026-09-10T11:15:44Z goto setup -> design
- 2026-09-10T11:15:54Z goto_blocked before_transfer (阻擋成功：spec.md 缺失時拒絕進入實作)
- 2026-09-10T11:18:06Z goto design -> develop (補齊 spec.md 後順利通過)
- 2026-09-10T11:28:56Z goto develop -> verify
- 2026-09-10T11:29:03Z goto verify -> complete (自動執行 unittest 通過：4/4 測試通過後交付)
```

---

## 🚀 快速上手

### 1. 執行任務看板 CLI 工具

```bash
# 輸出 ASCII 終端看板
python3 -m task_board example_tasks.md --format ascii

# 輸出 Markdown 總結格式
python3 -m task_board example_tasks.md --format markdown
```

#### ASCII 看板輸出範例：
```text
=== Project Task Board [Progress: 40.0%] ===
+----------------------------+----------------------------+----------------------------+
|            TODO            |        IN_PROGRESS         |            DONE            |
+----------------------------+----------------------------+----------------------------+
| TASK-003: Design high-avai | TASK-005: Implement OAuth2 | TASK-006: Setup StateM pip |
| TASK-004: Add GraphQL API  |                            | TASK-007: Initial codebase |
+----------------------------+----------------------------+----------------------------+
```

### 2. 執行自動化測試

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

### 3. 檢視或重新執行 StateM 流程

```bash
# 驗證 runbook.yaml 語法與規則結構
statem validate runbook.yaml

# 查看目前 Run 的當前狀態與指示
statem cur --run-id taskboard-v1

# 查看整個狀態流轉與阻擋審計歷史
statem history --run-id taskboard-v1
```

---

## 📄 授權條款
MIT License
