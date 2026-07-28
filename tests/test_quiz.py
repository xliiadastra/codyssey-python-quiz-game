"""Quiz 클래스 단위 테스트."""

import unittest

from quiz import Quiz


class QuizTest(unittest.TestCase):
    def test_correct_answer_and_json_conversion(self):
        quiz = Quiz("2 + 2는?", ["2", "3", "4", "5"], 3)

        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()).answer, 3)

    def test_quiz_requires_four_choices(self):
        with self.assertRaises(ValueError):
            Quiz("잘못된 문제", ["하나", "둘"], 1)

    def test_answer_must_be_between_one_and_four(self):
        with self.assertRaises(ValueError):
            Quiz("잘못된 정답", ["하나", "둘", "셋", "넷"], 5)


if __name__ == "__main__":
    unittest.main()

