"""QuizGame의 입력 검증과 파일 저장 테스트."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from quiz import Quiz
from quiz_game import QuizGame


class QuizGameTest(unittest.TestCase):
    def create_game(self, directory: str) -> QuizGame:
        state_path = Path(directory) / "state.json"
        with redirect_stdout(io.StringIO()):
            return QuizGame(state_path)

    def test_missing_file_creates_default_state(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            game = self.create_game(directory)

            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertTrue(state_path.exists())
            self.assertIsNone(game.best_score)
            self.assertEqual(game.score_history, [])
            self.assertTrue(all(quiz.hint for quiz in game.quizzes))

    def test_number_input_retries_until_valid(self):
        fake_inputs = ["", "abc", "9", " 3 "]
        output = io.StringIO()

        with patch("builtins.input", side_effect=fake_inputs):
            with redirect_stdout(output):
                result = QuizGame.read_number("선택: ", 1, 5)

        self.assertEqual(result, 3)
        self.assertIn("빈 입력", output.getvalue())
        self.assertIn("잘못된 입력", output.getvalue())
        self.assertIn("범위를 벗어났습니다", output.getvalue())

    def test_interactive_ctrl_d_is_blocked_and_reprompts(self):
        output = io.StringIO()
        terminal_input = Mock()
        terminal_input.isatty.return_value = True

        with patch("builtins.input", side_effect=[EOFError, " 4 "]):
            with patch("quiz_game.sys.stdin", terminal_input):
                with redirect_stdout(output):
                    result = QuizGame.read_number("선택: ", 1, 5)

        self.assertEqual(result, 4)
        self.assertIn("Ctrl+D로는 종료할 수 없습니다", output.getvalue())

    def test_noninteractive_eof_is_not_retried_forever(self):
        piped_input = Mock()
        piped_input.isatty.return_value = False

        with patch("builtins.input", side_effect=EOFError):
            with patch("quiz_game.sys.stdin", piped_input):
                with self.assertRaises(EOFError):
                    QuizGame.read_input("선택: ")

    def test_ctrl_c_saves_and_exits_normally(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            output = io.StringIO()

            with patch.object(game, "show_menu"):
                with patch.object(game, "read_number", side_effect=KeyboardInterrupt):
                    with redirect_stdout(output):
                        game.run()

            self.assertIn("정상 종료합니다", output.getvalue())
            self.assertTrue((Path(directory) / "state.json").exists())

    def test_added_quiz_is_loaded_again(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            inputs = [
                "새 문제",
                "보기 1",
                "보기 2",
                "보기 3",
                "보기 4",
                "2",
                "새 힌트",
            ]

            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(io.StringIO()):
                    game.add_quiz()

            loaded_game = self.create_game(directory)
            self.assertEqual(loaded_game.quizzes[-1].question, "새 문제")
            self.assertEqual(loaded_game.quizzes[-1].answer, 2)
            self.assertEqual(loaded_game.quizzes[-1].hint, "새 힌트")

    def test_play_updates_and_saves_best_score(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.quizzes = [Quiz("정답은 2번", ["1", "2", "3", "4"], 2)]

            with patch("builtins.input", side_effect=["1", "2"]):
                with redirect_stdout(io.StringIO()):
                    game.play_quiz()

            loaded_game = self.create_game(directory)
            self.assertEqual(loaded_game.best_score, 100)
            self.assertEqual(loaded_game.best_correct, 1)
            self.assertEqual(loaded_game.best_total, 1)
            self.assertEqual(len(loaded_game.score_history), 1)
            self.assertEqual(loaded_game.score_history[0]["score"], 100)

    def test_play_uses_random_order_and_selected_question_count(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.quizzes = [
                Quiz("첫 번째", ["A", "B", "C", "D"], 1),
                Quiz("두 번째", ["A", "B", "C", "D"], 2),
                Quiz("세 번째", ["A", "B", "C", "D"], 3),
            ]
            selected = [game.quizzes[2], game.quizzes[0]]

            with patch("quiz_game.random.sample", return_value=selected) as sample:
                with patch("builtins.input", side_effect=["2", "3", "1"]):
                    with redirect_stdout(io.StringIO()):
                        game.play_quiz()

            sample.assert_called_once_with(game.quizzes, k=2)
            self.assertEqual(game.score_history[-1]["total"], 2)
            self.assertEqual(game.score_history[-1]["correct"], 2)

    def test_hint_is_charged_only_once_per_question(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.quizzes = [
                Quiz("정답은 2번", ["1", "2", "3", "4"], 2, "2를 고르세요.")
            ]
            output = io.StringIO()

            with patch("builtins.input", side_effect=["1", "h", "h", "2"]):
                with redirect_stdout(output):
                    game.play_quiz()

            record = game.score_history[-1]
            self.assertEqual(record["hints_used"], 1)
            self.assertEqual(record["hint_penalty"], 5)
            self.assertEqual(record["score"], 95)
            self.assertEqual(game.best_score, 95)
            self.assertIn("이미 사용했습니다", output.getvalue())

    def test_quiz_deletion_is_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            original_count = len(game.quizzes)

            with patch("builtins.input", side_effect=["y", "1", "y"]):
                with redirect_stdout(io.StringIO()):
                    game.manage_quizzes()

            loaded_game = self.create_game(directory)
            self.assertEqual(len(loaded_game.quizzes), original_count - 1)
            self.assertNotEqual(
                loaded_game.quizzes[0].question,
                "Python을 만든 사람은 누구일까요?",
            )

    def test_legacy_state_migrates_hint_and_score_history(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            legacy_state = {
                "quizzes": [
                    {
                        "question": "Python을 만든 사람은 누구일까요?",
                        "choices": [
                            "귀도 반 로섬",
                            "리누스 토르발스",
                            "제임스 고슬링",
                            "데니스 리치",
                        ],
                        "answer": 1,
                    }
                ],
                "best_score": 100,
                "best_correct": 1,
                "best_total": 1,
            }
            state_path.write_text(
                json.dumps(legacy_state, ensure_ascii=False),
                encoding="utf-8",
            )

            game = self.create_game(directory)

            self.assertEqual(
                game.quizzes[0].hint,
                "네덜란드 출신이며 이름은 '귀도'로 시작합니다.",
            )
            self.assertEqual(len(game.score_history), 1)
            self.assertEqual(game.score_history[0]["score"], 100)

    def test_score_screen_shows_all_history(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.score_history = [
                {
                    "played_at": "2026-08-20T12:00:00+09:00",
                    "total": 2,
                    "correct": 1,
                    "hints_used": 1,
                    "raw_score": 50,
                    "hint_penalty": 5,
                    "score": 45,
                }
            ]
            output = io.StringIO()

            with redirect_stdout(output):
                game.show_best_score()

            self.assertIn("2026-08-20T12:00:00+09:00", output.getvalue())
            self.assertIn("힌트 1회", output.getvalue())
            self.assertIn("45점", output.getvalue())

    def test_broken_json_recovers_with_default_quizzes(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            state_path.write_text("{ broken json", encoding="utf-8")
            output = io.StringIO()

            with redirect_stdout(output):
                game = QuizGame(state_path)

            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertIn("기본 퀴즈 데이터로 복구합니다", output.getvalue())

            recovered_state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(len(recovered_state["quizzes"]), len(game.quizzes))


if __name__ == "__main__":
    unittest.main()
