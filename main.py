from __future__ import annotations

from error import ConversionError
from parser import parse_braille_cells
from translators.english import braille_to_english, english_to_braille
from visualizer import visualize_cells


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
