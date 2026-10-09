from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from chat import chat_ai, ChatPayload

app = FastAPI(title="twinAPI", version="0.1.0")

origins = [
    "http://localhost:5173",
    "https://twinchat-pearl.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/chat", response_model= dict)
async def chatPost(payload: ChatPayload):
    result =  chat_ai(payload.message, payload.history)
    response = {}
    response["message"] = result
    return response



def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

