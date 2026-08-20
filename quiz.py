"""개별 퀴즈를 표현하는 Quiz 클래스."""


class Quiz:
    """문제, 선택지, 정답을 하나로 묶어 관리한다."""

    CHOICE_COUNT = 4

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str | None = None,
    ):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")

        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError("선택지는 정확히 4개여야 합니다.")

        cleaned_choices = []
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("각 선택지는 비어 있지 않은 문자열이어야 합니다.")
            cleaned_choices.append(choice.strip())

        if (
            not isinstance(answer, int)
            or isinstance(answer, bool)
            or not 1 <= answer <= self.CHOICE_COUNT
        ):
            raise ValueError("정답은 1부터 4 사이의 정수여야 합니다.")

        if hint is not None and not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다.")

        cleaned_hint = hint.strip() if hint else ""
        if not cleaned_hint:
            answer_choice = cleaned_choices[answer - 1]
            cleaned_hint = f"정답은 '{answer_choice[0]}'(으)로 시작합니다."

        self.question = question.strip()
        self.choices = cleaned_choices
        self.answer = answer
        self.hint = cleaned_hint

    def display(self, number: int | None = None) -> None:
        """터미널에 문제와 네 개의 선택지를 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자의 답이 정답인지 반환한다."""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """JSON에 저장할 수 있는 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리에서 Quiz 객체를 생성한다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 딕셔너리여야 합니다.")

        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer"),
            hint=data.get("hint"),
        )
