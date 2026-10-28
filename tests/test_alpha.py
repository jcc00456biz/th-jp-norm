import pytest

from th_jp_norm.primitive.alpha import (
    alpha_to_full,
    alpha_to_half,
    capitalize_first,
    capitalize_fullwidth_first,
    sp_to_underscore,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ＡＢＣｄｅｆ", "ABCdef"),
        ("ＡＢＣ １２３！", "ABC １２３！"),
        ("ASCII", "ASCII"),
        ("", ""),
    ],
)
def test_alpha_to_half(text: str, expected: str) -> None:
    assert alpha_to_half(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ABCdef", "ＡＢＣｄｅｆ"),
        ("ABC 123!", "ＡＢＣ 123!"),
        ("全角", "全角"),
    ],
)
def test_alpha_to_full(text: str, expected: str) -> None:
    assert alpha_to_full(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Apple Juice", "Apple_Juice"),
        ("A B", "A_B"),
        ("A  B", "A  B"),
        ("日本語 の 文", "日本語 の 文"),
    ],
)
def test_sp_to_underscore(text: str, expected: str) -> None:
    assert sp_to_underscore(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("hELLO", "Hello"), ("", ""), ("日本語", "日本語")],
)
def test_capitalize_first(text: str, expected: str) -> None:
    assert capitalize_first(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("ａＢＣ", "Ａｂｃ"), ("ABC", "ABC"), ("", ""), ("ｘ猫", "Ｘ猫")],
)
def test_capitalize_fullwidth_first(text: str, expected: str) -> None:
    assert capitalize_fullwidth_first(text) == expected
