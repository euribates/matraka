#!/usr/bin/env python3

import pytest

from tags.colors import get_hex_from_rgb
from tags.colors import get_rgb_from_hex
from tags.colors import Color
from tags.colors import BLACK, WHITE


def test_get_hex_from_rgb():
    assert get_hex_from_rgb() == '#808080'
    assert get_hex_from_rgb(red=255) == '#FF8080'
    assert get_hex_from_rgb(green=255) == '#80FF80'
    assert get_hex_from_rgb(blue=255) == '#8080FF'
    assert get_hex_from_rgb(0, 0, 0) == '#000000'
    assert get_hex_from_rgb(255, 255, 255) == '#FFFFFF'
    assert get_hex_from_rgb(78, 137, 69) == '#4E8945'


def test_get_rgb_from_hex():
    assert get_rgb_from_hex('#4E8901') == (78, 137, 1)
    assert get_rgb_from_hex('#4E8945') == (78, 137, 69)
    assert get_rgb_from_hex('#000000') == (0, 0, 0)
    assert get_rgb_from_hex('#FFFFFF') == (255, 255, 255)


def test_create_color():
    color = Color(78, 137, 69)
    assert color.red == 78
    assert color.green == 137
    assert color.blue == 69
    assert str(color) == '#4E8945'


def test_create_random_color():
    color = Color.random_color()
    assert 0 <= color.red < 256
    assert 0 <= color.green < 256
    assert 0 <= color.blue < 256


def test_replace_color():
    color = Color(78, 137, 69)
    assert str(color) == '#4E8945'
    otro_color = color.replace(blue=1)
    assert str(color) == '#4E8945'
    assert str(otro_color) == '#4E8901'
    assert otro_color.blue == 1

    
def test_luminance():
    assert Color(0, 0, 0).luminance() == 0.0
    assert Color(255, 255, 255).luminance() == 1.0
    assert Color(128, 128, 128).luminance() == 0.502
    assert Color(78, 137, 69).luminance() == 0.4688


def test_foregroun_color_white():
    color = Color(78, 137, 69)
    assert color.luminance() <= 0.5
    assert color.foreground_color() == WHITE


def test_foregroun_color_black():
    color = Color(178, 137, 169)
    assert color.luminance() > 0.5
    assert color.foreground_color() == BLACK


if __name__ == "__main__":
    pytest.main()
