from fastapi import FastAPI
import uvicorn
import os
from chat import chat_ai, ChatPayload

app = FastAPI(title="twinAPI", version="0.1.0")


@app.get("/")
async def home():
    return {"message": "Welcome to twinAPI!", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/chat/{message}")
async def chat(message):
    result =  chat_ai(message, [])
    return result

@app.post("/chat")
async def chatPost(payload: ChatPayload):
    result =  chat_ai(payload.message, payload.history)
    return result



def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

