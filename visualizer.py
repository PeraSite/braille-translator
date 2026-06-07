from __future__ import annotations

from model import BrailleCell


def cell_to_braille_char(cell: BrailleCell) -> str:
    dot_values = [
        (cell[0][0], 1),
        (cell[1][0], 2),
        (cell[2][0], 4),
        (cell[0][1], 8),
        (cell[1][1], 16),
        (cell[2][1], 32),
    ]
    code = sum(value for dot, value in dot_values if dot)
    return chr(0x2800 + code)


def visualize_cell(cell: BrailleCell) -> str:
    return "\n".join(" ".join("●" if dot else "○" for dot in row) for row in cell)


def visualize_cells(cells: list[BrailleCell]) -> str:
    if not cells:
        return "(빈 점자 배열)"

    braille_chars = " ".join(cell_to_braille_char(cell) for cell in cells)
    rows: list[str] = []

    for start in range(0, len(cells), 6):
        rendered_cells = [
            visualize_cell(cell).splitlines() for cell in cells[start : start + 6]
        ]
        for row_index in range(3):
            rows.append("    ".join(cell[row_index] for cell in rendered_cells))
        rows.append("")

    return f"점자 문자: {braille_chars}\n\n점자 셀:\n" + "\n".join(rows).rstrip()
