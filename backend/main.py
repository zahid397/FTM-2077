import os
import random
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
from dotenv import load_dotenv

# =====================================================
# 1. CONFIG & SETUP
# =====================================================
load_dotenv() # Load .env file for local dev

PROJECT_NAME = "FTM-2077 OMEGA"
VERSION = "3.1.0 (SENTIENT)"
API_PREFIX = "/api"

app = FastAPI(title=PROJECT_NAME, version=VERSION)

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# 2. GEMINI NEURAL LINK
# =====================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = None

if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
        # Using 1.5-flash for speed
        GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ [NEURAL ENGINE] CONNECTED TO GEMINI CLOUD")
    except Exception as e:
        print(f"⚠️ [NEURAL ENGINE] CONNECTION FAILED: {e}")
else:
    print("⚠️ [SYSTEM] RUNNING ON LOCAL BACKUP POWER (OFFLINE MODE)")

# =====================================================
# 3. SMART FALLBACK (LOCAL BRAIN)
# =====================================================
def get_fallback_response(cmd, persona):
    """Generates smart responses when Gemini is offline"""
    cmd = cmd.lower()
    
    # Jarvis Style Responses
    if any(x in cmd for x in ['hi', 'hello', 'wake up']):
        return f"Greetings. {persona} systems online. Ready for directives."
    
    if 'status' in cmd or 'how are you' in cmd:
        return "Systems operational. Running on backup power. Efficiency at 98%."
    
    if 'who are you' in cmd:
        return f"I am {persona}, an advanced AI operating on the FTM-2077 framework."
    
    # The Iron Man Question
    if 'quantum' in cmd or 'iron man' in cmd:
        return (
            "Here's the situation. Standard computers deal in bits—zeros and ones. "
            "Quantum computing deals in qubits. It's like analyzing 14 million outcomes "
            "in a single nanosecond. That's how I think."
        )

    # Generic Cool Responses
    return random.choice([
        "Processing command... Done. Protocols updated.",
        "Analyzing input... Secure connection established.",
        "Command acknowledged. Running background diagnostics.",
        "Input received. Systems holding steady.",
        "Calculations complete. Awaiting further instructions."
    ])

# =====================================================
# 4. API ENDPOINTS
# =====================================================
@app.get("/")
def root():
    return {"status": "ONLINE", "system": PROJECT_NAME, "version": VERSION}

@app.post(f"{API_PREFIX}/execute")
async def execute(payload: dict):
    cmd = payload.get("command", "").strip()
    persona = payload.get("persona", "JARVIS").upper()

    if not cmd:
        return JSONResponse(status_code=400, content={"text": "⚠️ Input stream empty."})

    # --- SYSTEM INSTRUCTION (Make it act like JARVIS) ---
    system_prompt = (
        f"You are {persona}, an advanced AI OS. "
        "Tone: Cool, Tactical, Concise (max 2 sentences). "
        "Do NOT act like a generic AI. You are a military-grade assistant. "
        "If asked 'how are you', say 'Systems nominal'."
    )

    # --- TRY REAL AI (GEMINI) ---
    if GEMINI_MODEL:
        try:
            # Async call for better performance
            response = await GEMINI_MODEL.generate_content_async(
                f"{system_prompt}\n\nUSER COMMAND: {cmd}\nRESPONSE:"
            )
            
            if response.text:
                return {"text": response.text.strip()}
        
        except Exception as e:
            print(f"❌ Gemini Error: {e}")
            # Fallback will trigger below

    # --- FALLBACK (OFFLINE/ERROR) ---
    # This runs if Gemini is missing OR fails
    fallback_text = get_fallback_response(cmd, persona)
    return {"text": fallback_text}
    
