#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""空白文字の除去・圧縮関数を提供します。"""

import re


def rm_sp(text: str) -> str:
    """文字列からすべての空白文字および表示できない制御文字を完全に削除します。

    対象: 半角空白、全角空白、各種特殊スペース（NBSP等）、および
    改行、タブ、Null文字などのすべての制御文字（\\x00-\\x1F, \\x7F）。

    Args:
        text: 空白・制御文字を除去する文字列。

    Returns:
        空白および対象の制御文字を除去した文字列。
    """
    # \\s に加え、全角空白、特殊スペース、および C0 制御文字の範囲を指定
    pattern = r"[\s\u3000\u00A0\u2000-\u200F\x00-\x1F\x7F]+"
    return re.sub(pattern, "", text)


def clps_sp(text: str) -> str:
    """連続する空白を1つの半角スペースに正規化します。

    全角空白を半角に変換し、先頭と末尾の空白も除去します。

    Args:
        text: 空白を正規化する文字列。

    Returns:
        空白を正規化した文字列。
    """
    # 全角スペース（U+3000）を半角に変換
    text = text.replace("\u3000", " ")

    # 連続する空白（TAB含む）を1つの半角スペースに置換
    pattern = r"[ \t]+"
    text = re.sub(pattern, " ", text)

    return text.strip()
