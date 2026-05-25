from __future__ import annotations

from model import BrailleCell


def visualize_cell(cell: BrailleCell) -> str:
    return "\n".join(" ".join("O" if dot else "." for dot in row) for row in cell)


def visualize_cells(cells: list[BrailleCell]) -> str:
    if not cells:
        return "(빈 점자 배열)"

    rendered_cells = [visualize_cell(cell).splitlines() for cell in cells]
    rows: list[str] = []

    for row_index in range(3):
        rows.append("   ".join(cell[row_index] for cell in rendered_cells))

    return "\n".join(rows)

