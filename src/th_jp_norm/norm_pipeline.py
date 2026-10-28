#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""複数のプリミティブな正規化処理を連続して実行するパイプラインモジュール。"""

import re

from .primitive.alpha import alpha_to_half, sp_to_underscore
from .primitive.char import (
    fuse_kana,
    kana_half_to_full,
    norm_prolonged,
    norm_rd,
    rm_br_wave_dash,
    to_safe_win,
)
from .primitive.spaces import rm_sp
from .primitive.numerals import circled_to_num, norm_br_num, numerals_to_half
from .primitive.symbols import (
    brackets_to_half,
    parentheses_to_full,
    norm_brackets,
)

# 【最適化】末尾数字のゼロサブレス用のコンパイル済み正規表現
# 0単体、または 0.5 などの小数点前の0は残し、
# 01 や 002 などの先頭の冗長な0（ゼロパディング）のみを分離してマッチさせます。
# fmt: off
TRAILING_SUBLESS_PATTERN = re.compile(
    r"(?:0+(?=\d))?(\d+(?:\.\d+)?)$"
)
# fmt: on


def execute_pipeline(text: str) -> str:
    """標準の正規化処理を順番に適用します。

    Args:
        text: 正規化対象の文字列。

    Returns:
        各処理を適用して整形した文字列。
    """
    # 0. 【最優先】記号の挟み込み削除、長音・リーダー化
    text = rm_br_wave_dash(text)
    text = norm_prolonged(text)
    text = norm_rd(text)
    text = norm_brackets(text)

    # 1. 各種文字・記号の半角化フェーズ
    text = alpha_to_half(text)
    text = numerals_to_half(text)
    text = circled_to_num(text)
    text = brackets_to_half(text)

    # 2. 半角英文字間の空白をアンダースコアへ
    text = sp_to_underscore(text)

    # 3. カナ正規化フェーズ（半角カナを全角、濁点結合など）
    text = kana_half_to_full(text)
    text = fuse_kana(text)

    # 4. 括弧内の数字単体の正規化・外枠外し
    text = norm_br_num(text)

    # 6. Windows禁止文字のクリーンアップ
    text = to_safe_win(text)

    # 7. 丸括弧を全角に統一（末尾括弧除去の精度を高めるため）
    text = parentheses_to_full(text)

    # 8. 末尾の全角丸括弧（レーベル名など）を自動除去
    text = _strip_trailing_parentheses(text)

    # 9. 末尾アラビア数字の整数部ゼロサブレス処理
    text = _subless_trailing_digits(text)

    # 10. 最終的な空白の削除
    text = rm_sp(text)

    return text


def execute_pipeline2(text: str) -> str:
    """括弧内の数字正規化を除く標準処理を順番に適用します。

    Args:
        text: 正規化対象の文字列。

    Returns:
        各処理を適用して整形した文字列。
    """
    # 0. 【最優先】記号の挟み込み削除、長音・リーダー化
    text = rm_br_wave_dash(text)
    text = norm_prolonged(text)
    text = norm_rd(text)
    text = norm_brackets(text)

    # 1. 各種文字・記号の半角化フェーズ
    text = alpha_to_half(text)
    text = numerals_to_half(text)
    text = circled_to_num(text)
    text = brackets_to_half(text)

    # 2. 半角英文字間の空白をアンダースコアへ
    text = sp_to_underscore(text)

    # 3. カナ正規化フェーズ（半角カナを全角、濁点結合など）
    text = kana_half_to_full(text)
    text = fuse_kana(text)

    # 4. Windows禁止文字のクリーンアップ
    text = to_safe_win(text)

    # 5. 丸括弧を全角に統一（末尾括弧除去の精度を高めるため）
    text = parentheses_to_full(text)

    # 6. 最終的な空白の削除
    text = rm_sp(text)

    return text


def _subless_trailing_digits(text: str) -> str:
    """末尾の数字の整数部にある冗長な先頭ゼロを除去します。

    Args:
        text: 末尾にアラビア数字を含む文字列。

    Returns:
        整数部の先頭ゼロを除去した文字列。
    """
    if match := TRAILING_SUBLESS_PATTERN.search(text):
        # match.group(1) は冗長な先頭の0が除かれた数字文字列
        num_str = match.group(1)

        # 冗長な0を含めたマッチ全体の長さを取得し、ベース文字列を切り出す
        matched_len = len(match.group(0))
        base_text = text[:-matched_len]

        return f"{base_text}{num_str}"
    return text


def _strip_trailing_hyphen(text: str) -> str:
    """文字列末尾のハイフンを除去します。

    Args:
        text: 変換対象の文字列。

    Returns:
        末尾のハイフンを除去した文字列。
    """
    if text.endswith("-"):
        return text[:-1]
    return text


def _strip_trailing_parentheses(text: str) -> str:
    """末尾の丸括弧とその内容を、例外ラベルを除いて削除します。

    Args:
        text: 末尾の丸括弧を確認する文字列。

    Returns:
        末尾の括弧部分を削除した文字列。
    """
    if not text:
        return text

    exceptions = (
        "（上）",
        "（中）",
        "（下）",
        "（上巻）",
        "（中巻）",
        "（下巻）",
        "（前編）",
        "（中編）",
        "（後編）",
    )

    if text.endswith(exceptions):
        return text

    last_char = text[-1]
    if last_char != "）":
        return text

    # 括弧のネスト解析ロジック（既存のロジックをそのまま維持）
    depth = 0
    start_idx = -1
    for i in range(len(text) - 1, -1, -1):
        if text[i] == "）":
            depth += 1
        elif text[i] == "（":
            depth -= 1
            if depth == 0:
                start_idx = i
                break

    if start_idx != -1:
        # 括弧とその中身を削除
        text = text[:start_idx]
        # 削除後に末尾にハイフンが残れば安全に除去
        text = _strip_trailing_hyphen(text)

    return text
