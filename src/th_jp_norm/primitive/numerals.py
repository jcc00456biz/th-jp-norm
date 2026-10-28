#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数値に関する正規化処理を行うプリミティブモジュール。"""

import re

# 全角アラビア数字（０〜９）→ 半角（0〜9）への置換用マッピング
# Unicodeコードポイントを直接指定する箇所は16進数リテラルを使用
# fmt: off
Z2H_DIGIT_TRANSLATION: dict[int, int] = {
    code: code - 0xFEE0 for code in range(0xFF10, 0xFF1A)
}
# fmt: on


def numerals_to_half(text: str) -> str:
    """全角数字を半角に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        全角数字を半角に変換した文字列。
    """
    return text.translate(Z2H_DIGIT_TRANSLATION)


# 漢数字（零〜九）→ アラビア数字
# fmt: off
KANJI_DIGIT_TRANSLATION: dict[int, str] = str.maketrans({
    "零": "0", "一": "1", "二": "2", "三": "3", "四": "4",
    "五": "5", "六": "6", "七": "7", "八": "8", "九": "9",
})
# fmt: on


def kan_to_num(text: str) -> str:
    """漢数字（零〜九）をアラビア数字に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        漢数字をアラビア数字に置換した文字列。
    """
    return text.translate(KANJI_DIGIT_TRANSLATION)


# 大字（壱〜萬）→ アラビア数字
# fmt: off
DAIJI_DIGIT_TRANSLATION: dict[int, str] = str.maketrans({
    "零": "0",
    "壱": "1", "弐": "2", "参": "3",
    "肆": "4", "伍": "5", "陸": "6",
    "漆": "7", "捌": "8", "玖": "9",
    "拾": "10", "佰": "100", "仟": "1000", "萬": "10000",
})
# fmt: on


def dai_to_num(text: str) -> str:
    """大字をアラビア数字に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        大字をアラビア数字に置換した文字列。
    """
    return text.translate(DAIJI_DIGIT_TRANSLATION)


# 全角ローマ数字（Ⅰ〜Ⅻ）→ 半角アラビア数字（1〜12）
# fmt: off
FULLWIDTH_ROMAN_TRANSLATION: dict[int, str] = str.maketrans({
    "Ⅰ": "1", "Ⅱ": "2", "Ⅲ": "3", "Ⅳ": "4", "Ⅴ": "5",
    "Ⅵ": "6", "Ⅶ": "7", "Ⅷ": "8", "Ⅸ": "9", "Ⅹ": "10",
    "Ⅺ": "11", "Ⅻ": "12",
})
# fmt: on


def rom_to_num(text: str) -> str:
    """全角ローマ数字（Ⅰ〜Ⅻ）をアラビア数字に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        全角ローマ数字をアラビア数字に置換した文字列。
    """
    return text.translate(FULLWIDTH_ROMAN_TRANSLATION)


# parse_kanji_number 内の変換辞書は不変の定数として関数外に抽出し、
# 呼び出しごとの初期化オーバーヘッドを削減
# fmt: off
KANJI_VALS: dict[str, int] = {
    "〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
    "壱": 1, "弐": 2, "参": 3, "肆": 4, "伍": 5,
    "陸": 6, "漆": 7, "捌": 8, "玖": 9,
}

SUB_UNITS: dict[str, int] = {
    "十": 10, "拾": 10, "百": 100, "佰": 100, "千": 1000, "仟": 1000,
}

MAIN_UNITS: dict[str, int] = {
    "万": 10000, "萬": 10000,
}
# fmt: on


# 漢数字・大字・位取り文字の集合を高速探索用にセット（set）化
KANJI_SET = set(
    "〇零一二三四五六七八九" "壱弐参肆伍陸漆捌玖拾佰仟萬" "十百千万"
)


def parse_kanji_number(text: str) -> str:
    """位取りを含む漢数字・大字をアラビア数字の文字列に変換します。

    Args:
        text: 変換対象の漢数字を含む文字列。

    Returns:
        数値として解釈できる場合はアラビア数字、解釈できない場合は入力文字列。
    """
    if not text or text.isdigit():
        return text

    # 【高速化ガード】漢数字関連の文字が1文字も含まれていなければ即時リターン
    # 集合の交差判定（any）は C言語レイヤーで走るため、Pythonのforループを回すより圧倒的に高速です
    if not any(char in KANJI_SET for char in text):
        return text

    total = 0
    current_section = 0
    current_number = 0
    has_digit = False

    for char in text:
        if char in KANJI_VALS:
            current_number = current_number * 10 + KANJI_VALS[char]
            has_digit = True
        elif char in SUB_UNITS:
            val = current_number if has_digit else 1
            current_section += val * SUB_UNITS[char]
            current_number = 0
            has_digit = False
        elif char in MAIN_UNITS:
            if has_digit:
                current_section += current_number
            elif current_section == 0:
                current_section = 1
            total += current_section * MAIN_UNITS[char]
            current_section = 0
            current_number = 0
            has_digit = False
        else:
            return text

    current_section += current_number if has_digit else 0
    total += current_section

    return str(total)


