from anthropic import Anthropic
from secret import anthropic_api_key

client = Anthropic(api_key=anthropic_api_key)


def ask_claude(prompt: str) -> str:
    return (
        client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-5-sonnet-latest",
        )
        .content[0]
        .text
    )


if __name__ == "__main__":
    print(ask_claude("Hi there, are you fishing?"))
