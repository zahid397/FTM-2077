import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai

# -----------------------
# CONFIG
# -----------------------
PROJECT_NAME = "FTM-2077 OMEGA"
VERSION = "2.0.77"
API_PREFIX = "/api"

# 🔑 Gemini API Key (Vercel / Render env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# -----------------------
# FASTAPI INIT
# -----------------------
app = FastAPI(title=PROJECT_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# REQUEST MODEL
# -----------------------
class MissionRequest(BaseModel):
    command: str
    persona: str = "JARVIS"

# -----------------------
# ROOT
# -----------------------
@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "project": PROJECT_NAME,
        "version": VERSION
    }

# -----------------------
# CORE EXECUTE (REAL ANSWER)
# -----------------------
@app.post(f"{API_PREFIX}/execute")
def execute(payload: MissionRequest):
    cmd = payload.command.strip()
    persona = payload.persona.upper()

    if not cmd:
        return JSONResponse(
            status_code=400,
            content={"error": "Command cannot be empty"}
        )

    system_prompt = f"""
You are {persona}.
Respond like a real intelligent system.
No logs, no brackets, no system messages.
Answer directly like a human.
"""

    try:
        response = model.generate_content(
            system_prompt + "\nUser: " + cmd
        )

        return {
            "status": "SUCCESS",
            "persona": persona,
            "text": response.text
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }

# -----------------------
# HEALTH
# -----------------------
@app.get("/health")
def health():
    return {"status": "OK"}

# -----------------------
# LOCAL RUN
# -----------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
