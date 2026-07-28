"""퀴즈 게임 전체 흐름을 관리하는 QuizGame 클래스."""

import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz


class QuizGame:
    """메뉴, 퀴즈 목록, 점수를 관리한다."""

    def __init__(self, state_path: str | Path | None = None):
        project_root = Path(__file__).resolve().parent
        self.state_path = Path(state_path) if state_path else project_root / "state.json"
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None
        self.load_state()

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        """범위 안의 정수를 입력할 때까지 다시 묻는다."""
        while True:
            raw_value = input(prompt).strip()

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
    def read_text(prompt: str) -> str:
        """빈 문자열이 아닌 값을 입력할 때까지 다시 묻는다."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 내용은 입력할 수 없습니다. 내용을 입력해 주세요.")

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
                    self.list_quizzes()
                elif menu_number == 4:
                    self.show_best_score()
                else:
                    self.save_state()
                    print("\n게임을 종료합니다. 다음에 또 만나요!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
            self.save_state()

    def play_quiz(self) -> None:
        """저장된 퀴즈를 모두 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("\n현재 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            print("-" * 40)
            quiz.display(number)
            user_answer = self.read_number("\n정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번, '{correct_choice}'입니다.")

        score = round(correct_count / total * 100)
        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

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
        self.quizzes.append(Quiz(question, choices, answer))

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

    def show_best_score(self) -> None:
        """현재까지의 최고 점수를 출력한다."""
        if self.best_score is None:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
            return

        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )

    def reset_state(self) -> None:
        """퀴즈와 점수를 기본 상태로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

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

            loaded_quizzes = [Quiz.from_dict(item) for item in quiz_data]
            best_score = state.get("best_score")
            best_correct = state.get("best_correct")
            best_total = state.get("best_total")
            self.validate_score_data(best_score, best_correct, best_total)

            self.quizzes = loaded_quizzes
            self.best_score = best_score
            self.best_correct = best_correct
            self.best_total = best_total

            score_message = (
                "기록 없음" if self.best_score is None else f"최고 {self.best_score}점"
            )
            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, {score_message})"
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

    def save_state(self) -> bool:
        """현재 퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
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
