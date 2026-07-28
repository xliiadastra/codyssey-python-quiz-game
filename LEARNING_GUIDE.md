# 빠른 학습 가이드

## 1. 이 과제의 진짜 목적

이 과제는 Python 문법을 각각 외우는 것이 아니라 아래 흐름을 혼자 만들고
설명할 수 있는지 확인합니다.

```text
사용자 입력
   ↓
입력 검사
   ↓
조건에 맞는 기능 실행
   ↓
결과 출력
   ↓
JSON 파일에 상태 저장
   ↓
다음 실행에서 다시 불러오기
```

평가 포인트는 크게 네 가지입니다.

1. **동작**: 메뉴, 풀이, 추가, 목록, 점수가 실제로 작동하는가?
2. **구조**: 클래스와 메서드로 역할을 나눴는가?
3. **안정성**: 잘못된 입력과 파일 오류에도 프로그램이 종료되지 않는가?
4. **과정**: Git 커밋, 브랜치, 병합, clone, pull로 개발 과정을 기록했는가?

즉, 정답 코드 한 파일보다 “왜 이렇게 동작하고 어떻게 발전했는지”를
설명하는 능력이 더 중요한 과제입니다.

## 2. 프로그램 구조

```text
main.py
  └─ QuizGame 객체 생성
       ├─ load_state(): state.json 읽기
       ├─ run(): 메뉴 반복
       │    ├─ play_quiz()
       │    ├─ add_quiz()
       │    ├─ list_quizzes()
       │    └─ show_best_score()
       └─ save_state(): state.json 쓰기

QuizGame.quizzes
  └─ Quiz 객체 여러 개
       ├─ question
       ├─ choices
       ├─ answer
       ├─ display()
       └─ is_correct()
```

- `Quiz`는 **문제 한 개**만 책임집니다.
- `QuizGame`은 **게임 전체 흐름과 저장**을 책임집니다.
- 역할을 나누면 한 부분을 고칠 때 다른 부분에 미치는 영향이 줄어듭니다.

추천 코드 읽기 순서는 `main.py → quiz.py → default_quizzes.py →
quiz_game.py → tests`입니다.

## 3. 코드에서 배우는 Python 핵심

### 변수와 자료형

변수는 값을 기억해 두고 이름으로 다시 사용하기 위한 공간입니다.

- `str`: `"Python을 만든 사람은?"`처럼 글자를 저장합니다.
- `int`: 정답 번호 `1`, 점수 `100`처럼 정수를 저장합니다.
- `bool`: `quiz.is_correct(...)`의 결과인 `True` 또는 `False`입니다.
- `list`: `self.quizzes`, `choices`처럼 여러 값을 순서대로 저장합니다.
- `dict`: `{"question": ..., "answer": ...}`처럼 키와 값을 짝지어
  저장하며 JSON 변환에 사용합니다.

### 조건문

`if/elif/else`는 조건에 따라 서로 다른 코드를 실행합니다.

```python
if menu_number == 1:
    self.play_quiz()
elif menu_number == 2:
    self.add_quiz()
else:
    # 다른 선택 처리
```

메뉴 선택, 정답 판정, 최고 점수 갱신, 파일 존재 확인에 사용됩니다.

### 반복문

- `while`: 언제 끝날지 입력에 따라 달라지는 메뉴와 재입력에 적합합니다.
- `for`: 퀴즈 목록처럼 개수가 정해진 모음을 순서대로 확인할 때 적합합니다.

`enumerate(..., start=1)`는 값과 함께 화면에 표시할 1번부터의 번호를
얻습니다.

### 함수와 메서드

함수는 반복되는 동작에 이름을 붙인 코드 묶음입니다.

```python
def read_number(prompt, minimum, maximum):
    ...
    return number
```

- 매개변수: 함수가 동작할 때 필요한 입력값
- 반환값: 함수가 처리 후 호출한 곳에 돌려주는 결과
- 메서드: 클래스 안에 정의되어 객체의 일을 수행하는 함수

`read_number()`를 한 번 만들어 메뉴와 정답 입력에서 함께 사용하므로
검증 규칙이 중복되지 않습니다.

### 클래스와 객체

- 클래스: 객체를 만들기 위한 설계도
- 객체(인스턴스): 설계도로 실제 만든 값
- `__init__`: 객체가 만들어질 때 속성의 초기값을 정하는 메서드
- `self`: 현재 동작 중인 객체 자신
- 속성: `quiz.question`, `game.quizzes`처럼 객체가 가진 데이터
- 메서드: `quiz.is_correct()`, `game.play_quiz()`처럼 객체가 하는 동작

예를 들어 같은 `Quiz` 클래스로 문제 내용이 서로 다른 객체 7개를 만듭니다.

### 파일과 JSON

Python 객체는 프로그램이 끝나면 메모리에서 사라집니다. 다음 실행에서도
데이터를 쓰려면 디스크 파일에 저장해야 합니다.

JSON은 `str`, 숫자, `bool`, `list`, `dict`, `null` 같은 단순한 형태를
사람과 프로그램이 함께 읽기 쉬운 텍스트로 표현합니다. `Quiz` 객체를 바로
저장할 수는 없으므로 `to_dict()`로 딕셔너리로 바꾼 뒤 저장합니다.

```python
with path.open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```

