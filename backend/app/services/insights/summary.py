from app.services.llm.qwen import call_qwen
from app.services.llm.prompts import build_summary_prompt


def generate_comparison_summary(

    metadata_a,
    metadata_b,

    hook_comparison,

    cta_a,
    cta_b,

    speech_a,
    speech_b
):

    prompt = build_summary_prompt(

        metadata_a,
        metadata_b,

        hook_comparison,

        cta_a,
        cta_b,

        speech_a,
        speech_b
    )

    return call_qwen(prompt)