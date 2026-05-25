from __future__ import annotations

from error import ConversionError
from model import BrailleCell
from rules.english import BRAILLE_TO_ENGLISH, CAPITAL_SIGN, ENGLISH_TO_BRAILLE


BrailleResult = list[BrailleCell] | ConversionError
EnglishResult = str | ConversionError


def english_char_to_braille(char: str, position: int) -> BrailleResult:
    if len(char) != 1:
        return ConversionError(position, char, "한 글자만 변환할 수 있습니다.")

    if char.isupper() and char.lower() in ENGLISH_TO_BRAILLE:
        return [CAPITAL_SIGN, ENGLISH_TO_BRAILLE[char.lower()]]

    if char in ENGLISH_TO_BRAILLE:
        return [ENGLISH_TO_BRAILLE[char]]

    return ConversionError(position, char, "영어 알파벳과 공백만 지원합니다.")


def english_to_braille(text: str) -> BrailleResult:
    cells: list[BrailleCell] = []

    for index, char in enumerate(text, start=1):
        result = english_char_to_braille(char, index)
        if isinstance(result, ConversionError):
            return result
        cells.extend(result)

    return cells


def braille_cell_to_english(cell: BrailleCell, position: int) -> EnglishResult:
    if cell == CAPITAL_SIGN:
        return ConversionError(position, cell, "대문자 표시 점자는 단독으로 변환할 수 없습니다.")

    if cell not in BRAILLE_TO_ENGLISH:
        return ConversionError(position, cell, "등록되지 않은 점자 셀입니다.")

    return BRAILLE_TO_ENGLISH[cell]


def braille_to_english(cells: list[BrailleCell]) -> EnglishResult:
    letters: list[str] = []
    index = 0

    while index < len(cells):
        cell = cells[index]
        position = index + 1

        if cell == CAPITAL_SIGN:
            next_index = index + 1
            if next_index >= len(cells):
                return ConversionError(position, cell, "대문자 표시 뒤에 영어 점자가 없습니다.")

            next_cell = cells[next_index]
            next_position = next_index + 1
            converted = braille_cell_to_english(next_cell, next_position)
            if isinstance(converted, ConversionError):
                return converted
            if converted == " ":
                return ConversionError(next_position, next_cell, "공백은 대문자로 만들 수 없습니다.")

            letters.append(converted.upper())
            index += 2
            continue

        converted = braille_cell_to_english(cell, position)
        if isinstance(converted, ConversionError):
            return converted
        letters.append(converted)
        index += 1

    return "".join(letters)
