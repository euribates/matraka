#!/usr/bin/env python3

import random
from typing import Tuple
from dataclasses import dataclass


def get_hex_from_rgb(red=128, green=128, blue=128) -> str:
    return f'#{red:02x}{green:02x}{blue:02x}'.upper()


def get_rgb_from_hex(value: str) -> Tuple[int, int, int]:
    red = int(value[1:3], base=16)
    green = int(value[3:5], base=16)
    blue = int(value[5:7], base=16)
    return red, green, blue


@dataclass(frozen=True)
class Color:
    """A class to work with colors.
    """

    red: int = 128
    green: int = 128
    blue: int = 128

    def __str__(self):
        return get_hex_from_rgb(self.red, self.green, self.blue)

    def __len__(self):
        return 7

    @classmethod
    def random_color(Cls):
        red = random.randrange(0, 256)
        green = random.randrange(0, 256)
        blue = random.randrange(0, 256)
        return Cls(red, green, blue)

    def replace(self, red=None, green=None, blue=None):
        return Color(
            red or self.red,
            green or self.green,
            blue or self.blue,
            )

    def luminance(self) -> float:
        result = 0.2126 * self.red + 0.7152 * self.green + 0.0722 * self.blue
        return round(result / 255.0, 4)

    def foreground_color(self):
        return BLACK if self.luminance() > 0.5 else WHITE


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
SILVER = Color(192, 192, 192)
