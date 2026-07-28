"""퀴즈 게임 전체 흐름을 관리하는 QuizGame 클래스."""

from pathlib import Path

from default_quizzes import create_default_quizzes


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
        print("\n퀴즈 풀기 기능을 준비 중입니다.")

    def add_quiz(self) -> None:
        print("\n퀴즈 추가 기능을 준비 중입니다.")

    def list_quizzes(self) -> None:
        print("\n퀴즈 목록 기능을 준비 중입니다.")

    def show_best_score(self) -> None:
        print("\n점수 확인 기능을 준비 중입니다.")

