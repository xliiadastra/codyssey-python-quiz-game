"""퀴즈 게임 전체 흐름을 관리하는 QuizGame 클래스."""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz

# import 자체가 input()에 한글을 글자 단위로 지우는 줄 편집 기능을 연결한다.
# Windows처럼 readline이 없는 환경에서도 게임은 기본 입력 방식으로 실행된다.
try:
    import readline as _readline  # noqa: F401
except ImportError:
    _readline = None


class QuizGame:
    """메뉴, 퀴즈 목록, 점수를 관리한다."""

    HINT_PENALTY = 5

    def __init__(self, state_path: str | Path | None = None):
        project_root = Path(__file__).resolve().parent
        self.state_path = Path(state_path) if state_path else project_root / "state.json"
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None
        self.score_history = []
        self.load_state()

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        """범위 안의 정수를 입력할 때까지 다시 묻는다."""
        while True:
            raw_value = QuizGame.read_input(prompt).strip()

            if not raw_value:
                print(f"⚠️ 빈 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            try:
                number = int(raw_value)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            if not minimum <= number <= maximum:
                print(f"⚠️ 범위를 벗어났습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            return number

    @staticmethod
    def read_input(prompt: str) -> str:
        """입력을 받고, 대화형 Ctrl+D는 종료 대신 현재 입력을 다시 묻는다."""
        while True:
            try:
                return input(prompt)
            except EOFError:
                # 실제 터미널의 Ctrl+D만 차단한다. 파이프나 파일 입력의 끝은
                # 상위 run()으로 전달해야 무한 재입력에 빠지지 않는다.
                if not sys.stdin.isatty():
                    raise
                print("\n⚠️ Ctrl+D로는 종료할 수 없습니다. 메뉴에서 5번을 선택하세요.")

    @staticmethod
    def read_text(prompt: str) -> str:
        """빈 문자열이 아닌 값을 입력할 때까지 다시 묻는다."""
        while True:
            value = QuizGame.read_input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 내용은 입력할 수 없습니다. 내용을 입력해 주세요.")

    @staticmethod
    def read_yes_no(prompt: str) -> bool:
        """사용자에게 예 또는 아니요를 입력받는다."""
        while True:
            value = QuizGame.read_input(prompt).strip().lower()
            if value in {"y", "yes", "예", "네"}:
                return True
            if value in {"n", "no", "아니요", "아니오"}:
                return False
            print("⚠️ y 또는 n을 입력해 주세요.")

    @staticmethod
    def read_answer(quiz: Quiz) -> tuple[int, bool]:
        """정답 번호를 받고, H 입력 시 문제당 한 번 힌트를 보여 준다."""
        hint_used = False

        while True:
            raw_value = QuizGame.read_input("\n정답 입력 (1-4, H: 힌트): ").strip()

            if not raw_value:
                print("⚠️ 빈 입력입니다. 1-4 사이의 숫자 또는 H를 입력하세요.")
                continue

            if raw_value.lower() in {"h", "hint", "힌트"}:
                if hint_used:
                    print("💡 이 문제의 힌트는 이미 사용했습니다.")
                else:
                    print(f"💡 힌트: {quiz.hint}")
                    print(
                        f"⚠️ 힌트 사용으로 최종 점수에서 "
                        f"{QuizGame.HINT_PENALTY}점이 차감됩니다."
                    )
                    hint_used = True
                continue

            try:
                answer = int(raw_value)
            except ValueError:
                print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자 또는 H를 입력하세요.")
                continue

            if not 1 <= answer <= Quiz.CHOICE_COUNT:
                print("⚠️ 범위를 벗어났습니다. 1-4 사이의 숫자를 입력하세요.")
                continue

            return answer, hint_used

    @staticmethod
    def show_menu() -> None:
        """메인 메뉴를 출력한다."""
        print()
        print("=" * 40)
        print("        🎯 Python 기초 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self) -> None:
        """메뉴 선택에 따라 해당 기능을 반복 실행한다."""
        print("Python 기초 퀴즈 게임에 오신 것을 환영합니다!")

        try:
            while True:
                self.show_menu()
                menu_number = self.read_number("선택: ", 1, 5)

                if menu_number == 1:
                    self.play_quiz()
                elif menu_number == 2:
                    self.add_quiz()
                elif menu_number == 3:
                    self.manage_quizzes()
                elif menu_number == 4:
                    self.show_best_score()
                else:
                    self.save_state()
                    print("\n게임을 종료합니다. 다음에 또 만나요!")
                    break
        except KeyboardInterrupt:
            print("\n\nCtrl+C가 입력되었습니다. 데이터를 저장하고 정상 종료합니다.")
            self.save_state()
        except EOFError:
            print("\n\n입력 스트림이 종료되었습니다. 데이터를 저장하고 정상 종료합니다.")
            self.save_state()

    def play_quiz(self) -> None:
        """선택한 수만큼 퀴즈를 무작위로 출제하고 결과를 저장한다."""
        if not self.quizzes:
            print("\n현재 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        quiz_count = self.read_number(
            f"\n몇 문제를 풀까요? (1-{len(self.quizzes)}): ",
            1,
            len(self.quizzes),
        )
        selected_quizzes = random.sample(self.quizzes, k=quiz_count)

        total = len(selected_quizzes)
        correct_count = 0
        hint_count = 0
        print(f"\n📝 무작위 순서로 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(selected_quizzes, start=1):
            print()
            print("-" * 40)
            quiz.display(number)
            user_answer, hint_used = self.read_answer(quiz)
            if hint_used:
                hint_count += 1

            if quiz.is_correct(user_answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번, '{correct_choice}'입니다.")

        raw_score = round(correct_count / total * 100)
        hint_penalty = hint_count * self.HINT_PENALTY
        score = max(0, raw_score - hint_penalty)
        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! (기본 {raw_score}점)")
        if hint_count:
            print(f"💡 힌트 {hint_count}회 사용: -{hint_penalty}점")
        print(f"🎯 최종 점수: {score}점")

        self.score_history.append(
            {
                "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "total": total,
                "correct": correct_count,
                "hints_used": hint_count,
                "raw_score": raw_score,
                "hint_penalty": hint_penalty,
                "score": score,
            }
        )

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total
            print("🎉 새로운 최고 점수입니다!")

        self.save_state()
        print("=" * 40)

    def add_quiz(self) -> None:
        """사용자에게 새 퀴즈 정보를 입력받아 목록에 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_text("문제를 입력하세요: ")
        choices = []

        for number in range(1, Quiz.CHOICE_COUNT + 1):
            choice = self.read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.read_number("정답 번호 (1-4): ", 1, Quiz.CHOICE_COUNT)
        hint = self.read_text("힌트를 입력하세요: ")
        self.quizzes.append(Quiz(question, choices, answer, hint))

        if self.save_state():
            print("\n✅ 퀴즈가 추가되고 저장되었습니다!")
        else:
            print("\n⚠️ 퀴즈는 추가되었지만 파일에는 저장하지 못했습니다.")

    def list_quizzes(self) -> None:
        """등록된 퀴즈의 번호와 문제를 출력한다."""
        if not self.quizzes:
            print("\n현재 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def manage_quizzes(self) -> None:
        """퀴즈 목록을 보여 주고 원하는 경우 퀴즈를 삭제한다."""
        self.list_quizzes()
        if not self.quizzes:
            return

        if not self.read_yes_no("퀴즈를 삭제할까요? (y/n): "):
            return

        self.delete_quiz()

    def delete_quiz(self) -> None:
        """선택한 퀴즈를 확인 후 삭제하고 파일에 반영한다."""
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return

        quiz_number = self.read_number(
            f"삭제할 퀴즈 번호 (1-{len(self.quizzes)}): ",
            1,
            len(self.quizzes),
        )
        selected_quiz = self.quizzes[quiz_number - 1]

        if not self.read_yes_no(f"'{selected_quiz.question}' 문제를 삭제할까요? (y/n): "):
            print("삭제를 취소했습니다.")
            return

        del self.quizzes[quiz_number - 1]
        if self.save_state():
            print("✅ 퀴즈를 삭제하고 저장했습니다.")
        else:
            print("⚠️ 퀴즈는 삭제되었지만 파일에는 저장하지 못했습니다.")

    def show_best_score(self) -> None:
        """현재까지의 최고 점수와 모든 게임 기록을 출력한다."""
        if self.best_score is None:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(
                f"\n🏆 최고 점수: {self.best_score}점 "
                f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
            )

        self.show_score_history()

    def show_score_history(self) -> None:
        """날짜, 문제 수, 정답 수, 힌트 수, 점수를 모두 출력한다."""
        if not self.score_history:
            print("📊 저장된 게임 기록이 없습니다.")
            return

        print(f"\n📊 전체 게임 기록 (총 {len(self.score_history)}회)")
        print("-" * 72)
        for number, record in enumerate(self.score_history, start=1):
            print(
                f"[{number}] {record['played_at']} | "
                f"{record['total']}문제 중 {record['correct']}개 정답 | "
                f"힌트 {record['hints_used']}회 | {record['score']}점"
            )
        print("-" * 72)

    def reset_state(self) -> None:
        """퀴즈와 점수를 기본 상태로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None
        self.score_history = []

    def load_state(self) -> None:
        """state.json을 읽고, 문제가 있으면 기본 데이터로 복구한다."""
        if not self.state_path.exists():
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.reset_state()
            self.save_state()
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                state = json.load(file)

            if not isinstance(state, dict):
                raise ValueError("최상위 데이터는 딕셔너리여야 합니다.")

            quiz_data = state.get("quizzes")
            if not isinstance(quiz_data, list):
                raise ValueError("quizzes는 리스트여야 합니다.")

            default_hints = {
                quiz.question: quiz.hint for quiz in create_default_quizzes()
            }
            loaded_quizzes = []
            for item in quiz_data:
                quiz = Quiz.from_dict(item)
                if not item.get("hint") and quiz.question in default_hints:
                    quiz.hint = default_hints[quiz.question]
                loaded_quizzes.append(quiz)
            best_score = state.get("best_score")
            best_correct = state.get("best_correct")
            best_total = state.get("best_total")
            self.validate_score_data(best_score, best_correct, best_total)

            history_data = state.get("score_history")
            if history_data is None:
                score_history = self.create_legacy_score_history(
                    best_score,
                    best_correct,
                    best_total,
                )
            else:
                self.validate_score_history(history_data)
                score_history = history_data

            self.quizzes = loaded_quizzes
            self.best_score = best_score
            self.best_correct = best_correct
            self.best_total = best_total
            self.score_history = score_history

            score_message = (
                "기록 없음" if self.best_score is None else f"최고 {self.best_score}점"
            )
            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, {score_message}, "
                f"게임 기록 {len(self.score_history)}개)"
            )
        except (
            json.JSONDecodeError,
            UnicodeDecodeError,
            OSError,
            TypeError,
            ValueError,
        ) as error:
            print(f"⚠️ 저장 파일을 읽을 수 없습니다: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")
            self.reset_state()
            self.save_state()

    @staticmethod
    def validate_score_data(best_score, best_correct, best_total) -> None:
        """JSON에서 읽은 점수 값의 형태와 범위를 검사한다."""
        values = (best_score, best_correct, best_total)
        if all(value is None for value in values):
            return

        if any(
            not isinstance(value, int) or isinstance(value, bool) for value in values
        ):
            raise ValueError("점수 기록은 모두 정수이거나 모두 null이어야 합니다.")

        if not 0 <= best_score <= 100:
            raise ValueError("최고 점수는 0부터 100 사이여야 합니다.")

        if best_total <= 0 or not 0 <= best_correct <= best_total:
            raise ValueError("정답 수와 전체 문제 수가 올바르지 않습니다.")

    def create_legacy_score_history(
        self,
        best_score,
        best_correct,
        best_total,
    ) -> list[dict]:
        """기존 최고 점수를 첫 번째 히스토리 항목으로 변환한다."""
        if best_score is None:
            return []

        played_at = (
            datetime.fromtimestamp(self.state_path.stat().st_mtime)
            .astimezone()
            .isoformat(timespec="seconds")
        )
        return [
            {
                "played_at": played_at,
                "total": best_total,
                "correct": best_correct,
                "hints_used": 0,
                "raw_score": best_score,
                "hint_penalty": 0,
                "score": best_score,
            }
        ]

    @staticmethod
    def validate_score_history(score_history) -> None:
        """JSON에서 읽은 전체 게임 기록의 형태와 범위를 검사한다."""
        if not isinstance(score_history, list):
            raise ValueError("score_history는 리스트여야 합니다.")

        integer_fields = (
            "total",
            "correct",
            "hints_used",
            "raw_score",
            "hint_penalty",
            "score",
        )
        for record in score_history:
            if not isinstance(record, dict):
                raise ValueError("각 게임 기록은 딕셔너리여야 합니다.")
            if not isinstance(record.get("played_at"), str) or not record["played_at"]:
                raise ValueError("게임 기록의 날짜와 시간이 올바르지 않습니다.")
            try:
                datetime.fromisoformat(record["played_at"])
            except ValueError as error:
                raise ValueError("게임 기록의 날짜와 시간이 올바르지 않습니다.") from error
            if any(
                not isinstance(record.get(field), int)
                or isinstance(record.get(field), bool)
                for field in integer_fields
            ):
                raise ValueError("게임 기록의 숫자 값이 올바르지 않습니다.")

            total = record["total"]
            correct = record["correct"]
            hints_used = record["hints_used"]
            raw_score = record["raw_score"]
            hint_penalty = record["hint_penalty"]
            score = record["score"]

            if total <= 0 or not 0 <= correct <= total:
                raise ValueError("게임 기록의 문제 수와 정답 수가 올바르지 않습니다.")
            if not 0 <= hints_used <= total:
                raise ValueError("게임 기록의 힌트 수가 올바르지 않습니다.")
            if not 0 <= raw_score <= 100 or not 0 <= score <= 100:
                raise ValueError("게임 기록의 점수가 올바르지 않습니다.")
            if raw_score != round(correct / total * 100):
                raise ValueError("게임 기록의 기본 점수가 올바르지 않습니다.")
            if hint_penalty != hints_used * QuizGame.HINT_PENALTY:
                raise ValueError("게임 기록의 힌트 감점이 올바르지 않습니다.")
            if score != max(0, raw_score - hint_penalty):
                raise ValueError("게임 기록의 최종 점수가 올바르지 않습니다.")

    def save_state(self) -> bool:
        """현재 퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "score_history": self.score_history,
        }
        temporary_path = self.state_path.with_name(f"{self.state_path.name}.tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
                file.write("\n")
            temporary_path.replace(self.state_path)
            return True
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")
            return False
