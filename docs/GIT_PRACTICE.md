# Git 실습 기록

## 저장소

- GitHub: <https://github.com/xliiadastra/codyssey-python-quiz-game>
- 공개 범위: Public
- 기본 브랜치: `main`

## 기능 브랜치와 병합

퀴즈 풀기 기능은 `feature/quiz-play` 브랜치에서 구현한 뒤 `main`에
`--no-ff` 방식으로 병합했습니다.

```bash
git checkout -b feature/quiz-play
git add quiz_game.py
git commit -m "Feat: 퀴즈 출제와 정답 판정 기능 구현"
git checkout main
git merge --no-ff feature/quiz-play -m "Merge: 퀴즈 풀기 기능 병합"
```

그래프 확인 명령은 다음과 같습니다.

```bash
git log --oneline --graph --decorate --all
```

## clone과 pull

2026년 7월 28일에 다음 순서로 실제 실습했습니다.

1. GitHub 저장소를 별도 임시 로컬 디렉터리에 `clone`
2. 복제본의 README에 “저장소 복제 실습” 문구 추가
3. 복제본에서 commit 후 GitHub에 `push`
4. 원래 프로젝트 디렉터리에서 `pull --ff-only`
5. 원본 README에 문구가 반영된 것을 확인

```bash
git clone git@github.com:xliiadastra/codyssey-python-quiz-game.git <별도-폴더>
cd <별도-폴더>
# README 수정
git add README.md
git commit -m "Docs: 저장소 clone 실습 확인 문구 추가"
git push origin main

cd <원래-프로젝트-폴더>
git pull --ff-only origin main
```

복제본에서 만든 커밋은 다음과 같습니다.

```text
5f56c32 Docs: 저장소 clone 실습 확인 문구 추가
```

## 제출 화면 캡처

아래 두 명령의 결과가 한 화면에 보이도록 터미널 폭을 조절해 캡처합니다.

```bash
git remote -v
git log --oneline --graph --decorate --all
```

`clone`과 `pull`은 커밋 로그 자체에 명령 실행 기록이 남는 기능은 아닙니다.
따라서 이 문서와 복제본에서 만든 커밋을 함께 제시하고, 필요하면 명령 실행
직후의 터미널 화면도 캡처합니다.

