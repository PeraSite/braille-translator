# Braille Translator

컴퓨팅사고와 활용 6팀 `닷츠`의 점자/한국어 양방향 점역/역점역 프로그램입니다.
영어/한글과 점자를 서로 변환하는 Python GUI 프로젝트이며, 영어 알파벳, 대문자, 공백과 한글 초성/중성/종성 점자 변환을 지원합니다.

## 팀 정보

- 팀명: 닷츠
- 프로젝트 주제: 점자/한국어 양방향 점역/역점역 프로그램

## 조원 및 역할

| 이름 | 학번 | 담당 역할 |
| --- | --- | --- |
| 정제훈 | 20251650 | 팀장, 점자<->영어 구현, PPT/발표 |
| 장백준 | 20261723 | 점자<->한국어 구현 |
| 김민경 | 20261672 | 점자 입력, 결과 출력 UI 제작 |
| 김빛나 | 20261675 | 한국어<->점자 구현 |

## 주요 기능

- 한국어 또는 영어 문장을 점자로 변환
- 점자 배열을 한국어 또는 영어 문자열로 변환
- 3x2 점자 셀 배열 파싱 및 시각화
- 변환 중 지원하지 않는 입력에 대한 오류 메시지 제공

## 실행

```bash
uv run main.py
```

## Windows에서 처음 실행하는 방법

Python이나 uv가 설치되어 있지 않은 Windows 사용자는 아래 순서대로 실행합니다.

1. PowerShell을 엽니다.
2. uv를 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. PowerShell을 닫았다가 다시 엽니다.
4. uv 설치가 되었는지 확인합니다.

```powershell
uv --version
```

5. 프로젝트 폴더로 이동합니다.

```powershell
cd "프로젝트 폴더 경로"
```

예시:

```powershell
cd "C:\Users\사용자이름\Downloads\braille-translator"
```

6. 프로그램을 실행합니다.

```powershell
uv run main.py
```

처음 실행할 때는 uv가 필요한 Python과 패키지를 자동으로 준비하므로 시간이 조금 걸릴 수 있습니다.

## 사용 방법

실행 후 GUI에서 언어와 번역 방향을 선택합니다.

- `점역`: 한국어 또는 영어 문장을 입력하면 점자 보기와 점자 배열을 출력합니다.
- `역점역`: 3x2 점자 버튼으로 점자를 추가한 뒤 한국어 또는 영어로 변환합니다.

## 파일 구조

- `model.py`: 3x2 점자 셀 타입
- `error.py`: 변환 오류 모델
- `parser.py`: CLI에서 입력한 점자 배열 파싱
- `rules/english.py`: 영어 점자 규칙 데이터
- `rules/korean.py`: 한글 점자 규칙 데이터
- `translators/english.py`: 영어 -> 점자, 점자 -> 영어 변환 함수
- `translators/korean.py`: 한글 -> 점자, 점자 -> 한글 변환 함수
- `visualizer.py`: 점자 셀 배열을 보기 좋은 2x3 형태로 출력
- `ui.py`: Tkinter GUI 화면과 번역 기능 연결
- `main.py`: GUI 실행 파일
