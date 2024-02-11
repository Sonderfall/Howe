from sqs import ThinkRequest, ThinkResponse

from typing import Dict, List, Optional
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    TextStreamer,
)

# __MODEL_NAME = "bofenghuang/vigogne-2-7b-chat"
# __REVISION = "v2.0"
__MODEL_NAME = "TheBloke/Vigostral-7B-Chat-GPTQ"
__REVISION = "gptq-4bit-32g-actorder_True"

__model = AutoModelForCausalLM.from_pretrained(
    __MODEL_NAME, revision=__REVISION, device_map="cuda:0"
)
__tokenizer = AutoTokenizer.from_pretrained(
    __MODEL_NAME, revision=__REVISION, use_fast=True
)
__streamer = TextStreamer(
    __tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True
)
__history = []


def think(request: ThinkRequest) -> ThinkResponse:
    response = __chat(
        query=request.utterance,
        temperature=request.temperature,
        max_new_tokens=request.max_len,
    )

    print(response)

    response = ThinkResponse(
        utterance=response, total_response_count=1, response_index=0
    )

    return response


def __chat(
    query: str,
    temperature: float = 0.7,
    top_p: float = 1.0,
    top_k: float = 0,
    repetition_penalty: float = 1.1,
    max_new_tokens: int = 256,
    **kwargs,
):
    global __history
    if __history is None:
        __history = []

    __history.append({"role": "user", "content": query})

    input_ids = __tokenizer.apply_chat_template(
        conversation=__history, add_generation_prompt=True, return_tensors="pt"
    ).to(__model.device)
    input_length = input_ids.shape[1]

    generated_outputs = __model.generate(
        input_ids=input_ids,
        generation_config=GenerationConfig(
            temperature=temperature,
            do_sample=temperature > 0.0,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_tokens,
            pad_token_id=__tokenizer.eos_token_id,
            **kwargs,
        ),
        streamer=__streamer,
        return_dict_in_generate=True,
    )

    generated_tokens = generated_outputs.sequences[0, input_length:]
    generated_text = __tokenizer.decode(generated_tokens, skip_special_tokens=True)

    __history.append({"role": "assistant", "content": generated_text})

    return generated_text


if __name__ == "__main__":
    print(
        think(
            ThinkRequest(
                utterance="Comment vas tu ?",
                temperature=1,
                max_len=512,
            )
        )
    )
