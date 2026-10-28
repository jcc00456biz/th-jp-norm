import pytest

from th_jp_norm.primitive.spaces import clps_sp, rm_sp
from th_jp_norm.primitive.symbols import (
    brackets_to_half,
    norm_brackets,
    optimize_brackets,
    parentheses_to_full,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (" a\u3000b\tc\n", "abc"),
        ("a\u00a0\u2003b", "ab"),
        ("a\x00b\x7fc", "abc"),
        ("", ""),
    ],
)
def test_rm_sp(text: str, expected: str) -> None:
    assert rm_sp(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  a   b  ", "a b"),
        ("\u3000a\t\tb\u3000", "a b"),
        ("a\nb", "a\nb"),
    ],
)
def test_clps_sp(text: str, expected: str) -> None:
    assert clps_sp(text) == expected


def test_brackets_to_half_only_changes_square_brackets() -> None:
    assert brackets_to_half("［項目］（内容）") == "[項目]（内容）"


def test_parentheses_to_full() -> None:
    assert parentheses_to_full("(項目) []") == "（項目） []"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("A（x）B", "A （x） B"),
        ("（a\u200bb）", "（ab）"),
        ("A「b」C", "A 「b」 C"),
        ("", ""),
    ],
)
def test_optimize_brackets(text: str, expected: str) -> None:
    assert optimize_brackets(text) == expected


def test_norm_brackets_converts_double_corner_quotes() -> None:
    assert norm_brackets("『題名』と『副題』") == "「題名」と「副題」"
