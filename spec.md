# Markdown Task Board Generator Specification

## Objective
A lightweight Python CLI tool that parses tasks from Markdown files, organizes them into Kanban-like columns (`TODO`, `IN_PROGRESS`, `DONE`), computes completion metrics, and formats them into an ASCII/Markdown board.

## Data Structures
- `TaskItem(id: str, title: str, status: str, priority: str, tags: list[str])`
- `TaskBoard(title: str, tasks: list[TaskItem])`

## API Interface
- `TaskBoard.from_markdown(text: str) -> TaskBoard`
- `TaskBoard.render_ascii() -> str`
- `TaskBoard.render_markdown() -> str`
- `TaskBoard.completion_rate() -> float`

## CLI Interface
- `python3 -m task_board <markdown_file> [--format ascii|markdown]`
