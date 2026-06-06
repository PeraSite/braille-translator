from __future__ import annotations

from jamo import h2j, j2h, jamo_to_hcj

from error import ConversionError
from model import BrailleCell
from rules.korean import (
    BraillePattern,
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
    # 한글 점자는 글자 단위가 아니라 초성/중성/종성 단위로 규칙이 나뉘기 때문에 먼저 자모로 분리한다.
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
        # 공백은 자모 분리 대상이 아니므로 별도의 점자 셀로 바로 저장한다.
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


def braille_to_korean(cells: list[BrailleCell]) -> KoreanTextResult:
    real_text: list[str] = []
    index = 0

    # 변환 중간에 잘못된 점자를 만나면 어느 위치가 문제인지 알려주기 위해 먼저 전체 입력을 검사한다.
    for position, cell in enumerate(cells, start=1):
        if cell not in 읽기_가능한_점자:
            return ConversionError(position, cell, "등록되지 않은 한국어 점자 셀입니다.")

    while index < len(cells):
        cell = cells[index]

        if cell == 공백_점자:
            real_text.append(" ")
            index += 1
            continue

        # 초성이 없는 글자는 ㅇ으로 시작하므로 기본 초성을 ㅇ으로 둔다. 예: 아, 우, 이
        초성 = "ㅇ"
        중성 = None
        종성 = None

        다음_점자 = cells[index + 1] if index + 1 < len(cells) else None
        # 일부 점자는 초성과 중성 표에 동시에 들어갈 수 있다.
        # 다음 점자가 중성이면 현재 점자를 새 글자의 초성으로 보는 것이 자연스럽다.
        if cell in 초성_읽기 and (cell not in 중성_읽기 or 다음_점자 in 중성_읽기):
            초성 = 초성_읽기[cell]
            index += 1

            # 된소리는 별도 점자 뒤에 기본 초성이 이어지는 방식이라 두 칸을 한 초성으로 합친다.
            if cell == ((0, 0), (0, 0), (0, 1)) and index < len(cells):
                다음_초성 = 초성_읽기.get(cells[index])
                if 다음_초성 in 된소리_초성:
                    초성 = 된소리_초성[다음_초성]
                    index += 1

        if index >= len(cells) or cells[index] not in 중성_읽기:
            return ConversionError(index + 1, cell, "중성 점자를 찾을 수 없습니다.")

        중성 = 중성_읽기[cells[index]]
        index += 1

        # ㅒ, ㅙ, ㅞ, ㅟ처럼 두 개의 점자로 표현되는 모음은 앞 모음에 ㅐ 점자가 붙은 형태로 처리한다.
        if index < len(cells) and cells[index] == 중성_점자["ㅐ"][0]:
            if 중성 == "ㅑ":
                중성 = "ㅒ"
                index += 1
            elif 중성 == "ㅘ":
                중성 = "ㅙ"
                index += 1
            elif 중성 == "ㅝ":
                중성 = "ㅞ"
                index += 1
            elif 중성 == "ㅜ":
                중성 = "ㅟ"
                index += 1

        # 받침 점자가 다음 글자의 초성으로도 해석될 수 있으면, 다음에 중성이 오는지 보고 새 글자로 넘긴다.
        if index < len(cells) and cells[index] in 종성_읽기:
            다음_점자 = cells[index + 1] if index + 1 < len(cells) else None
            다음_글자_초성 = cells[index] in 초성_읽기 and 다음_점자 in 중성_읽기

            if not 다음_글자_초성:
                종성 = 종성_읽기[cells[index]]
                index += 1

        if 종성:
            real_text.append(j2h(초성, 중성, 종성))
        else:
            real_text.append(j2h(초성, 중성))

    return "".join(real_text).rstrip()