# 不可視文字の正規表現パターン（文字列リテラル内はUnicodeエスケープを使用）
INV_CHARS = r"\s\u3000\u00A0\u2000-\u200F\x00-\x1F\x7F"

# 許容する数字関連文字
# fmt: off
NUM_CHARS = (
    r"\d"
    r"０-９"
    r"〇零一二三四五六七八九"
    r"壱弐参肆伍陸漆捌玖拾佰仟萬"
    r"十百千万"
)
# fmt: on

# 括弧のパターン定義をコンパイルしてキャッシュ（パフォーマンス向上）
BR_NUM_PATTERN = re.compile(rf"[(\[（［]([{NUM_CHARS}{INV_CHARS}]+)[)\]）］]")

# サブレス処理用のコンパイル済み正規表現
# 冗長な先頭の0のみを対象とし、0単体や0.5などの0は残す
SUBLESS_PATTERN = re.compile(r"^0+(?=\d)")


def norm_br_num(text: str) -> str:
    """括弧に囲まれた数字を半角数字に正規化し、括弧を外します。

    対象：アラビア数字（半角・全角）、漢数字（零〜九、十、百、万など）、大字
    括弧内に上記対象の数字、空白、表示できない不可視文字以外が
    1文字でも含まれる場合（例:「第」や「建物」など）は一切置換しません。
    表示できない文字（空白・制御文字等）は、無いものとして扱います。

    Args:
        text: 括弧内の数字を正規化する文字列。

    Returns:
        数字だけで構成された括弧部分を正規化して括弧を外した文字列。
    """

    def _clean(match: re.Match) -> str:
        """括弧内の数字を正規化し、必要に応じて括弧を外します。

        Args:
            match: 括弧と中の数字に一致した正規表現の結果。

        Returns:
            正規化した数字、または変換しない場合の元の括弧表現。
        """
        inner = match.group(1)

        # 1. 表示できない不可視文字（空白・制御文字等）を完全に除去
        inner = re.sub(rf"[{INV_CHARS}]", "", inner)

        # 2. 全角アラビア数字をあらかじめ半角に
        inner = numerals_to_half(inner)

        # 3. 漢数字・大字の位取りパース
        inner = parse_kanji_number(inner)

        # 4. 数字が1文字も含まれていない場合は変換しない
        if not inner or not inner.isdigit():
            return match.group(0)

        # 5. 整数部の先頭にある冗長な0をサブレスする
        if len(inner) > 1:
            inner = inner.lstrip("0")
            if not inner:
                inner = "0"

        return inner

    return BR_NUM_PATTERN.sub(_clean, text)


# 抽出用パターンを拡張
# 漢数字も対象に含めるため、文字クラスを定義
KANJI_DIGITS = r"〇零一二三四五六七八九壱弐参肆伍陸漆捌玖拾佰仟萬十百千万"
NUM_OR_KANJI = rf"(?:\d+(?:\.\d+)?|[{KANJI_DIGITS}]+)"

# パターン定義の整理と強化
# 1. Vol系: Vol.123, vol 123 など
VOLUME_VOL_PATTERN = re.compile(rf"(?i)Vol\.?\s*{NUM_OR_KANJI}")

# 2. その他（巻・話）: 1巻, 第1話, 一巻, 第壱話 など
# 接頭辞「第」の有無と、数字、単位を組み合わせる
VOLUME_SUFFIX_PATTERN = re.compile(rf"(?:第\s*)?{NUM_OR_KANJI}\s*(?:巻|話)")


def rm_volume_suffix(text: str) -> str:
    """巻数・話数の接頭辞や接尾辞を除去し、数値を正規化します。

    Args:
        text: 巻数・話数を含む文字列。

    Returns:
        「Vol.」「第」「巻」「話」を除去し、数値を正規化した文字列。
    """

    def _clean_match(match: re.Match[str]) -> str:
        """一致した巻数・話数表現から数値を取り出して正規化します。

        Args:
            match: 巻数・話数の表現に一致した正規表現の結果。

        Returns:
            接頭辞・接尾辞を除去して数値を正規化した文字列。
        """
        # マッチした文字列から数値部分のみを抜き出す
        # Vol.等の接頭辞や巻・話の接尾辞を除去
        content = match.group(0)

        # 漢数字・アラビア数字・全角数字の正規化
        # 1. 単位文字を取り除く
        cleaned = re.sub(r"[第巻話Vol\.  ]", "", content, flags=re.IGNORECASE)

        # 2. 漢数字をアラビア数字に変換
        val = parse_kanji_number(numerals_to_half(cleaned))

        # 3. 先頭の不要な0を削除（正規表現で01->1等）
        return SUBLESS_PATTERN.sub("", val)

    # 順次置換を適用
    text = VOLUME_VOL_PATTERN.sub(_clean_match, text)
    text = VOLUME_SUFFIX_PATTERN.sub(_clean_match, text)

    return text


