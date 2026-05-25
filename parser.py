from __future__ import annotations

import ast

from error import ConversionError
from model import BrailleCell


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
