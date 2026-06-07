from __future__ import annotations

import os
import sys
from pathlib import Path
from pprint import pformat


def _configure_tk_library_paths():
    prefixes = dict.fromkeys((Path(sys.base_prefix), Path(sys.prefix)))

    for prefix in prefixes:
        tcl_library = prefix / "lib" / "tcl8.6"
        tk_library = prefix / "lib" / "tk8.6"

        if tcl_library.exists():
            os.environ.setdefault("TCL_LIBRARY", str(tcl_library))
        if tk_library.exists():
            os.environ.setdefault("TK_LIBRARY", str(tk_library))


_configure_tk_library_paths()

import tkinter as tk
from tkinter import ttk

from error import ConversionError
from model import BrailleCell
from translators.english import braille_to_english, english_to_braille
from translators.korean import braille_to_korean, korean_to_braille
from visualizer import visualize_cells


class BrailleTranslatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("점자 번역기")

        self.language_var = tk.StringVar(value="한국어")
        self.direction_var = tk.StringVar(value="점역")
        self.braille_buttons: list[list[tk.Button]] = []
        self.braille_values = [[0, 0], [0, 0], [0, 0]]
        self.braille_input_list: list[BrailleCell] = []

        self._build_widgets()
        self.update_input_type()
        self._set_initial_window_geometry()

    def _set_initial_window_geometry(self):
        width = 700
        height = 820

        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        usable_height = max(720, screen_height - 120)
        height = min(height, usable_height)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_widgets(self):
        title = tk.Label(
            self.root, text="점자 번역기", font=("맑은 고딕", 22, "bold")
        )
        title.pack(pady=20)

        language_frame = tk.Frame(self.root)
        language_frame.pack(pady=5)

        tk.Label(language_frame, text="언어 선택", font=("맑은 고딕", 12)).pack(
            side="left", padx=10
        )

        language_combo = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=["한국어", "영어"],
            state="readonly",
            width=15,
            font=("맑은 고딕", 11),
        )
        language_combo.pack(side="left")

        direction_frame = tk.Frame(self.root)
        direction_frame.pack(pady=5)

        tk.Label(direction_frame, text="번역 방향", font=("맑은 고딕", 12)).pack(
            side="left", padx=10
        )

        direction_combo = ttk.Combobox(
            direction_frame,
            textvariable=self.direction_var,
            values=["점역", "역점역"],
            state="readonly",
            width=15,
            font=("맑은 고딕", 11),
        )
        direction_combo.pack(side="left")
        direction_combo.bind("<<ComboboxSelected>>", lambda _event: self.update_input_type())

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        input_label = tk.Label(
            self.input_frame, text="입력", font=("맑은 고딕", 13, "bold")
        )
        input_label.pack(anchor="w")

        self.hint_label = tk.Label(
            self.input_frame,
            text="번역할 문장을 입력하세요.",
            fg="gray",
            font=("맑은 고딕", 10),
        )
        self.hint_label.pack(pady=5)

        self.text_input_box = tk.Text(
            self.input_frame,
            width=65,
            height=7,
            font=("맑은 고딕", 11),
        )
        self.text_input_box.pack()

        self.braille_frame = tk.Frame(self.input_frame)

        dot_frame = tk.Frame(self.braille_frame)
        dot_frame.pack()

        for row in range(3):
            row_buttons = []
            for col in range(2):
                button = tk.Button(
                    dot_frame,
                    text="○",
                    width=3,
                    height=1,
                    font=("맑은 고딕", 12),
                    bg="white",
                    fg="black",
                    command=lambda row=row, col=col: self.toggle_dot(row, col),
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                row_buttons.append(button)
            self.braille_buttons.append(row_buttons)

        button_frame = tk.Frame(self.braille_frame)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="점자 추가",
            command=self.add_braille,
            width=10,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="초기화",
            command=self.reset_braille,
            width=10,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="입력 지우기",
            command=self.clear_braille_input,
            width=10,
        ).pack(side="left", padx=5)

        self.input_preview = tk.Text(
            self.braille_frame,
            width=65,
            height=3,
            font=("맑은 고딕", 10),
        )
        self.input_preview.pack(pady=5)
        self.input_preview.config(state="disabled")

        tk.Button(
            self.root,
            text="번역하기",
            command=self.show_result,
            width=15,
            font=("맑은 고딕", 12, "bold"),
        ).pack(pady=20)

        tk.Label(self.root, text="출력", font=("맑은 고딕", 13, "bold")).pack(
            anchor="w", padx=50
        )

        self.output_box = tk.Text(
            self.root,
            width=65,
            height=12,
            font=("맑은 고딕", 11),
        )
        self.output_box.pack(pady=5)
        self.output_box.config(state="disabled")

    def update_input_type(self):
        direction = self.direction_var.get()

        if direction == "역점역":
            self.text_input_box.pack_forget()
            self.braille_frame.pack(pady=5)
            self.hint_label.config(text="점자를 버튼으로 입력한 뒤 '점자 추가'를 누르세요.")
            return

        self.braille_frame.pack_forget()
        self.text_input_box.pack()
        self.hint_label.config(text="번역할 문장을 입력하세요.")

    def toggle_dot(self, row: int, col: int):
        self.braille_values[row][col] = 1 - self.braille_values[row][col]
        button = self.braille_buttons[row][col]

        if self.braille_values[row][col] == 1:
            button.config(text="●", bg="black", fg="white")
        else:
            button.config(text="○", bg="white", fg="black")

    def add_braille(self):
        cell: BrailleCell = (
            (self.braille_values[0][0], self.braille_values[0][1]),
            (self.braille_values[1][0], self.braille_values[1][1]),
            (self.braille_values[2][0], self.braille_values[2][1]),
        )
        self.braille_input_list.append(cell)
        self._refresh_input_preview()
        self.reset_braille()

    def reset_braille(self):
        for row in range(3):
            for col in range(2):
                self.braille_values[row][col] = 0
                self.braille_buttons[row][col].config(text="○", bg="white", fg="black")

    def clear_braille_input(self):
        self.braille_input_list.clear()
        self.reset_braille()
        self._refresh_input_preview()

    def show_result(self):
        language = self.language_var.get()
        direction = self.direction_var.get()

        if direction == "점역":
            text = self.text_input_box.get("1.0", "end-1c")
            result = (
                korean_to_braille(text)
                if language == "한국어"
                else english_to_braille(text)
            )
            if isinstance(result, ConversionError):
                self._write_output(f"오류: {result}")
                return

            self._write_output(
                f"점자 보기:\n{visualize_cells(result)}\n\n"
                f"점자 배열:\n{pformat(result, width=72)}"
            )
            return

        result = (
            braille_to_korean(self.braille_input_list)
            if language == "한국어"
            else braille_to_english(self.braille_input_list)
        )
        if isinstance(result, ConversionError):
            self._write_output(f"오류: {result}")
            return

        self._write_output(f"역점역 결과:\n{result}")

    def _refresh_input_preview(self):
        self.input_preview.config(state="normal")
        self.input_preview.delete("1.0", tk.END)
        self.input_preview.insert(tk.END, str(self.braille_input_list))
        self.input_preview.config(state="disabled")

    def _write_output(self, text: str):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.config(state="disabled")


def main():
    root = tk.Tk()
    BrailleTranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
