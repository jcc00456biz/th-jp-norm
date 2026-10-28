#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基本的な文字列の正規化処理（プリミティブ関数群）を提供するパッケージ。"""

"""日本語文字列の正規化に使うプリミティブ関数を提供します。"""

from .alpha import alpha_to_full, alpha_to_half, sp_to_underscore
from .char import (
    fuse_kana,
    kana_half_to_full,
    norm_prolonged,
    norm_rd,
    rm_br_wave_dash,
    to_safe_win,
)
from .numerals import (
    dai_to_num,
    kan_to_num,
    norm_br_num,
    rom_to_num,
    circled_to_num,
    norm_trailing_roman,
    norm_trailing_kanji,
)
from .numerals import numerals_to_half
from .spaces import clps_sp, rm_sp
from .symbols import (
    brackets_to_half,
    parentheses_to_full,
    optimize_brackets,
    norm_brackets,
)

__all__ = [
    "rm_sp",
    "clps_sp",
    "alpha_to_half",
    "alpha_to_full",
    "sp_to_underscore",
    "fuse_kana",
    "kana_half_to_full",
    "norm_prolonged",
    "norm_rd",
    "rm_br_wave_dash",
    "to_safe_win",
    "numerals_to_half",
    "kan_to_num",
    "dai_to_num",
    "rom_to_num",
    "norm_br_num",
    "circled_to_num",
    "norm_trailing_roman",
    "norm_trailing_kanji",
    "brackets_to_half",
    "parentheses_to_full",
    "optimize_brackets",
    "norm_brackets",
]
