from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# -----------------------
# CONFIG + INTERNAL MODULES
# -----------------------
from config import settings
from models.mission_model import MissionRequest
from utils.logger import sys_log
from utils.log_stream import streamer
from core.fusion_engine import fusion
from services.security_engine import security

# -----------------------
# OPTIONAL MODULES (SAFE)
# -----------------------
try:
    from services.audio_engine import audio_engine
except Exception:
    audio_engine = None

try:
    from services.vultr_storage import vultr
except Exception:
    vultr = None

try:
    from services.report_engine import report_engine
except Exception:
    report_engine = None


# -----------------------
# APP INITIALIZE
# -----------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# STATIC FILES (AUDIO)
# -----------------------
if os.path.exists(settings.AUDIO_DIR):
    app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")


# -----------------------
# WEBSOCKET LOG STREAM
# -----------------------
@app.websocket("/ws/logs")
async def log_stream(ws: WebSocket):
    await streamer.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        streamer.disconnect(ws)


# -----------------------
# LOGIN MODEL
# -----------------------
class LoginRequest(BaseModel):
    password: str


# -----------------------
# ROOT
# -----------------------
@app.get("/")
def root():
    return {
        "system": "FTM-2077",
        "status": "ONLINE",
        "god_mode": settings.GOD_MODE
    }


# -----------------------
# LOGIN
# -----------------------
@app.post("/auth/login")
async def login(req: LoginRequest):
    res = security.login(req.password)
    if res["status"] == "SUCCESS" and res.get("mode") == "GOD":
        settings.GOD_MODE = True
        await streamer.broadcast("⚡ GOD MODE ACTIVATED", "GOD")
    return res


# -----------------------
# MAIN EXECUTION
# -----------------------
@app.post(f"{settings.API_PREFIX}/execute")
async def execute(req: MissionRequest):
    sys_log.log("CORE", f"CMD: {req.command} [{req.persona}]")
    await streamer.broadcast(f"Processing: {req.command}", "CORE")

    # 1. Fusion Engine
    result = fusion.process(req.command, req.persona)

    # 2. Audio (Optional)
    if audio_engine:
        try:
            result["audio"] = audio_engine.generate_voice(
                result["analysis"],
                req.persona
            )
        except Exception as e:
            sys_log.log("ERROR", f"Audio Failed: {e}")

    # 3. Report + Cloud Upload (Optional)
    if report_engine:
        try:
            rep = report_engine.create_mission_report(result)
            result["report_local"] = rep["path"]

            if vultr:
                cloud = vultr.upload_file(
                    rep["path"],
                    f"reports/{rep['report_id']}.json"
                )
                if cloud:
                    result["cloud_report"] = cloud
                    await streamer.broadcast("Report Sent To Cloud", "CLOUD")
        except Exception as e:
            sys_log.log("ERROR", f"Report Failed: {e}")

    await streamer.broadcast(
        f"Done. Probability: {result.get('probability', 0)}%",
        "AI"
    )

    return result


# -----------------------
# TOGGLE GOD MODE
# -----------------------
@app.post(f"{settings.API_PREFIX}/godmode")
async def toggle_god(key: str):
    if settings.validate_god_key(key):
        settings.GOD_MODE = not settings.GOD_MODE
        await streamer.broadcast(f"GOD MODE: {settings.GOD_MODE}", "GOD")
        return {"status": "SUCCESS", "god_mode": settings.GOD_MODE}

    return {"status": "ERROR"}


# -----------------------
# LOCAL DEV SUPPORT
# -----------------------
if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Running on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT
    )
