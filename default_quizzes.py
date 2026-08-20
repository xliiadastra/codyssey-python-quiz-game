"""첫 실행과 데이터 복구에 사용할 기본 퀴즈."""

from quiz import Quiz


def create_default_quizzes() -> list[Quiz]:
    """Python 기초 주제의 기본 퀴즈를 새 객체 목록으로 반환한다."""
    return [
        Quiz(
            question="Python을 만든 사람은 누구일까요?",
            choices=[
                "귀도 반 로섬",
                "리누스 토르발스",
                "제임스 고슬링",
                "데니스 리치",
            ],
            answer=1,
            hint="네덜란드 출신이며 이름은 '귀도'로 시작합니다.",
        ),
        Quiz(
            question="Python에서 한 줄 주석을 시작할 때 사용하는 기호는?",
            choices=["//", "#", "/*", "--"],
            answer=2,
            hint="해시 기호라고도 부르는 기호입니다.",
        ),
        Quiz(
            question="여러 값을 순서대로 저장하며, 내용을 바꿀 수 있는 자료형은?",
            choices=["int", "bool", "list", "str"],
            answer=3,
            hint="대괄호 []로 만들고 append로 값을 추가할 수 있습니다.",
        ),
        Quiz(
            question="조건이 참일 때만 코드를 실행하려면 주로 어떤 문을 사용할까요?",
            choices=["import", "class", "return", "if"],
            answer=4,
            hint="영어로 '만약'이라는 뜻을 가진 키워드입니다.",
        ),
        Quiz(
            question="리스트의 모든 값을 차례대로 확인할 때 가장 알맞은 반복문은?",
            choices=["for", "if", "try", "def"],
            answer=1,
            hint="모음의 값을 하나씩 차례대로 순회할 때 사용합니다.",
        ),
        Quiz(
            question="딕셔너리(dict)는 데이터를 어떤 형태로 저장할까요?",
            choices=[
                "문자 하나씩",
                "키와 값의 쌍",
                "참 또는 거짓만",
                "숫자만",
            ],
            answer=2,
            hint="사전의 단어와 뜻처럼 두 값을 짝지어 저장합니다.",
        ),
        Quiz(
            question="함수 실행 결과를 호출한 곳으로 돌려주는 키워드는?",
            choices=["break", "continue", "return", "while"],
            answer=3,
            hint="함수를 끝내고 결과를 호출한 곳으로 돌려보냅니다.",
        ),
    ]
