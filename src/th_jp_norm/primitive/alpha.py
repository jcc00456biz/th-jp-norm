#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""アルファベットの全角・半角変換関数を提供します。"""

import re

# fmt: off
# 半角化用: Ａ-Ｚ, ａ-ｚ を 0xXXXX リテラルで定義
Z2H_ALPHA_TRANSLATION = {
    code: code - 0xFEE0 for code in range(0xFF21, 0xFF3B)
} | {
    code: code - 0xFEE0 for code in range(0xFF41, 0xFF5B)
}
# fmt: on


def alpha_to_half(text: str) -> str:
    """アルファベットを半角に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        全角アルファベットを半角に変換した文字列。
    """
    return text.translate(Z2H_ALPHA_TRANSLATION)


# fmt: off
# 全角化用: 半角から全角へ（既存の辞書を反転）
H2Z_ALPHA_TRANSLATION = {
    v: k for k, v in Z2H_ALPHA_TRANSLATION.items()
}
# fmt: on


def alpha_to_full(text: str) -> str:
    """アルファベットを全角に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        半角アルファベットを全角に変換した文字列。
    """
    return text.translate(H2Z_ALPHA_TRANSLATION)


def sp_to_underscore(text: str) -> str:
    """アルファベット間の空白をアンダースコアに置換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        アルファベット間の空白をアンダースコアに置換した文字列。

    Examples:
        >>> sp_to_underscore("Apple Juice")
        'Apple_Juice'
    """
    # PEP 8 の行長制限を考慮し、パターンを独立させて記述
    pattern = r"(?<=[A-Za-z])\s(?=[A-Za-z])"
    return re.sub(pattern, "_", text)


def capitalize_first(text: str) -> str:
    """先頭を大文字、それ以降を小文字に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        先頭を大文字、それ以降を小文字にした文字列。
    """
    return text[:1].upper() + text[1:].lower()


def capitalize_fullwidth_first(text: str) -> str:
    """全角アルファベットの先頭1文字を全角大文字にし、残りの全角アルファベットを全角小文字にします。

    半角文字やその他の文字は一切変換せず、そのまま保持します。

    Args:
        text: 変換対象の文字列。

    Returns:
        先頭とそれ以降の大文字・小文字を調整した文字列。
    """
    if not text:
        return ""

    chars: list[str] = []

    # 先頭文字の処理：全角小文字なら全角大文字に変換
    first_char: str = text[0]
    first_code: int = ord(first_char)
    if 0xFF41 <= first_code <= 0xFF5A:
        chars.append(chr(first_code - 0x20))
    else:
        chars.append(first_char)

    # 2文字目以降の処理：全角大文字なら全角小文字に変換
    for char in text[1:]:
        code: int = ord(char)
        if 0xFF21 <= code <= 0xFF3A:
            chars.append(chr(code + 0x20))
        else:
            chars.append(char)

    return "".join(chars)
