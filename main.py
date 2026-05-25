from __future__ import annotations

import ast

from english import braille_to_english, english_to_braille
from model import BrailleCell, ConversionError
from visualizer import visualize_cells


def parse_braille_cells(raw_value: str) -> list[BrailleCell] | ConversionError:
    try:
        value = ast.literal_eval(raw_value)
    except (SyntaxError, ValueError) as error:
        return ConversionError(1, raw_value, f"점자 배열 문법이 올바르지 않습니다: {error}")

    if not isinstance(value, list):
        return ConversionError(1, value, "점자 배열은 list 형식이어야 합니다.")

    parsed_cells: list[BrailleCell] = []
    for index, cell in enumerate(value, start=1):
        if not _is_braille_cell(cell):
            return ConversionError(index, cell, "점자 한 글자는 3x2 크기의 0/1 배열이어야 합니다.")
        parsed_cells.append(tuple(tuple(row) for row in cell))  # type: ignore[arg-type]

    return parsed_cells


def _is_braille_cell(value: object) -> bool:
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        return False

    for row in value:
        if not isinstance(row, (tuple, list)) or len(row) != 2:
            return False
        if any(dot not in (0, 1) for dot in row):
            return False

    return True


def translate_english_to_braille() -> None:
    text = input("영어 입력: ")
    result = english_to_braille(text)

    if isinstance(result, ConversionError):
        print(f"오류: {result}")
        return

    print("점자 배열:")
    print(result)
    print("점자 보기:")
    print(visualize_cells(result))


def translate_braille_to_english() -> None:
    raw_cells = input("점자 배열 입력: ")
    cells = parse_braille_cells(raw_cells)

    if isinstance(cells, ConversionError):
        print(f"오류: {cells}")
        return

    result = braille_to_english(cells)
    if isinstance(result, ConversionError):
        print(f"오류: {result}")
        return

    print("영어:")
    print(result)


def main() -> None:
    while True:
        print()
        print("1. 영어 -> 점자")
        print("2. 점자 -> 영어")
        print("3. 종료")
        choice = input("선택: ").strip()

        if choice == "1":
            translate_english_to_braille()
        elif choice == "2":
            translate_braille_to_english()
        elif choice == "3":
            print("종료합니다.")
            break
        else:
            print("1, 2, 3 중에서 선택해 주세요.")


if __name__ == "__main__":
    main()

