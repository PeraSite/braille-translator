from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConversionError:
    position: int
    value: object
    message: str

    def __str__(self) -> str:
        return f"{self.position}번째 값 {self.value!r}: {self.message}"

