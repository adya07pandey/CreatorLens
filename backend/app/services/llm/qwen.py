import os
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url=
        "https://openrouter.ai/api/v1"
)


def call_qwen(
    prompt,
    temperature=0.3
):

    start = time.perf_counter()

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=temperature
    )

    print(
        f"[LATENCY] Qwen generation: "
        f"{time.perf_counter()-start:.2f}s"
    )

    return (
        response
        .choices[0]
        .message
        .content
    )

def stream_qwen(
    prompt,
    temperature=0.3
):

    start = time.perf_counter()

    stream = client.chat.completions.create(
        model="qwen/qwen3-32b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=temperature,

        stream=True
    )

    first_token = False

    for chunk in stream:

        delta = (
            chunk
            .choices[0]
            .delta
            .content
        )

        if delta:

            if not first_token:

                print(
                    f"[LATENCY] First token: "
                    f"{time.perf_counter()-start:.2f}s"
                )

                first_token = True

            yield delta

    print(
        f"[LATENCY] Stream completed: "
        f"{time.perf_counter()-start:.2f}s"
    )