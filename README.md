# th-jp-norm

日本語テキストの表記ゆれを整えるための、依存ライブラリ不要の文字列正規化パッケージです。
全角・半角、カタカナ、数字、括弧、空白などの正規化関数と、標準パイプラインを提供します。

## インストール

```shell
pip install th-jp-norm
```

## 使い方

```python
from th_jp_norm import NormalizationPipeline, execute_pipeline
from th_jp_norm.primitive import alpha_to_half, numerals_to_half

print(execute_pipeline("ＡＢＣ（００１）"))

pipeline = NormalizationPipeline([alpha_to_half, numerals_to_half])
print(pipeline.execute("ＡＢＣ１２３"))
```

## 主なAPI

- `execute_pipeline(text)`: 全角・半角、カタカナ、括弧内の数字、禁止記号、末尾の括弧・数字などを一括で正規化します。
- `execute_pipeline2(text)`: 標準的な文字・記号の正規化を行います。括弧内数字の正規化や末尾数字のゼロ除去は行いません。
- `NormalizationPipeline`: 正規化関数を追加・挿入・削除・並べ替えして独自の処理順を構成します。
- `th_jp_norm.primitive`: 個別の正規化関数を提供します。各関数の詳細はPythonのヘルプで確認できます。

## 動作環境

Python 3.14以降に対応しています。

## テスト

開発用依存関係をインストールし、テストを実行します。

```shell
python -m pip install -e ".[test]"
python -m pytest
```

## ライセンス

Apache License 2.0。詳細は [LICENSE](./LICENSE) を参照してください。
