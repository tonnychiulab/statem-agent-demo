import sys
import argparse
from pathlib import Path
from .core import TaskBoard

def main():
    parser = argparse.ArgumentParser(description="Render Markdown tasks into a visual board")
    parser.add_argument("file", help="Path to markdown tasks file")
    parser.add_argument("--format", choices=["ascii", "markdown"], default="ascii", help="Output format")
    parser.add_argument("--title", default="Project Task Board", help="Board title")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    board = TaskBoard.from_markdown(content, default_title=args.title)

    if args.format == "ascii":
        print(board.render_ascii())
    else:
        print(board.render_markdown())

if __name__ == "__main__":
    main()
