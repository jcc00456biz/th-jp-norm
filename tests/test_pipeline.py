import pytest

from th_jp_norm import NormalizationPipeline, execute_pipeline, execute_pipeline2
from th_jp_norm.primitive.alpha import alpha_to_half
from th_jp_norm.primitive.numerals import numerals_to_half


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ＡＢＣ（００１）", "ABC1"),
        ("ｶﾞｯﾂﾎﾟｰｽﾞ", "ガッツポーズ"),
        ("Book（上巻）", "Book（上巻）"),
        ("名前００２", "名前2"),
        ("a/b:c", "a／b：c"),
        ("  Ａ Ｂ  ", "A_B"),
        ("", ""),
    ],
)
def test_execute_pipeline(text: str, expected: str) -> None:
    assert execute_pipeline(text) == expected


def test_execute_pipeline2_preserves_parenthesized_number_and_leading_zero() -> None:
    assert execute_pipeline2("ＡＢＣ（００１）") == "ABC（001）"


def test_execute_pipeline2_normalizes_half_width_kana() -> None:
    assert execute_pipeline2("ｶﾞｯﾂﾎﾟｰｽﾞ") == "ガッツポーズ"


def test_normalization_pipeline_executes_steps_in_order() -> None:
    pipeline = NormalizationPipeline([alpha_to_half, numerals_to_half])

    assert pipeline.execute("ＡＢＣ１２３") == "ABC123"


def test_normalization_pipeline_mutations_are_chainable() -> None:
    pipeline = NormalizationPipeline([str.strip])
    assert pipeline.add_step(str.upper) is pipeline
    assert pipeline.insert_step(0, lambda text: f" {text} ") is pipeline
    assert pipeline.execute("hello") == "HELLO"

    assert pipeline.swap_steps(0, 1) is pipeline
    assert pipeline.remove_step(0) is pipeline
    assert pipeline.execute(" hello ") == "  HELLO  "


def test_normalization_pipeline_ignores_out_of_range_mutations() -> None:
    pipeline = NormalizationPipeline([str.upper])

    assert pipeline.remove_step(1) is pipeline
    assert pipeline.swap_steps(0, 1) is pipeline
    assert pipeline.execute("hello") == "HELLO"


def test_normalization_pipeline_copies_initial_step_list() -> None:
    steps = [str.upper]
    pipeline = NormalizationPipeline(steps)
    steps.clear()

    assert pipeline.execute("hello") == "HELLO"


def test_normalization_pipeline_propagates_step_errors() -> None:
    def fail(_: str) -> str:
        raise RuntimeError("normalization failed")

    with pytest.raises(RuntimeError, match="normalization failed"):
        NormalizationPipeline([fail]).execute("text")
