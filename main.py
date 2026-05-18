from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from groq import Groq
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are DevBot, an expert AI coding assistant. You help developers with:
- Explaining code and concepts clearly
- Debugging errors and fixing bugs
- Code reviews and best practices
- Algorithms, data structures, and system design
Be concise and practical."""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages
    )
    reply = response.choices[0].message.content
    return JSONResponse({"reply": reply})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