- `with`: 작업 후 파일을 자동으로 닫습니다.
- `encoding="utf-8"`: 한글을 올바르게 저장하고 읽습니다.
- `ensure_ascii=False`: 한글을 그대로 보이게 저장합니다.
- `indent=4`: JSON을 읽기 좋게 들여씁니다.

### 예외 처리

예외는 실행 중 발생하는 오류 상황입니다.

- `ValueError`: `"abc"`를 숫자로 바꾸거나 잘못된 Quiz를 만들 때
- `JSONDecodeError`: JSON 문법이 깨졌을 때
- `OSError`: 파일 읽기·쓰기에 실패했을 때
- `KeyboardInterrupt`: 사용자가 `Ctrl+C`를 눌렀을 때
- `EOFError`: 입력 스트림이 끝났을 때

`try/except`는 오류를 숨기는 문법이 아니라, 예상 가능한 실패에 프로그램이
어떻게 대응할지 정하는 문법입니다.

## 4. 꼭 이해할 구현 포인트

1. `input()`의 결과는 항상 문자열이므로 숫자로 쓰기 전에 `int()`가
   필요합니다.
2. `" 1 "`도 허용하려고 `strip()`으로 앞뒤 공백을 지웁니다.
3. 화면의 답 번호는 1~4지만 리스트 인덱스는 0~3이므로 정답 선택지를
   찾을 때 `quiz.answer - 1`을 사용합니다.
4. 최고 점수 `0`과 아직 기록이 없는 상태는 다르므로 미플레이 상태는
   `None`으로 표현합니다. JSON에서는 `null`이 됩니다.
5. JSON에는 `Quiz` 객체를 직접 저장할 수 없어 `dict`로 변환합니다.
6. `state.json.tmp`에 먼저 쓴 뒤 `state.json`으로 교체해 저장 도중
   중단될 때 원본이 손상될 가능성을 줄였습니다.

## 5. Git 명령을 설명하는 법

| 명령 | 하는 일 |
|---|---|
| `git init` | 현재 폴더를 Git 저장소로 시작 |
| `git add` | 다음 커밋에 담을 변경 선택 |
| `git commit` | 선택한 변경을 하나의 기록으로 저장 |
| `git push` | 로컬 커밋을 GitHub 원격 저장소로 전송 |
| `git pull` | 원격 변경을 가져와 현재 브랜치에 반영 |
| `git checkout` | 다른 브랜치로 이동하거나 새 브랜치 생성 |
| `git clone` | 원격 저장소 전체를 새 로컬 폴더에 복제 |

브랜치는 기존 `main`을 유지하면서 기능을 독립적으로 개발하기 위한 작업
흐름입니다. 이 프로젝트에서는 `feature/quiz-play`에서 퀴즈 풀이를 구현하고
`main`에 병합했습니다.

```bash
git checkout -b feature/quiz-play
# 기능 작성, add, commit
git checkout main
git merge --no-ff feature/quiz-play
```

## 6. 1분 발표 예시

> 이 프로젝트는 Python 기초 주제의 콘솔 퀴즈 게임입니다. `Quiz` 클래스는
> 문제 한 개의 데이터와 정답 확인을 맡고, `QuizGame` 클래스는 메뉴, 풀이,
> 추가, 목록, 점수, 파일 저장을 관리합니다. 메뉴와 재입력에는 종료 시점을
> 사용자가 정하므로 `while`을 썼고, 퀴즈 전체 순회에는 `for`를 썼습니다.
> 입력은 문자열이므로 공백을 제거하고 정수 변환과 범위 검사를 합니다.
> 퀴즈 객체는 딕셔너리로 바꿔 UTF-8 JSON에 저장하며, 파일이 없거나
> 손상되면 예외를 처리해 기본 퀴즈로 복구합니다. Git에서는 기능 단위로
> 커밋하고 풀이 기능을 별도 브랜치에서 만든 뒤 main에 병합했습니다.

## 7. 제출 전에 직접 해 볼 것

코드를 제출하는 것만으로 끝내지 말고 다음을 한 번씩 직접 수행해야 설명이
자연스러워집니다.

1. `python3 main.py`로 실행합니다.
2. 일부러 빈 값, `abc`, `9`를 메뉴에 입력해 봅니다.
3. 본인이 만든 퀴즈 한 개를 추가합니다.
4. 프로그램을 종료하고 다시 실행해 추가 문제가 남아 있는지 확인합니다.
5. 한 번 전부 풀고 재실행한 뒤 최고 점수가 남아 있는지 확인합니다.
6. `state.json`을 열어 객체가 어떤 JSON 데이터로 바뀌었는지 확인합니다.
7. README에 적힌 제출용 화면을 직접 캡처합니다.
8. `git log --oneline --graph --all`에서 기능 브랜치 병합을 확인합니다.

## 8. 스스로 답해 볼 확인 질문

- `Quiz`와 `QuizGame`을 한 클래스로 합치지 않은 이유는?
- `while`과 `for`를 서로 바꾸면 어떤 점이 불편한가?
- `best_score is None`과 `best_score == 0`의 차이는?
- `Quiz.to_dict()`가 없으면 왜 JSON 저장이 어려운가?
- 손상된 `state.json`을 읽을 때 프로그램은 어떤 순서로 복구하는가?
- `git add`와 `git commit`, `git push`의 차이는?

이 여섯 질문에 코드 없이 말로 답할 수 있으면 과제의 핵심을 이해한 것입니다.

