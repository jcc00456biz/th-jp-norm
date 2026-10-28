import pytest

from th_jp_norm.primitive.char import (
    fuse_kana,
    kana_half_to_full,
    norm_prolonged,
    norm_rd,
    rm_br_wave_dash,
    to_safe_win,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ｶﾞｯﾂﾎﾟｰｽﾞ", "ガッツポーズ"),
        ("ﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ", "パピプペポ"),
        ("ｶﾅ｡､･", "カナ。、・"),
        ("漢字 ABC", "漢字 ABC"),
    ],
)
def test_kana_half_to_full(text: str, expected: str) -> None:
    assert kana_half_to_full(text) == expected


def test_fuse_kana_composes_decomposed_characters() -> None:
    assert fuse_kana("か\u3099") == "が"


@pytest.mark.parametrize(
    ("text", "expected"),
    [("A—B", "AーB"), ("A–B―C", "AーBーC"), ("A-B", "A-B")],
)
def test_norm_prolonged(text: str, expected: str) -> None:
    assert norm_prolonged(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("……", "・・・"), ("⋯", "・・・"), ("・・", "・・・"), ("・", "・")],
)
def test_norm_rd(text: str, expected: str) -> None:
    assert norm_rd(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("前～削除～後", "前後"),
        ("前〜削除〜後", "前後"),
        ("前～削除", "前～削除"),
        ("変更なし", "変更なし"),
    ],
)
def test_rm_br_wave_dash(text: str, expected: str) -> None:
    assert rm_br_wave_dash(text) == expected


def test_to_safe_win_replaces_forbidden_characters_and_symbols() -> None:
    assert to_safe_win('a/b:c*?"<>|!&%+=♡♥') == (
        "a／b：c＊？”＜＞｜！＆％＋＝"
    )


def test_to_safe_win_replaces_double_exclamation_variants() -> None:
    assert to_safe_win("‼‼︎⁈⁉") == "！！！！？！！？"
