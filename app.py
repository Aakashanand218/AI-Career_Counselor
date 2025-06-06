# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key="AIzaSyBfasvVkK-gQ4sEcEeSXM_DytD05MvBK9U"  # 🔒 For testing only
    )
    default_prompt = ("You are a helpful career counselor. and provide me with career advice. "
    "with following skils and ans me questions about my career in one sentence. ")
    user_input = input("A helpful career counselor, please help me with my career: ")
    if not user_input:
        print("No input provided. Exiting.")
        return
    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=default_prompt+user_input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
