from __future__ import annotations

from model import BrailleCell, ConversionError


BrailleResult = list[BrailleCell] | ConversionError
EnglishResult = str | ConversionError

EMPTY_CELL: BrailleCell = ((0, 0), (0, 0), (0, 0))
CAPITAL_SIGN: BrailleCell = ((0, 0), (0, 0), (0, 1))


ENGLISH_TO_BRAILLE: dict[str, BrailleCell] = {
    " ": EMPTY_CELL,
    "a": ((1, 0), (0, 0), (0, 0)),
    "b": ((1, 0), (1, 0), (0, 0)),
    "c": ((1, 1), (0, 0), (0, 0)),
    "d": ((1, 1), (0, 1), (0, 0)),
    "e": ((1, 0), (0, 1), (0, 0)),
    "f": ((1, 1), (1, 0), (0, 0)),
    "g": ((1, 1), (1, 1), (0, 0)),
    "h": ((1, 0), (1, 1), (0, 0)),
    "i": ((0, 1), (1, 0), (0, 0)),
    "j": ((0, 1), (1, 1), (0, 0)),
    "k": ((1, 0), (0, 0), (1, 0)),
    "l": ((1, 0), (1, 0), (1, 0)),
    "m": ((1, 1), (0, 0), (1, 0)),
    "n": ((1, 1), (0, 1), (1, 0)),
    "o": ((1, 0), (0, 1), (1, 0)),
    "p": ((1, 1), (1, 0), (1, 0)),
    "q": ((1, 1), (1, 1), (1, 0)),
    "r": ((1, 0), (1, 1), (1, 0)),
    "s": ((0, 1), (1, 0), (1, 0)),
    "t": ((0, 1), (1, 1), (1, 0)),
    "u": ((1, 0), (0, 0), (1, 1)),
    "v": ((1, 0), (1, 0), (1, 1)),
    "w": ((0, 1), (1, 1), (0, 1)),
    "x": ((1, 1), (0, 0), (1, 1)),
    "y": ((1, 1), (0, 1), (1, 1)),
    "z": ((1, 0), (0, 1), (1, 1)),
}


BRAILLE_TO_ENGLISH: dict[BrailleCell, str] = {
    cell: char for char, cell in ENGLISH_TO_BRAILLE.items()
}


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
