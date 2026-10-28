#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""記号の半角化・全角化をピンポイントで行うプリミティブモジュール。"""

import re

# 全角四角括弧を半角に変換するマッピング
# fmt: off
Z2H_BRACKET_MAP = str.maketrans({
    "［": "[", "］": "]",
})
# fmt: on

# 半角丸括弧を全角に変換するマッピング
# fmt: off
H2Z_PAREN_MAP = str.maketrans({
    "(": "（", ")": "）",
})
# fmt: on


def brackets_to_half(text: str) -> str:
    """全角の四角括弧（［］）を半角（[]）に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        全角の四角括弧を半角に置換した文字列。
    """
    return text.translate(Z2H_BRACKET_MAP)


def parentheses_to_full(text: str) -> str:
    """半角の丸括弧（()）を全角（（））に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        半角の丸括弧を全角に置換した文字列。
    """
    return text.translate(H2Z_PAREN_MAP)


# 表示できない空白文字（制御文字、通常の空白以外の特殊な空白など）のパターン
# \u200b(Zero Width Space)などを対象とし、通常の半角/全角空白は含めません。
INVISIBLE_SPACES_RE = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200d\ufeff]")

# 対象となる括弧のペア（左括弧: 右括弧）
# PEP 8の行長制限を考慮し、# fmt: off で1行に配置
# fmt: off
BRACKETS = {
    chr(0xFF08): chr(0xFF09), chr(0x0028): chr(0x0029),  # 丸括弧 （）()
    chr(0x300C): chr(0x300D),                            # 鉤括弧 「」
    chr(0x300E): chr(0x300F),                            # 二重鉤括弧 『』
    chr(0x3010): chr(0x3011),                            # 隅付括弧 【】
    chr(0xFF3B): chr(0xFF3D), chr(0x005B): chr(0x005D),  # 角括弧 ［］[]
    chr(0xFF5B): chr(0xFF5D), chr(0x007B): chr(0x007D),  # 波括弧 ｛｝{}
}
# fmt: on

# 正規表現用にすべての左括弧と右括弧をエスケープして結合
_left_brackets = "".join(re.escape(k) for k in BRACKETS.keys())
_right_brackets = "".join(re.escape(v) for v in BRACKETS.values())

# 括弧で囲まれた中身を抽出するための正規表現（最小マッチ）
BRACKET_PATTERN = re.compile(
    f"([{_left_brackets}])(.*?)([{_right_brackets}])", re.DOTALL
)


def optimize_brackets(text: str) -> str:
    """文字列中の括弧内と括弧外を最適化します。

    Args:
        text: 最適化対象の文字列。

    Returns:
        括弧内の不可視文字を除去し、括弧の前後の空白を調整した文字列。
    """
    if not text:
        return text

    # 1. 括弧内の最適化（表示できない空白文字を除去）
    def _replace_bracket_content(match: re.Match) -> str:
        """対応する括弧ペア内の不可視文字を取り除きます。

        Args:
            match: 開き括弧・内容・閉じ括弧に一致した結果。

        Returns:
            対応する括弧ペア内の不可視文字を除去した文字列。
        """
        open_b = match.group(1)
        content = match.group(2)
        close_b = match.group(3)

        # 対応する正しいペアであるか確認（入れ子やクロスを簡易防止）
        if BRACKETS.get(open_b) == close_b:
            # 表示できない空白（不可視文字）を除去
            optimized_content = INVISIBLE_SPACES_RE.sub("", content)
            return f"{open_b}{optimized_content}{close_b}"
        return match.group(0)

    text = BRACKET_PATTERN.sub(_replace_bracket_content, text)

    # 2. 括弧外の最適化（括弧前後に文字があれば半角空白を1つ挿入）
    # 左括弧の前に文字がある場合（ただし空白や他の左括弧は除く）
    text = re.sub(
        f"([^\\s{_left_brackets}])([{_left_brackets}])", r"\1 \2", text
    )

    # 右括弧の後に文字がある場合（ただし空白や他の右括弧は除く）
    text = re.sub(
        f"([{_right_brackets}])([^\\s{_right_brackets}])", r"\1 \2", text
    )

    # 既存の空白と重複して連続した半角空白が生まれた場合の調整
    text = re.sub(f" +([{_left_brackets}])", r" \1", text)
    text = re.sub(f"([{_right_brackets}]) +", r"\1 ", text)

    return text


OPEN_BRACKET_PATTERN = re.compile(r"『")
CLOSE_BRACKET_PATTERN = re.compile(r"』")


def norm_brackets(text: str) -> str:
    """文字列内の全角二重括弧『』を全角括弧「」に正規化します。

    Args:
        text: 置換対象の文字列。

    Returns:
        『』が「」に置換された文字列。
    """
    text = OPEN_BRACKET_PATTERN.sub("「", text)
    text = CLOSE_BRACKET_PATTERN.sub("」", text)
    return text
