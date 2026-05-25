# Braille Translator

영어와 점자를 서로 변환하는 Python CLI 프로젝트입니다. 현재는 영어 알파벳, 대문자, 공백을 지원하고, 한국어 점자는 나중에 확장할 수 있도록 변환 로직을 모듈별로 분리했습니다.

## 실행

```bash
uv run main.py
```

## 파일 구조

- `model.py`: 3x2 점자 셀 데이터와 변환 오류 모델
- `english.py`: 영어 -> 점자, 점자 -> 영어 변환 함수
- `visualizer.py`: 점자 셀 배열을 보기 좋은 2x3 형태로 출력
- `main.py`: 메뉴형 CLI 실행 파일

