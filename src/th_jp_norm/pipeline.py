#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""利用者ごとにカスタマイズ可能な正規化パイプラインクラスを提供するモジュール。"""

from collections.abc import Callable
from typing import Self


class NormalizationPipeline:
    """正規化処理のステップを動的に構築・変更・実行するためのパイプラインクラス。

    利用者が独自の処理や既存のプリミティブ関数を追加・削除・入れ替えを行い、
    専用のパイプラインを柔軟に構築できるようにします。
    """

    def __init__(
        self, steps: list[Callable[[str], str]] | None = None
    ) -> None:
        """パイプラインを初期化します。

        Args:
            steps: 初期登録する処理関数のリスト。省略した場合は空のパイプライン。
        """
        self._steps: list[Callable[[str], str]] = list(steps) if steps else []

    @property
    def steps(self) -> list[Callable[[str], str]]:
        """登録されている正規化ステップのリストを返します。

        Returns:
            登録順の処理関数リスト。返されたリストの変更はパイプラインに反映されます。
        """
        return self._steps

    def add_step(self, func: Callable[[str], str]) -> Self:
        """パイプラインの末尾に新しい正規化ステップを追加します。

        Args:
            func: 文字列を受け取り文字列を返す処理関数。

        Returns:
            メソッドチェイン用の自分自身のインスタンス。
        """
        self._steps.append(func)
        return self

    def insert_step(self, index: int, func: Callable[[str], str]) -> Self:
        """指定したインデックスの位置に新しい正規化ステップを挿入します。

        Args:
            index: 挿入する位置のインデックス。
            func: 文字列を受け取り文字列を返す処理関数。

        Returns:
            メソッドチェイン用の自分自身のインスタンス。
        """
        self._steps.insert(index, func)
        return self

    def remove_step(self, index: int) -> Self:
        """指定したインデックスの正規化ステップを削除します。

        Args:
            index: 削除するステップのインデックス。範囲外の場合は何も削除しません。

        Returns:
            メソッドチェイン用の自分自身のインスタンス。
        """
        if 0 <= index < len(self._steps):
            self._steps.pop(index)
        return self

    def swap_steps(self, index1: int, index2: int) -> Self:
        """指定した2つのインデックスの正規化ステップの位置を入れ替えます。

        Args:
            index1: 入れ替える一方のインデックス。
            index2: 入れ替える他方のインデックス。

        Returns:
            両インデックスが範囲内の場合に入れ替えた自分自身のインスタンス。
        """
        if 0 <= index1 < len(self._steps) and 0 <= index2 < len(self._steps):
            self._steps[index1], self._steps[index2] = (
                self._steps[index2],
                self._steps[index1],
            )
        return self

    def execute(self, text: str) -> str:
        """登録されたすべての正規化ステップを順番に実行します。

        Args:
            text: 処理対象の文字列。

        Returns:
            登録されたすべての処理を順に適用した文字列。
        """
        current_text = text
        for step in self._steps:
            current_text = step(current_text)
        return current_text
