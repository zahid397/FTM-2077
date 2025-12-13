import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

# -----------------------
# CONFIGURATION
# -----------------------
PROJECT_NAME = "FTM-2077 OMEGA"
VERSION = "2.0.77"
API_PREFIX = "/api"

# Directory Setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# -----------------------
# FASTAPI INIT
# -----------------------
app = FastAPI(title=PROJECT_NAME, version=VERSION)

# CORS Middleware (To allow frontend connections)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# DATA MODELS
# -----------------------
class CommandRequest(BaseModel):
    command: str
    persona: Optional[str] = "JARVIS"

# -----------------------
# ROOT ENDPOINT
# -----------------------
@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "system": PROJECT_NAME,
        "version": VERSION,
        "mode": "ACTIVE"
    }

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/health")
def health():
    return {"status": "OK", "core_integrity": "100%"}

# -----------------------
# API EXECUTE (AI BRAIN)
# -----------------------
@app.post(f"{API_PREFIX}/execute")
def execute(payload: CommandRequest):
    cmd = payload.command.strip()
    persona = payload.persona.upper()

    if not cmd:
        return JSONResponse(
            status_code=400,
            content={"status": "ERROR", "reason": "Empty command sequence."}
        )

    clean_cmd = cmd.lower()

    # ---- LOGIC CORE (Simple Rules) ----
    response_text = ""

    if clean_cmd in ["hi", "hello", "wake up", "system on"]:
        response_text = f"Greetings. {persona} systems are fully operational. Ready for directives."
    
    elif clean_cmd in ["status", "report", "check systems"]:
        response_text = (
            f"[{persona} DIAGNOSTIC]\n"
            f"---------------------\n"
            f"CPU: OPTIMAL\n"
            f"MEMORY: STABLE\n"
            f"NETWORK: SECURE\n"
            f"THREAT LEVEL: 0%"
        )
    
    elif "who are you" in clean_cmd:
        response_text = f"I am {persona}, the central AI interface for Project FTM-2077."

    elif "thank" in clean_cmd:
        response_text = "You are welcome. Standing by."

    else:
        # Default fallback
        response_text = (
            f"[{persona} LOG]\n"
            f"Command '{cmd}' received.\n"
            f"Processing request... Done.\n"
            f"Awaiting further inputs."
        )

    return {
        "status": "SUCCESS",
        "persona": persona,
        "text": response_text
    }

# -----------------------
# CYBERPUNK UI (HTML)
# -----------------------
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>FTM-2077 TERMINAL</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
            
            body { 
                background-color: #050505; 
                color: #00ff41; 
                font-family: 'VT323', monospace; 
                margin: 0; 
                padding: 40px;
                overflow: hidden;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                border: 2px solid #00ff41;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
                background: rgba(0, 20, 0, 0.9);
                min-height: 500px;
            }

            h2 {
                text-align: center;
                border-bottom: 1px dashed #00ff41;
                padding-bottom: 10px;
                letter-spacing: 2px;
                text-shadow: 0 0 5px #00ff41;
            }

            .input-group {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }

            input { 
                background: #000; 
                color: #00ff41; 
                border: 1px solid #00ff41; 
                padding: 10px; 
                flex-grow: 1;
                font-family: 'VT323', monospace;
                font-size: 1.2rem;
                outline: none;
            }

            button { 
                background: #00ff41; 
                color: #000; 
                border: none; 
                padding: 10px 20px; 
                cursor: pointer; 
                font-family: 'VT323', monospace;
                font-size: 1.2rem;
                font-weight: bold;
            }

            button:hover {
                background: #00cc33;
                box-shadow: 0 0 10px #00ff41;
            }

            pre { 
                margin-top: 20px; 
                background: #0a0a0a; 
                padding: 15px; 
                border-left: 3px solid #00ff41; 
                white-space: pre-wrap; 
                min-height: 100px;
                font-size: 1.1rem;
                line-height: 1.4;
            }

            .scanline {
                width: 100%;
                height: 100px;
                z-index: 10;
                background: linear-gradient(0deg, rgba(0,0,0,0) 0%, rgba(0, 255, 65, 0.04) 50%, rgba(0,0,0,0) 100%);
                opacity: 0.1;
                position: absolute;
                bottom: 100%;
                animation: scanline 10s linear infinite;
                pointer-events: none;
            }

            @keyframes scanline {
                0% { bottom: 100%; }
                100% { bottom: -100%; }
            }
        </style>
    </head>
    <body>
        <div class="scanline"></div>
        <div class="container">
            <h2>SYSTEM: FTM-2077 OMEGA</h2>
            <div id="output-area">
                <pre id="out">System initialized. Waiting for input...</pre>
            </div>
            
            <div class="input-group">
                <input id="cmd" placeholder="Enter command protocol..." onkeypress="handleEnter(event)"/>
                <button onclick="run()">EXECUTE</button>
            </div>
        </div>

        <script>
            function handleEnter(e) {
                if (e.key === 'Enter') run();
            }

            async function run(){
                const cmdInput = document.getElementById("cmd");
                const outScreen = document.getElementById("out");
                const cmd = cmdInput.value;

                if(!cmd) return;

                outScreen.innerText = "Processing: " + cmd + "...";

                try {
                    const res = await fetch("/api/execute", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({command: cmd, persona: "JARVIS"})
                    });
                    
                    const data = await res.json();
                    
                    // Typewriter effect simulation (instant for now)
                    outScreen.innerText = data.text;
                    cmdInput.value = ""; // Clear input
                    
                } catch(err) {
                    outScreen.innerText = "CRITICAL ERROR: Connection to core lost.";
                }
            }
        </script>
    </body>
    </html>
    """

# -----------------------
# WEBSOCKET (REAL-TIME)
# -----------------------
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("FTM-2077 SECURE CHANNEL ESTABLISHED")
        while True:
            data = await websocket.receive_text()
            # Echo back with style
            await websocket.send_text(f"SERVER_ACK: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# -----------------------
# RUNNER
# -----------------------
if __name__ == "__main__":
    # Runs the server on localhost:8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
