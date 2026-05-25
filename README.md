# Braille Translator

영어/한글과 점자를 서로 변환하는 Python CLI 프로젝트입니다. 영어 알파벳, 대문자, 공백과 한글 초성/중성/종성 점자 변환을 지원합니다.

## 실행

```bash
uv run main.py
```

## 파일 구조

- `model.py`: 3x2 점자 셀 타입
- `error.py`: 변환 오류 모델
- `parser.py`: CLI에서 입력한 점자 배열 파싱
- `rules/english.py`: 영어 점자 규칙 데이터
- `rules/korean.py`: 한글 점자 규칙 데이터
- `translators/english.py`: 영어 -> 점자, 점자 -> 영어 변환 함수
- `translators/korean.py`: 한글 -> 점자, 점자 -> 한글 변환 함수
- `visualizer.py`: 점자 셀 배열을 보기 좋은 2x3 형태로 출력
- `main.py`: 메뉴형 CLI 실행 파일
