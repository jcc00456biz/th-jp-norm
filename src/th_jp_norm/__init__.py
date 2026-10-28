#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日本語文字列の正規化機能を提供するパッケージ。"""

from .norm_pipeline import execute_pipeline, execute_pipeline2
from .pipeline import NormalizationPipeline
from .primitive.spaces import rm_sp
from .primitive.symbols import optimize_brackets
from .primitive.numerals import norm_trailing_roman, norm_trailing_kanji

__all__ = [
    "execute_pipeline",
    "execute_pipeline2",
    "NormalizationPipeline",
    "rm_sp",
    "optimize_brackets",
    "norm_trailing_roman",
    "norm_trailing_kanji",
]
