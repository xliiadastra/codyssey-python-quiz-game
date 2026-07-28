"""퀴즈 게임 전체 흐름을 관리하는 QuizGame 클래스."""

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
                    print("\n게임을 종료합니다. 다음에 또 만나요!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n입력이 중단되었습니다. 안전하게 게임을 종료합니다.")

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
        print("\n✅ 퀴즈가 추가되었습니다!")

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
        print("\n점수 확인 기능을 준비 중입니다.")
