from anthropic import Anthropic
from sefaria_translation.secret import anthropic_api_key

client = Anthropic(api_key=anthropic_api_key)


def ask_claude(prompt: str) -> str:
    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-5-sonnet-latest",
    ).content[0]

    if not hasattr(response, "text") or not isinstance(response.text, str):
        raise ValueError(
            "Claude response missing text property or text is not a string"
        )
    else:
        return response.text


if __name__ == "__main__":
    print(ask_claude("Hi there, are you fishing?"))
