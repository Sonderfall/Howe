from llama_cpp import Llama


def think():
    llm = Llama(model_path="models/llama-2-7b.gguf", chat_format="llama-2")

    output = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant who perfectly describes images.",
            },
            {"role": "user", "content": "Describe this image in detail please."},
        ]
    )

    print(output)


if __name__ == "__main__":
    think()
