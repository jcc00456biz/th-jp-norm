import pytest

from th_jp_norm.primitive.numerals import (
    circled_to_num,
    dai_to_num,
    kan_to_num,
    norm_br_num,
    norm_trailing_kanji,
    norm_trailing_roman,
    numerals_to_half,
    parse_kanji_number,
    rm_volume_suffix,
    rom_to_num,
)


def test_numerals_to_half() -> None:
    assert numerals_to_half("０１２３４５６７８９") == "0123456789"
    assert numerals_to_half("A１２") == "A12"


def test_kan_to_num() -> None:
    assert kan_to_num("零一二三四五六七八九") == "0123456789"


def test_dai_to_num() -> None:
    assert dai_to_num("壱弐参肆伍陸漆捌玖拾佰仟萬") == "12345678910100100010000"


def test_rom_to_num() -> None:
    assert rom_to_num("ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ") == "123456789101112"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("123", "123"),
        ("二〇二四", "2024"),
        ("一二三四", "1234"),
        ("十二", "12"),
        ("百二十三", "123"),
        ("一万二千三百四十五", "12345"),
        ("壱萬弐仟参佰肆拾伍", "12345"),
        ("対象外", "対象外"),
        ("一二a", "一二a"),
    ],
)
def test_parse_kanji_number(text: str, expected: str) -> None:
    assert parse_kanji_number(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("番号（００１）", "番号1"),
        ("番号[十二]", "番号12"),
        ("番号（ 〇〇 ）", "番号0"),
        ("番号（第十二）", "番号（第十二）"),
        ("番号[建物]", "番号[建物]"),
    ],
)
def test_norm_br_num(text: str, expected: str) -> None:
    assert norm_br_num(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Vol.001", "1"),
        ("vol １２", "12"),
        ("第１２話", "12"),
        ("一巻", "1"),
        ("第壱話", "1"),
        ("本編", "本編"),
    ],
)
def test_rm_volume_suffix(text: str, expected: str) -> None:
    assert rm_volume_suffix(text) == expected


def test_circled_to_num() -> None:
    assert circled_to_num("①⑩⑳") == "11020"
    assert circled_to_num("㉑") == "㉑"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("本編Ⅳ", "本編4"),
        ("本編 IV", "本編 4"),
        ("本編 ABC", "本編 ABC"),
        ("", ""),
    ],
)
def test_norm_trailing_roman(text: str, expected: str) -> None:
    assert norm_trailing_roman(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("第十二", "第12"),
        ("版二〇二四", "版2024"),
        ("対象外", "対象外"),
        ("", ""),
    ],
)
def test_norm_trailing_kanji(text: str, expected: str) -> None:
    assert norm_trailing_kanji(text) == expected
