# Python 기초 퀴즈 게임

터미널에서 퀴즈를 풀고, 새 문제를 등록하고, 최고 점수를 저장할 수 있는
콘솔 프로그램입니다. 외부 라이브러리 없이 Python 표준 라이브러리만 사용했습니다.

## 프로젝트 개요

Python의 입력·출력, 조건문, 반복문, 함수, 클래스, 예외 처리, JSON 파일
입출력을 하나의 동작하는 프로그램에서 연습하기 위한 프로젝트입니다.
`Quiz`와 `QuizGame` 두 클래스로 문제 한 개와 게임 전체의 역할을 나눴습니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초 문법**입니다. 프로그램을 만들면서 사용한 `list`,
`dict`, `if`, `for`, 함수 같은 개념을 퀴즈로 다시 확인하면 구현과 복습을
한 번에 할 수 있기 때문에 이 주제를 선택했습니다. 기본 퀴즈는 7개입니다.

## 실행 환경

- Python 3.10 이상
- 별도 패키지 설치 없음

## 실행 방법

```bash
git clone https://github.com/xliiadastra/codyssey-python-quiz-game.git
cd codyssey-python-quiz-game
python3 main.py
```

Windows에서 `python3` 명령을 찾지 못하면 `python main.py`를 사용합니다.

## 기능 목록

1. 퀴즈 풀기
   - 저장된 모든 문제를 순서대로 출제
   - 답 입력 후 정답·오답과 정답 내용 표시
   - 정답 수와 100점 기준 점수 계산
2. 퀴즈 추가
   - 문제, 선택지 4개, 정답 번호 입력
   - 추가 직후 `state.json`에 저장
3. 퀴즈 목록
   - 등록된 전체 문제의 번호와 질문 표시
4. 점수 확인
   - 최고 점수와 당시 정답 수 표시
   - 퀴즈를 풀지 않은 상태도 별도로 안내
5. 안전한 입력과 종료
   - 빈 입력, 문자 입력, 범위 밖 숫자를 안내한 뒤 재입력
   - `Ctrl+C`와 입력 스트림 종료 시 가능한 데이터를 저장하고 종료
   - 저장 파일이 없거나 손상되어도 기본 퀴즈로 실행

## 파일 구조

```text
.
├── main.py                    # 프로그램 시작점
├── quiz.py                    # Quiz 클래스
├── quiz_game.py               # QuizGame 클래스와 게임 전체 흐름
├── default_quizzes.py         # Python 기초 기본 퀴즈 7개
├── state.json                 # 퀴즈와 최고 점수 저장 파일
├── tests/
│   ├── test_quiz.py           # Quiz 단위 테스트
│   └── test_quiz_game.py      # 입력·저장·복구 테스트
├── docs/
│   ├── GIT_PRACTICE.md        # 브랜치·clone·pull 실습 기록
│   └── screenshots/           # 제출용 실행 화면 이미지
├── LEARNING_GUIDE.md          # 빠른 복습과 발표용 설명
├── .gitignore
└── README.md
```

## 데이터 파일 설명

프로젝트 루트의 `state.json`에 UTF-8 형식으로 저장합니다.

```json
{
    "quizzes": [
        {
            "question": "Python을 만든 사람은 누구일까요?",
            "choices": ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "데니스 리치"],
            "answer": 1
        }
    ],
    "best_score": null,
    "best_correct": null,
    "best_total": null
}
```

- `quizzes`: 퀴즈 객체를 변환한 딕셔너리 목록
- `best_score`: 100점 기준 최고 점수
- `best_correct`: 최고 기록에서 맞힌 문제 수
- `best_total`: 최고 기록에서 출제된 전체 문제 수
- 아직 게임 기록이 없으면 점수 관련 값은 JSON의 `null`입니다.

파일이 없으면 기본 퀴즈를 사용해 새로 생성합니다. JSON 형식이나 내부 값이
잘못되면 오류를 처리하고 기본 데이터로 복구합니다.

## 테스트 실행

```bash
python3 -m unittest discover -s tests -v
```

숫자 입력 재시도, 퀴즈 검증, 추가 데이터 재로딩, 최고 점수 저장, 손상된
JSON 복구를 외부 라이브러리 없이 검사합니다.

## 제출용 스크린샷

다음 파일명으로 직접 실행 화면을 캡처해 `docs/screenshots`에 넣을 수 있습니다.

- `environment.png`: Python 버전, Git 설정 또는 VS Code 화면
- `menu.png`: 메인 메뉴
- `add_quiz.png`: 퀴즈 추가 결과
- `list.png`: 퀴즈 목록
- `play.png`: 퀴즈 풀이와 최종 결과
- `score.png`: 최고 점수 확인
- `git-log.png`: `git log --oneline --graph --all` 결과

## 저장소 복제 실습

별도 로컬 폴더에서 저장소를 clone한 뒤 이 문장을 추가하고 push했습니다.
