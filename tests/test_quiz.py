"""Quiz 클래스 단위 테스트."""

import unittest

from quiz import Quiz


class QuizTest(unittest.TestCase):
    def test_correct_answer_and_json_conversion(self):
        quiz = Quiz("2 + 2는?", ["2", "3", "4", "5"], 3, "두 수를 더하세요.")

        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        restored_quiz = Quiz.from_dict(quiz.to_dict())
        self.assertEqual(restored_quiz.answer, 3)
        self.assertEqual(restored_quiz.hint, "두 수를 더하세요.")

    def test_old_quiz_without_hint_gets_automatic_hint(self):
        quiz = Quiz.from_dict(
            {
                "question": "정답은 무엇일까요?",
                "choices": ["alpha", "beta", "gamma", "delta"],
                "answer": 2,
            }
        )

        self.assertEqual(quiz.hint, "정답은 'b'(으)로 시작합니다.")

    def test_quiz_requires_four_choices(self):
        with self.assertRaises(ValueError):
            Quiz("잘못된 문제", ["하나", "둘"], 1)

    def test_answer_must_be_between_one_and_four(self):
        with self.assertRaises(ValueError):
            Quiz("잘못된 정답", ["하나", "둘", "셋", "넷"], 5)

    def test_hint_must_be_text(self):
        with self.assertRaises(ValueError):
            Quiz("잘못된 힌트", ["하나", "둘", "셋", "넷"], 1, 123)


if __name__ == "__main__":
    unittest.main()
