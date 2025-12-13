from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

-----------------------

LOAD SETTINGS

-----------------------

from backend.config import settings

-----------------------

INTERNAL MODULES

-----------------------

from backend.models.mission_model import MissionRequest
from backend.utils.logger import sys_log
from backend.utils.log_stream import streamer
from backend.core.fusion_engine import fusion
from backend.services.security_engine import security

-----------------------

OPTIONAL MODULES (SAFE)

-----------------------

try:
from backend.services.audio_engine import audio_engine
except Exception:
audio_engine = None

try:
from backend.services.vultr_storage import vultr
except Exception:
vultr = None

=====================================================

FASTAPI APP INIT

=====================================================

app = FastAPI(
title=settings.PROJECT_NAME,
version=settings.VERSION
)

-----------------------

CORS (OPEN FOR NOW)

-----------------------

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=True,
allow_methods=[""],
allow_headers=["*"],
)

-----------------------

STATIC AUDIO SERVING

-----------------------

if os.path.exists(settings.AUDIO_DIR):
app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")

=====================================================

ROUTES

=====================================================

@app.get("/")
def root():
return {
"status": "ONLINE",
"project": settings.PROJECT_NAME,
"version": settings.VERSION
}

@app.post(f"{settings.API_PREFIX}/execute")
def execute_mission(payload: MissionRequest):
sys_log("MISSION_RECEIVED", payload.command)

# 🔐 Security check  
if not security.validate(payload.command):  
    return {  
        "status": "BLOCKED",  
        "reason": "Security policy violation"  
    }  

result = fusion.process(  
    cmd=payload.command,  
    persona=payload.persona  
)  

# 🔊 Optional audio generation  
if audio_engine:  
    try:  
        audio_path = audio_engine.speak(result["text"], payload.persona)  
        result["audio"] = audio_path  
    except Exception as e:  
        sys_log("AUDIO_FAIL", str(e))  

return result

=====================================================

WEBSOCKET (LIVE STREAM)

=====================================================

@app.websocket("/ws/logs")
async def websocket_logs(ws: WebSocket):
await ws.accept()
streamer.connect(ws)

try:  
    while True:  
        await ws.receive_text()  
except WebSocketDisconnect:  
    streamer.disconnect(ws)

=====================================================

HEALTH CHECK

=====================================================

@app.get("/health")
def health():
return {
"status": "OK",
"god_mode": settings.GOD_MODE
}
