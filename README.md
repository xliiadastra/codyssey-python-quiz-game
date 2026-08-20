# Python 기초 퀴즈 게임

터미널에서 퀴즈를 풀고, 새 문제를 등록·삭제하고, 최고 점수와 전체 게임
기록을 저장할 수 있는 콘솔 프로그램입니다. 외부 라이브러리 없이 Python
표준 라이브러리만 사용했습니다.

## 프로젝트 개요

Python의 입력·출력, 조건문, 반복문, 함수, 클래스, 예외 처리, JSON 파일
입출력을 하나의 동작하는 프로그램에서 연습하기 위한 프로젝트입니다.
`Quiz`와 `QuizGame` 두 클래스로 문제 한 개와 게임 전체의 역할을 나눴습니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초 문법**입니다. 프로그램을 만들면서 사용한 `list`,
`dict`, `if`, `for`, 함수 같은 개념을 퀴즈로 다시 확인하면 구현과 복습을
한 번에 할 수 있기 때문에 이 주제를 선택했습니다. 기본 퀴즈는 7개입니다.

`default_quizzes.py`에는 기본 문제 7개가 있으며, 현재 `state.json`에는 실행
실습에서 사용자가 추가한 문제 1개까지 영속화되어 총 8개가 저장되어 있습니다.
저장 파일을 삭제한 첫 실행이나 손상 복구 시에는 다시 기본 7개로 시작합니다.

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
   - 풀 문제 수를 직접 선택
   - 저장된 문제 중 선택한 수만큼 중복 없이 무작위 출제
   - `H`를 입력하면 문제당 한 번 힌트 표시
   - 힌트 한 번당 최종 점수에서 5점 차감
   - 답 입력 후 정답·오답과 정답 내용 표시
   - 정답 수와 100점 기준 점수 계산
2. 퀴즈 추가
   - 문제, 선택지 4개, 정답 번호, 힌트 입력
   - 추가 직후 `state.json`에 저장
3. 퀴즈 목록과 삭제
   - 등록된 전체 문제의 번호와 질문 표시
   - 목록 확인 후 선택한 퀴즈를 확인 절차를 거쳐 삭제
4. 점수 확인
   - 최고 점수와 당시 정답 수 표시
   - 점수가 같으면 더 많은 문제를 맞힌 기록을 최고 기록으로 우선
   - 날짜·문제 수·정답 수·힌트 수·최종 점수의 전체 기록 표시
   - 퀴즈를 풀지 않은 상태도 별도로 안내
5. 안전한 입력과 종료
   - 빈 입력, 문자 입력, 범위 밖 숫자를 안내한 뒤 재입력
   - 한글을 입력했다 지워도 글자 단위로 올바르게 편집
   - `Ctrl+C` 입력 시 가능한 데이터를 저장하고 정상 종료
   - 터미널의 `Ctrl+D`는 종료하지 않고 현재 입력을 다시 요청
   - 파이프·파일 입력 자체가 끝난 경우에는 저장 후 정상 종료
   - 저장 파일이 없거나 손상되어도 기본 퀴즈로 실행

## 보너스 기능 구현

- [x] 랜덤 출제
- [x] 문제 수 선택
- [x] 힌트와 점수 차감
- [x] 퀴즈 삭제 및 파일 반영
- [x] 날짜·시간을 포함한 전체 점수 기록

## 파일 구조

```text
.
├── main.py                    # 프로그램 시작점
├── quiz.py                    # Quiz 클래스
├── quiz_game.py               # QuizGame 클래스와 게임 전체 흐름
├── default_quizzes.py         # Python 기초 기본 퀴즈 7개
├── state.json                 # 퀴즈, 점수, 전체 게임 기록 저장 파일
├── tests/
│   ├── test_quiz.py           # Quiz 단위 테스트
│   └── test_quiz_game.py      # 입력·저장·복구 테스트
├── docs/
│   ├── GIT_PRACTICE.md        # 브랜치·clone·pull 실습 기록
│   ├── CODE_EXPLANATION_SCENARIO.md # 코드 설명 발표 대본과 예상 질문
│   ├── SCREENSHOT_GUIDE.md     # 제출 화면 6장 촬영 순서
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
            "answer": 1,
            "hint": "네덜란드 출신이며 이름은 '귀도'로 시작합니다."
        }
    ],
    "best_score": 95,
    "best_correct": 1,
    "best_total": 1,
    "score_history": [
        {
            "played_at": "2026-08-20T12:00:00+09:00",
            "total": 1,
            "correct": 1,
            "hints_used": 1,
            "raw_score": 100,
            "hint_penalty": 5,
            "score": 95
        }
    ]
}
```

- `quizzes`: 퀴즈 객체를 변환한 딕셔너리 목록
- `hint`: 해당 문제의 힌트
- `best_score`: 100점 기준 최고 점수
- `best_correct`: 최고 기록에서 맞힌 문제 수
- `best_total`: 최고 기록에서 출제된 전체 문제 수
- `score_history`: 날짜·문제 수·정답 수·힌트·감점을 포함한 모든 게임 기록
- 아직 게임 기록이 없으면 최고 점수 관련 값은 `null`, 전체 기록은 빈
  리스트 `[]`입니다.

파일이 없으면 기본 퀴즈를 사용해 새로 생성합니다. JSON 형식이나 내부 값이
잘못되면 오류를 처리하고 기본 데이터로 복구합니다. 보너스 구현 전의 JSON은
힌트와 점수 기록을 자동으로 추가해 현재 스키마로 읽습니다.

## 테스트 실행

```bash
python3 -m unittest discover -s tests -v
```

숫자 입력 재시도, 퀴즈 검증, 랜덤 출제, 문제 수 선택, 힌트 감점, 퀴즈 삭제,
전체 점수 기록, 이전 JSON 마이그레이션, 손상된 JSON 복구, `Ctrl+C` 안전
종료, 대화형 `Ctrl+D` 차단을 외부 라이브러리 없이 검사합니다.

## 제출용 스크린샷

제출용 화면 6장과 별도 메뉴 화면 1장을 `docs/screenshots`에 정리했습니다.
자세한 촬영 순서는 `docs/SCREENSHOT_GUIDE.md`에서 확인할 수 있습니다.
스크린샷은 필수 기능 완성 시점의 실행 증빙이며, 이후 추가된 보너스 기능은
코드·JSON·자동 테스트와 Git 커밋으로 별도 확인할 수 있습니다.

- [메인 메뉴](docs/screenshots/menu.png)
- [퀴즈 추가 결과](docs/screenshots/add_quiz.png)
- [퀴즈 8개 목록](docs/screenshots/list.png)
- [8문제 만점 풀이 결과](docs/screenshots/play.png)
- [재실행 후 최고 점수](docs/screenshots/score.png)
- [Python 및 Git 개발 환경](docs/screenshots/environment.png)
- [Git 브랜치와 커밋 그래프](docs/screenshots/git-log.png)

## 저장소 복제 실습

별도 로컬 폴더에서 저장소를 clone한 뒤 이 문장을 추가하고 push했습니다.
