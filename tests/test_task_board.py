import unittest
from task_board.core import TaskBoard, TaskItem

SAMPLE_MD = """
# Sprint Backlog
- [ ] Implement user authentication !HIGH #auth #security
- [~] Refactor database connector #database
- [x] Setup CI pipeline !HIGH #devops
- [x] Initial project scaffold #core
"""

class TestTaskBoard(unittest.TestCase):
    def test_markdown_parsing(self):
        board = TaskBoard.from_markdown(SAMPLE_MD, default_title="Sprint 1")
        self.assertEqual(len(board.tasks), 4)

        todo = board.get_by_status("TODO")
        in_progress = board.get_by_status("IN_PROGRESS")
        done = board.get_by_status("DONE")

        self.assertEqual(len(todo), 1)
        self.assertEqual(len(in_progress), 1)
        self.assertEqual(len(done), 2)

        self.assertEqual(todo[0].priority, "HIGH")
        self.assertIn("auth", todo[0].tags)
        self.assertIn("security", todo[0].tags)

    def test_completion_rate(self):
        board = TaskBoard.from_markdown(SAMPLE_MD)
        # 2 out of 4 done -> 50.0%
        self.assertAlmostEqual(board.completion_rate(), 50.0)

    def test_empty_board(self):
        board = TaskBoard.from_markdown("")
        self.assertEqual(len(board.tasks), 0)
        self.assertEqual(board.completion_rate(), 0.0)
        rendered = board.render_ascii()
        self.assertIn("TODO", rendered)

    def test_render_formats(self):
        board = TaskBoard.from_markdown(SAMPLE_MD, default_title="Sprint Board")
        ascii_out = board.render_ascii()
        md_out = board.render_markdown()

        self.assertIn("=== Sprint Board", ascii_out)
        self.assertIn("# Sprint Board", md_out)
        self.assertIn("50.0%", md_out)

if __name__ == "__main__":
    unittest.main()
