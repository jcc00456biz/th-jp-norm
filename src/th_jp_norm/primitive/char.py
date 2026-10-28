#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文字の全角化や結合処理を行うプリミティブモジュール。"""

import re
import unicodedata

# 2文字構成の半角カタカナ（濁点・半濁点付き）から全角へのマッピング
# fmt: off
H2Z_KANA_VOICED_MAP = {
    "ｶﾞ": "ガ", "ｷﾞ": "ギ", "ｸﾞ": "グ", "ｹﾞ": "ゲ", "ｺﾞ": "ゴ",
    "ｻﾞ": "ザ", "ｼﾞ": "ジ", "ｽﾞ": "ズ", "ｾﾞ": "ゼ", "ｿﾞ": "ゾ",
    "ﾀﾞ": "ダ", "ﾁﾞ": "ヂ", "ﾂﾞ": "ヅ", "ﾃﾞ": "デ", "ﾄﾞ": "ド",
    "ﾊﾞ": "バ", "ﾋﾞ": "ビ", "ﾌﾞ": "ブ", "ﾍﾞ": "ベ", "ﾎﾞ": "ボ",
    "ﾊﾟ": "パ", "ﾋﾟ": "ピ", "ﾌﾟ": "プ", "ﾍﾟ": "ペ", "ﾎﾟ": "ポ",
    "ｳﾞ": "ヴ",
}
# fmt: on

# 1文字の半角カタカナ・カナ記号のみのマッピング（括弧は含まない）
# fmt: off
H2Z_KANA_SINGLE_MAP = {
    0xFF61: "。", 0xFF62: "「", 0xFF63: "」", 0xFF64: "、", 0xFF65: "・",
    0xFF66: "ヲ", 0xFF67: "ァ", 0xFF68: "ィ", 0xFF69: "ゥ", 0xFF6A: "ェ",
    0xFF6B: "ォ", 0xFF6C: "ャ", 0xFF6D: "ュ", 0xFF6E: "ョ", 0xFF6F: "ッ",
    0xFF70: "ー", 0xFF71: "ア", 0xFF72: "イ", 0xFF73: "ウ", 0xFF74: "エ",
    0xFF75: "オ", 0xFF76: "カ", 0xFF77: "キ", 0xFF78: "ク", 0xFF79: "ケ",
    0xFF7A: "コ", 0xFF7B: "サ", 0xFF7C: "シ", 0xFF7D: "ス", 0xFF7E: "セ",
    0xFF7F: "ソ", 0xFF80: "タ", 0xFF81: "チ", 0xFF82: "ツ", 0xFF83: "テ",
    0xFF84: "ト", 0xFF85: "ナ", 0xFF86: "ニ", 0xFF87: "ヌ", 0xFF88: "ネ",
    0xFF89: "ノ", 0xFF8A: "ハ", 0xFF8B: "ヒ", 0xFF8C: "フ", 0xFF8D: "ヘ",
    0xFF8E: "ホ", 0xFF8F: "マ", 0xFF90: "ミ", 0xFF91: "ム", 0xFF92: "メ",
    0xFF93: "モ", 0xFF94: "ヤ", 0xFF95: "ユ", 0xFF96: "ヨ", 0xFF97: "ラ",
    0xFF98: "リ", 0xFF99: "ル", 0xFF9A: "レ", 0xFF9B: "ロ", 0xFF9C: "ワ",
    0xFF9D: "ン", 0xFF9E: "゛", 0xFF9F: "゜",
}
# fmt: on


def fuse_kana(text: str) -> str:
    """結合文字を合成済み文字へ正規化します。

    Args:
        text: 正規化対象の文字列。

    Returns:
        Unicode NFC 形式に正規化した文字列。
    """
    return unicodedata.normalize("NFC", text)


def kana_half_to_full(text: str) -> str:
    """半角カタカナおよびカナ記号を全角に正規化します。

    Args:
        text: 変換対象の文字列。

    Returns:
        半角カタカナとカナ記号を全角に変換した文字列。
    """
    for half_combo, full_char in H2Z_KANA_VOICED_MAP.items():
        text = text.replace(half_combo, full_char)
    return text.translate(H2Z_KANA_SINGLE_MAP)


def norm_prolonged(text: str) -> str:
    """長音符に似た文字を長音符（U+30FC）に正規化します。

    Args:
        text: 正規化対象の文字列。

    Returns:
        対象の罫線・ダッシュ類を長音符に置換した文字列。
    """
    targets = r"[\u2010\u2011\u2013\u2014\u2015\u2500]"
    return re.sub(targets, "\u30fc", text)


def norm_rd(text: str) -> str:
    """連続する三点リーダーまたは中黒を中黒3文字に統一します。

    Args:
        text: 正規化対象の文字列。

    Returns:
        連続する対象記号を中黒3文字に置換した文字列。
    """
    pattern = r"[…⋯]{1,}|・{2,}"
    target = "・" * 3
    return re.sub(pattern, target, text)


def rm_br_wave_dash(text: str) -> str:
    """「～」または「―」で括られた部分を削除します。
    各種波ダッシュ（U+FF5E, U+301C）に対応しています。

    Args:
        text: 波ダッシュで囲まれた部分を含む文字列。

    Returns:
        対応する波ダッシュのペアと、その間の文字列を削除した文字列。
    """
    # 0xFF5E (全角チルダ) と 0x301C (波ダッシュ) の両方を許容する文字クラス
    wave_dash = f"[{chr(0xFF5E)}{chr(0x301C)}]"

    # 各パターンを組み立て
    patterns = [
        f"{wave_dash}.*?{wave_dash}",
    ]
    combined_pattern = "|".join(patterns)

    return re.sub(combined_pattern, "", text)


def to_safe_win(text: str) -> str:
    """Windowsでファイル名に使えない記号などを全角化します。

    Args:
        text: 変換対象の文字列。

    Returns:
        禁止記号などを全角化した文字列。
    """
    # 0x203C (2連感嘆符) と 0xFE0E (異体字セレクタ)
    double_excl = chr(0x203C)
    var_selector = chr(0xFE0E)

    translation_table: dict[str | int, str] = {
        "\\": "￥",
        "/": "／",
        ":": "：",
        ";": "；",
        ",": "，",
        "*": "＊",
        "?": "？",
        '"': "”",
        "<": "＜",
        ">": "＞",
        "|": "｜",
        "!": "！",
        "&": "＆",
        "%": "％",
        "+": "＋",
        "=": "＝",
        "♡": "",
        "♥": "",
        # 1文字の2連感嘆符を置換
        0x203C: "！！",
        0x2048: "？！",
        0x2049: "！？",
    }
    translation = str.maketrans(translation_table)

    # 異体字セレクタ付きの2文字の組み合わせ（"‼︎"）を先に置換してから全体を翻訳
    # ※ str.maketrans のキーにはマルチ文字（2文字以上の文字列）の数値を指定できないため
    text = text.replace(f"{double_excl}{var_selector}", "！！")

    return text.translate(translation)
