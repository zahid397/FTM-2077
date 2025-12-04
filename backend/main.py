from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

sys.path.append(os.getcwd())

from backend.config import settings
from backend.models.mission_model import MissionRequest
from backend.utils.logger import sys_log
from backend.utils.log_stream import streamer
from backend.core.fusion_engine import fusion
from backend.services.security_engine import security

# Safe Imports (Services)
try: from backend.services.audio_engine import audio_engine
except: audio_engine = None
try: from backend.services.vultr_storage import vultr
except: vultr = None
try: from backend.services.report_engine import report_engine
except: report_engine = None

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")

@app.websocket("/ws/logs")
async def log_stream(ws: WebSocket):
    await streamer.connect(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect:
        streamer.disconnect(ws)

class LoginRequest(BaseModel):
    password: str

@app.get("/")
def root():
    return {"system": "FTM-2077", "status": "ONLINE", "god_mode": settings.GOD_MODE}

@app.post("/auth/login")
async def login(req: LoginRequest):
    res = security.login(req.password)
    if res["status"] == "SUCCESS" and res.get("mode") == "GOD":
        settings.GOD_MODE = True
        await streamer.broadcast("⚡ GOD MODE ACTIVATED", "GOD")
    return res

@app.post(f"{settings.API_PREFIX}/execute")
async def execute(req: MissionRequest):
    sys_log.log("CORE", f"CMD: {req.command} [{req.persona}]")
    await streamer.broadcast(f"Processing: {req.command}", "CORE")

    # 1. Fusion
    result = fusion.process(req.command, req.persona)

    # 2. Audio (Updated)
    if audio_engine:
        result["audio"] = audio_engine.generate_voice(result["analysis"], req.persona)

    # 3. Report & Cloud (Updated)
    if report_engine:
        try:
            rep = report_engine.create_mission_report(result)
            result["report_local"] = rep["path"]
            
            if vultr:
                cloud = vultr.upload_file(rep["path"], f"reports/{rep['report_id']}.json")
                if cloud:
                    result["cloud_report"] = cloud
                    await streamer.broadcast("Report Sent To Cloud", "CLOUD")
        except Exception as e:
            sys_log.log("ERROR", f"Report Failed: {e}")

    await streamer.broadcast(f"Done. Probability: {result['probability']}%", "AI")
    return result

@app.post(f"{settings.API_PREFIX}/godmode")
async def toggle_god(key: str):
    if settings.validate_god_key(key):
        settings.GOD_MODE = not settings.GOD_MODE
        await streamer.broadcast(f"GOD MODE: {settings.GOD_MODE}", "GOD")
        return {"status": "SUCCESS", "god_mode": settings.GOD_MODE}
    return {"status": "ERROR"}

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Running on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
