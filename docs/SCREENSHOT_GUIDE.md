# 제출용 스크린샷 가이드

중복을 제외하면 **총 6장**이면 충분합니다. 현재 저장소에는 확인하기 편하도록
별도 메뉴 화면까지 포함해 총 7장을 정리했습니다.

macOS에서는 원하는 화면을 만든 뒤 `Shift + Command + 4`, `Space`, 터미널
창 클릭 순서로 창 전체를 캡처할 수 있습니다.

## 1. 개발 환경

```bash
cd /Users/choeihyeon/dev/codyssey/E1/02
clear
pwd
python3 --version
git --version
git config --get user.name
git config --get user.email
```

파일명 예시: `environment.png`

## 2. 퀴즈 추가

```bash
python3 main.py
```

메뉴에서 `2`를 선택하고 다음 예시를 입력합니다.

```text
문제: Python에서 함수를 정의할 때 사용하는 키워드는?
선택지 1: function
선택지 2: func
선택지 3: def
선택지 4: define
정답 번호: 3
```

`퀴즈가 추가되고 저장되었습니다` 메시지가 보일 때 캡처합니다.

파일명 예시: `add_quiz.png`

## 3. 퀴즈 목록

메뉴에서 `3`을 선택합니다. 방금 추가한 문제까지 총 8개가 표시되는 화면을
캡처합니다.

파일명 예시: `list.png`

## 4. 퀴즈 풀이 결과

메뉴에서 `1`을 선택합니다. 기본 7문제와 위에서 추가한 문제의 정답은 다음
순서입니다.

```text
1, 2, 3, 4, 1, 2, 3, 3
```

마지막에 `8문제 중 8문제 정답! (100점)`과 `새로운 최고 점수입니다`가
보이는 화면을 캡처합니다.

파일명 예시: `play.png`

## 5. 재실행 후 점수 확인

메뉴에서 `5`를 선택해 종료한 뒤 다시 실행합니다.

```bash
python3 main.py
```

저장된 퀴즈 8개와 최고 100점을 불러왔다는 문구를 확인하고 메뉴에서 `4`를
선택합니다. 최고 점수 화면을 캡처하면 재실행 후 데이터 유지도 함께 증명됩니다.

파일명 예시: `score.png`

## 6. Git 브랜치·커밋 기록

게임을 `5`로 종료한 뒤 실행합니다.

```bash
clear
git log --oneline --graph --decorate --all
```

`feature/quiz-play` 브랜치와 병합 선이 보이도록 터미널 창을 충분히 크게 만든
뒤 캡처합니다.

파일명 예시: `git-log.png`

## 캡처 후 선택 사항

퀴즈와 점수를 저장하면서 `state.json`이 변경됩니다. 이 실행 데이터까지
GitHub에 제출하려면 다음처럼 기록할 수 있습니다.

```bash
git add state.json docs/screenshots
git commit -m "Data: 실행 결과와 제출 스크린샷 추가"
git push origin main
```
