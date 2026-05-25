from __future__ import annotations

from jamo import h2j, j2h, jamo_to_hcj

from error import ConversionError
from model import BrailleCell
from rules.korean import (
    BraillePattern,
    겹받침,
    공백_점자,
    된소리_초성,
    읽기_가능한_점자,
    종성_읽기,
    종성_점자,
    중성_읽기,
    중성_점자,
    초성_읽기,
    초성_점자,
)


KoreanBrailleResult = list[BrailleCell] | ConversionError
KoreanTextResult = str | ConversionError


def 한글_자모_분리(한글글자: str) -> tuple[str | None, str | None, str | None]:
    쪼갠_글자 = h2j(한글글자)
    자모_리스트 = list(jamo_to_hcj(쪼갠_글자))

    첫소리 = 자모_리스트[0] if len(자모_리스트) > 0 else None
    가운데소리 = 자모_리스트[1] if len(자모_리스트) > 1 else None
    끝소리 = 자모_리스트[2] if len(자모_리스트) > 2 else None

    return 첫소리, 가운데소리, 끝소리


def 한국어_매칭_점역(전체문장: str) -> list[tuple[str, BraillePattern]]:
    매칭_결과 = []

    for 글자 in 전체문장:
        if 글자 == " ":
            매칭_결과.append(("공백", [공백_점자]))
            continue

        첫소리, 가운데소리, 끝소리 = 한글_자모_분리(글자)

        # 1단계: 초성 매칭
        if 첫소리 and 첫소리 != "ㅇ":
            if 첫소리 in 초성_점자:
                매칭_결과.append((첫소리, 초성_점자[첫소리]))

        # 2단계: 중성 매칭
        if 가운데소리:
            if 가운데소리 in 중성_점자:
                매칭_결과.append((가운데소리, 중성_점자[가운데소리]))

        # 3단계: 종성 매칭
        if 끝소리:
            if 끝소리 in 종성_점자:
                매칭_결과.append((끝소리, 종성_점자[끝소리]))

    return 매칭_결과


def korean_to_braille(text: str) -> KoreanBrailleResult:
    cells: list[BrailleCell] = []

    for position, 글자 in enumerate(text, start=1):
        if 글자 == " ":
            cells.append(공백_점자)
            continue

        첫소리, 가운데소리, 끝소리 = 한글_자모_분리(글자)
        if 가운데소리 is None:
            return ConversionError(position, 글자, "완성형 한글과 공백만 지원합니다.")

        if 첫소리 and 첫소리 != "ㅇ":
            if 첫소리 not in 초성_점자:
                return ConversionError(position, 글자, f"지원하지 않는 초성입니다: {첫소리}")
            cells.extend(초성_점자[첫소리])

        if 가운데소리 not in 중성_점자:
            return ConversionError(position, 글자, f"지원하지 않는 중성입니다: {가운데소리}")
        cells.extend(중성_점자[가운데소리])

        if 끝소리:
            if 끝소리 not in 종성_점자:
                return ConversionError(position, 글자, f"지원하지 않는 종성입니다: {끝소리}")
            cells.extend(종성_점자[끝소리])

    return cells


def _compose(ing: list[str]) -> str | None:
    if len(ing) == 1:
        ing.append("ㅏ")
    if len(ing) in (2, 3):
        return j2h(*ing)
    return None


def trans(cell: BrailleCell, ing: list[str]) -> tuple[list[str], str | None]:
    ret = None

    # 초성부터 판별
    if cell in 초성_읽기:
        초성 = 초성_읽기[cell]
        if len(ing) == 1 and ing[0] == "ㅅ" and 초성 in 된소리_초성:  # ㅅ+ㄱ이 입력된 경우 ㄲ으로 변경
            ing[0] = 된소리_초성[초성]
            return ing, ret
        if ing:
            ret = _compose(ing)
            ing.clear()
        ing.append(초성)  # 빈 리스트에 초성 추가
        return ing, ret  # 입력 버퍼와 완성된 글자(초기값 None) 리턴

    # 아래부터 중성 판별
    if cell == 중성_점자["ㅐ"][0]:  # 중성으로 ㅐ가 입력된 경우
        if len(ing) == 3:  # 입력버퍼에 이미 종성까지 입력됐다면
            ret = j2h(*ing)  # 글자 완성 후
            ing.clear()  # 입력버퍼 비우기
        elif len(ing) == 2:  # 입력버퍼에 중성이 입력되어 있는데
            if ing[1] == "ㅑ":  # 그게 ㅑ라면
                ing[1] = "ㅒ"  # ㅒ로 변경
            elif ing[1] == "ㅘ":
                ing[1] = "ㅙ"
            elif ing[1] == "ㅝ":
                ing[1] = "ㅞ"
            elif ing[1] == "ㅜ":
                ing[1] = "ㅟ"
            else:  # 입력버퍼에 중성이 입력되어 있는데, 그게 복합 모음이 아니라면
                ret = j2h(*ing)  # 글자 완성 후
                ing.clear()  # 입력버퍼 지우기
        if len(ing) == 0:
            ing.append("ㅇ")
        if len(ing) == 1:
            ing.append("ㅐ")
        return ing, ret

    if cell in 중성_읽기:
        if len(ing) == 3 or len(ing) == 2:  # 입력버퍼에 이미 중성 또는 종성까지 들어가 있는 경우
            ret = j2h(*ing)  # 입력버퍼 값으로 글자 완성 후
            ing.clear()  # 입력버퍼 비우기
        if len(ing) == 0:  # 초성이 입력되지 않은 채 중성이 입력된 경우
            ing.append("ㅇ")  # ㅇ을 자동으로 입력
        ing.append(중성_읽기[cell])  # 중성 입력
        return ing, ret

    # 아래부터 종성 판별
    if cell in 종성_읽기:
        종성 = 종성_읽기[cell]
        if len(ing) == 3:  # 입력버퍼에 이미 종성까지 입력된 경우
            합친_종성 = 겹받침.get((ing[2], 종성))
            if 합친_종성:
                ing[2] = 합친_종성
                ret = j2h(*ing)
                ing.clear()
                return ing, ret
            ret = j2h(*ing)  # 위 경우가 아니라면 글자 완성 후 입력버퍼 비우기
            ing.clear()
        if len(ing) == 1:  # 초성만 입력되어 있는 겨우 ㅏ 자동 입력
            ing.append("ㅏ")
        if len(ing) == 0:  # 입력버퍼가 비워져있는 경우 아 자동 입력
            ing = ["ㅇ", "ㅏ"]
        ing.append(종성)  # 종성 입력
        return ing, ret

    if cell == ((0, 0), (0, 0), (0, 0)):
        # 전부 0이 입력된 경우 입력버퍼 비우기
        if len(ing) == 2 or len(ing) == 3:
            ret = j2h(*ing)
            ing.clear()
        elif len(ing) == 1:
            ret = j2h(ing[0], "ㅏ")
            ing.clear()
        return ing, ret

    return [], None


def braille_to_korean(cells: list[BrailleCell]) -> KoreanTextResult:
    ingredients: list[str] = []  # 입력버퍼
    real_text: list[str] = []  # 완성된 글자 모아두는 리스트

    for index, cell in enumerate(cells, start=1):
        if cell not in 읽기_가능한_점자:
            return ConversionError(index, cell, "등록되지 않은 한국어 점자 셀입니다.")

        ingredients, text = trans(cell, ingredients)
        if text:
            real_text.append(text)
        if cell == 공백_점자:
            real_text.append(" ")

    text = _compose(ingredients)
    if text:
        real_text.append(text)

    return "".join(real_text).rstrip()