# 丸数字（①〜⑳）→ 半角数字（1〜20）への置換用マッピング
# 辞書のキー自体を最初からint型で定義することで、ord()による変換を不要にします
# fmt: off
CIRCLED_NUMBER_TRANSLATION: dict[int, str] = {
    0x2460: "1", 0x2461: "2", 0x2462: "3", 0x2463: "4", 0x2464: "5",
    0x2465: "6", 0x2466: "7", 0x2467: "8", 0x2468: "9", 0x2469: "10",
    0x246A: "11", 0x246B: "12", 0x246C: "13", 0x246D: "14", 0x246E: "15",
    0x246F: "16", 0x2470: "17", 0x2471: "18", 0x2472: "19", 0x2473: "20",
}
# fmt: on


def circled_to_num(text: str) -> str:
    """丸数字（①〜⑳）を半角数字に変換します。

    Args:
        text: 変換対象の文字列。

    Returns:
        丸数字を半角数字に置換した文字列。
    """
    return text.translate(CIRCLED_NUMBER_TRANSLATION)


# numerals.py

# 1. 全角・半角ローマ数字を網羅するパターン
# 半角は I, V, X, L, C, D, M を使用。末尾以外にマッチしないよう \b (境界) を使用
# 誤爆を防ぐため、半角ローマ数字は少なくとも1文字以上、かつ英字のみで構成される場合を対象とします
# fmt: off
TRAILING_ROMAN_PATTERN = re.compile(
    r"(?:"
    r"[Ⅰ-Ⅻ]+"  # 全角ローマ数字
    r"|"
    r"\b[IVXLCDM]+\b"  # 半角ローマ数字（境界指定あり）
    r")$"
)
# fmt: on


def norm_trailing_roman(text: str) -> str:
    """末尾のローマ数字をアラビア数字に変換します。

    Args:
        text: 末尾にローマ数字を含む文字列。

    Returns:
        末尾の全角または半角ローマ数字を変換した文字列。
    """
    if not text:
        return text

    # 1. 全角ローマ数字の処理
    if match := re.search(r"[Ⅰ-Ⅻ]+$", text):
        return text[: match.start()] + match.group(0).translate(
            FULLWIDTH_ROMAN_TRANSLATION
        )

    # 2. 半角ローマ数字の処理
    # 末尾のアルファベットのみを抽出
    if match := re.search(r"([A-Za-z]+)$", text):
        alpha_part = match.group(1)
        # すべてがローマ数字文字であるか確認
        if all(c.upper() in "IVXLCDM" for c in alpha_part):
            # 変換して置換
            arabic_str = _roman_to_int_str(alpha_part)
            return text[: match.start()] + arabic_str

    return text


def _roman_to_int_str(s: str) -> str:
    """半角ローマ数字を数値文字列に変換します。

    Args:
        s: 半角ローマ数字。

    Returns:
        ローマ数字を整数に換算した文字列。
    """
    s = s.upper()  # ここで確実に大文字化
    mapping = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    val = 0
    i = 0
    while i < len(s):
        curr = mapping.get(s[i], 0)
        # 次の文字が存在し、かつ現在の値より大きい場合は減算則（IV等）
        if i + 1 < len(s):
            next_val = mapping.get(s[i + 1], 0)
            if curr < next_val:
                val += next_val - curr
                i += 2
                continue
        val += curr
        i += 1
    return str(val)


# 末尾の漢数字・大字にマッチするパターン
# 1文字以上の漢数字が文字列の最後にある場合
TRAILING_KANJI_PATTERN = re.compile(rf"([{KANJI_DIGITS}]+)$")


def norm_trailing_kanji(text: str) -> str:
    """末尾の漢数字・大字をアラビア数字に変換します。

    Args:
        text: 末尾に漢数字または大字を含む文字列。

    Returns:
        数値として解釈できる末尾の漢数字をアラビア数字にした文字列。
    """
    if not text:
        return text

    if match := TRAILING_KANJI_PATTERN.search(text):
        kanji_part = match.group(1)
        # 漢数字を数値文字列に変換
        arabic_str = parse_kanji_number(kanji_part)

        # 変換できた場合のみ置換（変換不能な文字列でないことを確認）
        if arabic_str != kanji_part:
            return text[: match.start()] + arabic_str

    return text
