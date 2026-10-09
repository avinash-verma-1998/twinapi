import os
from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from dotenv import load_dotenv
from pydantic import BaseModel


class ChatPayload(BaseModel):
    message: str
    history: list[dict] = []

load_dotenv(override=True)

MODEL_NAME = "gemini-3.5-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

google_api_key = os.getenv('GOOGLE_API_KEY')
gemini = OpenAI(api_key=google_api_key, base_url=GEMINI_BASE_URL)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat_ai(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = gemini.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = gemini.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content



