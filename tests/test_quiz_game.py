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

            self.assertEqual(len(game.quizzes), 7)
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

    def test_noninteractive_eof_run_saves_and_exits(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            output = io.StringIO()

            with patch.object(game, "show_menu"):
                with patch.object(game, "read_number", side_effect=EOFError):
                    with redirect_stdout(output):
                        game.run()

            self.assertIn("입력 스트림이 종료되었습니다", output.getvalue())
            self.assertTrue((Path(directory) / "state.json").exists())

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

    def test_ctrl_c_during_add_does_not_save_partial_quiz(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)

            with patch(
                "builtins.input",
                side_effect=["2", "작성 중인 문제", KeyboardInterrupt],
            ):
                with redirect_stdout(io.StringIO()):
                    game.run()

            loaded_game = self.create_game(directory)
            self.assertEqual(len(loaded_game.quizzes), 7)
            self.assertNotIn(
                "작성 중인 문제",
                [quiz.question for quiz in loaded_game.quizzes],
            )

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

    def test_added_quiz_connects_to_play_history_and_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            added_question = "추가 문제도 모든 기능에 연결될까요?"
            add_inputs = [
                added_question,
                "아니요 1",
                "아니요 2",
                "네",
                "아니요 4",
                "3",
                "추가 문제 전용 힌트",
            ]

            with patch("builtins.input", side_effect=add_inputs):
                with redirect_stdout(io.StringIO()):
                    game.add_quiz()

            reloaded_game = self.create_game(directory)
            self.assertEqual(len(reloaded_game.quizzes), 8)
            added_quiz = reloaded_game.quizzes[-1]

            with patch("quiz_game.random.sample", return_value=[added_quiz]) as sample:
                with patch("builtins.input", side_effect=["1", "h", "3"]):
                    with redirect_stdout(io.StringIO()):
                        reloaded_game.play_quiz()

            sample.assert_called_once_with(reloaded_game.quizzes, k=1)
            played_game = self.create_game(directory)
            self.assertEqual(played_game.score_history[-1]["hints_used"], 1)
            self.assertEqual(played_game.score_history[-1]["score"], 95)
            self.assertEqual(played_game.best_score, 95)

            with patch("builtins.input", side_effect=["y", "8", "y"]):
                with redirect_stdout(io.StringIO()):
                    played_game.manage_quizzes()

            final_game = self.create_game(directory)
            self.assertEqual(len(final_game.quizzes), 7)
            self.assertNotIn(
                added_question,
                [quiz.question for quiz in final_game.quizzes],
            )
            self.assertEqual(len(final_game.score_history), 1)
            self.assertEqual(final_game.best_score, 95)

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

    def test_lower_score_keeps_best_and_appends_history(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.quizzes = [Quiz("정답은 2번", ["1", "2", "3", "4"], 2)]

            with patch("builtins.input", side_effect=["1", "2", "1", "1"]):
                with redirect_stdout(io.StringIO()):
                    game.play_quiz()
                    game.play_quiz()

            loaded_game = self.create_game(directory)
            self.assertEqual(loaded_game.best_score, 100)
            self.assertEqual(len(loaded_game.score_history), 2)
            self.assertEqual(
                [record["score"] for record in loaded_game.score_history],
                [100, 0],
            )

    def test_equal_score_prefers_record_with_more_questions(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.best_score = 100
            game.best_correct = 1
            game.best_total = 1

            self.assertTrue(game.is_new_best(100, 8, 8))
            self.assertFalse(game.is_new_best(100, 1, 1))
            self.assertFalse(game.is_new_best(95, 8, 8))

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

    def test_empty_quiz_list_is_handled_without_input(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            game.quizzes = []
            game.save_state()
            output = io.StringIO()

            with redirect_stdout(output):
                game.play_quiz()
                game.manage_quizzes()
                game.delete_quiz()

            self.assertIn("등록된 퀴즈가 없습니다", output.getvalue())
            self.assertIn("삭제할 퀴즈가 없습니다", output.getvalue())
            self.assertEqual(self.create_game(directory).quizzes, [])

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

    def test_invalid_json_schema_recovers_with_default_quizzes(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            state_path.write_text(
                json.dumps({"quizzes": "리스트가 아님"}, ensure_ascii=False),
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                game = QuizGame(state_path)

            self.assertEqual(len(game.quizzes), 7)
            self.assertIn("기본 퀴즈 데이터로 복구합니다", output.getvalue())

    def test_save_error_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            game = self.create_game(directory)
            output = io.StringIO()

            with patch.object(Path, "open", side_effect=OSError("쓰기 실패")):
                with redirect_stdout(output):
                    result = game.save_state()

            self.assertFalse(result)
            self.assertIn("데이터를 저장하지 못했습니다", output.getvalue())


if __name__ == "__main__":
    unittest.main()
