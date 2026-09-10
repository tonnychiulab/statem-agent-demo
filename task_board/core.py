import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TaskItem:
    id: str
    title: str
    status: str = "TODO"  # "TODO", "IN_PROGRESS", "DONE"
    priority: str = "NORMAL"  # "LOW", "NORMAL", "HIGH"
    tags: List[str] = field(default_factory=list)

    def is_done(self) -> bool:
        return self.status == "DONE"

class TaskBoard:
    def __init__(self, title: str = "Task Board"):
        self.title = title
        self.tasks: List[TaskItem] = []

    def add_task(self, task: TaskItem):
        self.tasks.append(task)

    @classmethod
    def from_markdown(cls, text: str, default_title: str = "Task Board") -> "TaskBoard":
        board = cls(title=default_title)
        lines = text.strip().splitlines()
        
        task_pattern = re.compile(r"^[-*]\s+\[(?P<state>[ xX~])\]\s+(?P<content>.*)$")
        tag_pattern = re.compile(r"#([a-zA-Z0-9_\-]+)")
        prio_pattern = re.compile(r"!(HIGH|LOW|NORMAL)", re.IGNORECASE)

        for idx, line in enumerate(lines, 1):
            line = line.strip()
            match = task_pattern.match(line)
            if not match:
                continue
            
            state_char = match.group("state")
            content = match.group("content").strip()

            if state_char.lower() == "x":
                status = "DONE"
            elif state_char == "~":
                status = "IN_PROGRESS"
            else:
                status = "TODO"

            prio_match = prio_pattern.search(content)
            priority = prio_match.group(1).upper() if prio_match else "NORMAL"

            tags = tag_pattern.findall(content)

            clean_title = tag_pattern.sub("", content)
            clean_title = prio_pattern.sub("", clean_title).strip()

            board.add_task(
                TaskItem(
                    id=f"TASK-{idx:03d}",
                    title=clean_title,
                    status=status,
                    priority=priority,
                    tags=tags,
                )
            )
        return board

    def completion_rate(self) -> float:
        if not self.tasks:
            return 0.0
        done_count = sum(1 for t in self.tasks if t.is_done())
        return (done_count / len(self.tasks)) * 100.0

    def get_by_status(self, status: str) -> List[TaskItem]:
        return [t for t in self.tasks if t.status == status]

    def render_markdown(self) -> str:
        lines = [f"# {self.title}", "", f"**Completion**: {self.completion_rate():.1f}% ({sum(1 for t in self.tasks if t.is_done())}/{len(self.tasks)})", ""]
        for status in ["TODO", "IN_PROGRESS", "DONE"]:
            tasks = self.get_by_status(status)
            lines.append(f"## {status} ({len(tasks)})")
            if not tasks:
                lines.append("_None_")
            else:
                for t in tasks:
                    tag_str = " ".join(f"`#{tag}`" for tag in t.tags)
                    prio_str = f"[{t.priority}]" if t.priority != "NORMAL" else ""
                    parts = [f"- {t.id}: {t.title}"]
                    if prio_str:
                        parts.append(prio_str)
                    if tag_str:
                        parts.append(tag_str)
                    lines.append(" ".join(parts))
            lines.append("")
        return "\n".join(lines).strip()

    def render_ascii(self) -> str:
        columns = ["TODO", "IN_PROGRESS", "DONE"]
        col_tasks = {col: self.get_by_status(col) for col in columns}
        max_rows = max(len(tasks) for tasks in col_tasks.values()) if col_tasks else 0
        
        col_width = 28
        sep = "+" + "+".join(["-" * col_width for _ in columns]) + "+"
        header = "|" + "|".join([f" {col.center(col_width - 2)} " for col in columns]) + "|"

        lines = [
            f"=== {self.title} [Progress: {self.completion_rate():.1f}%] ===",
            sep,
            header,
            sep,
        ]

        if max_rows == 0:
            lines.append("|" + "|".join([" " * col_width for _ in columns]) + "|")
        else:
            for r in range(max_rows):
                row_cells = []
                for col in columns:
                    if r < len(col_tasks[col]):
                        t = col_tasks[col][r]
                        text = f"{t.id}: {t.title}"[:col_width - 2]
                        row_cells.append(f" {text.ljust(col_width - 2)} ")
                    else:
                        row_cells.append(" " * col_width)
                lines.append("|" + "|".join(row_cells) + "|")

        lines.append(sep)
        return "\n".join(lines)
