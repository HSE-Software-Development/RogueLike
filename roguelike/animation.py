from roguelike.interfaces import IAnimation
from typing import Any, override
from pydantic import BaseModel
from roguelike.types import Cell, Color
import os


class Pixel(BaseModel):
    char: str
    color: Color = Color.WHITE
    z_buffer: int = -1

    def __str__(self):
        return f"\033[{self.color.value}m{self.char}\033[0m"


class Text(BaseModel):
    text: str
    color: Color = Color.WHITE

    def __str__(self):
        return f"\033[{self.color.value}m{self.text}\033[0m"


class Animation(IAnimation):

    def __init__(self, margin_x: int, margin_y: int, width: int, height: int):
        self._width = width
        self._height = height
        self._margin_x = margin_x
        self._margin_y = margin_y

        self._canvas = self._clean_canvas()
        self._text: list[Text] = []

    def _clean_canvas(self) -> list[list[Pixel]]:
        return [
            [Pixel(char=" ") for _ in range(self._margin_x + self._width)]
            for _ in range(self._margin_y + self._height)
        ]

    @override
    def draw(self, cell, char, color=Color.WHITE, z_buffer=0):
        if cell.x < 0 or cell.y < 0 or cell.x >= self._width or cell.y >= self._height:
            return

        pixel = self._canvas[cell.y + self._margin_y][cell.x + self._margin_x]

        if pixel.z_buffer <= z_buffer:
            pixel.z_buffer = z_buffer
            pixel.char = char
            pixel.color = color

    @override
    def print(self, text: str, color: Color = Color.WHITE):
        self._text.append(Text(text=text, color=color))

    def render(self):
        for y in range(self._margin_y + self._height):
            for x in range(self._margin_x + self._width):
                pixel = self._canvas[y][x]
                print(str(pixel), end="")
            print()

        print("Text Output:")
        for text in self._text:
            print(str(text))

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
        self._canvas = self._clean_canvas()
