from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

# -----------------------
# SIMPLE SETTINGS (NO PYDANTIC DRAMA)
# -----------------------
PROJECT_NAME = "FTM-2077 OMEGA"
VERSION = "2.0.77"
API_PREFIX = "/api"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# -----------------------
# FASTAPI APP INIT
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
# ROOT
# -----------------------
@app.get("/")
def root():
    return {"status": "ONLINE", "project": PROJECT_NAME, "version": VERSION}

# -----------------------
# HEALTH
# -----------------------
@app.get("/health")
def health():
    return {"status": "OK"}

# -----------------------
# API EXECUTE (DEMO)
# -----------------------
@app.post(f"{API_PREFIX}/execute")
def execute(payload: dict):
    cmd = payload.get("command", "").strip()
    persona = payload.get("persona", "JARVIS")

    if not cmd:
        return JSONResponse(
            status_code=400,
            content={"status": "ERROR", "reason": "Command empty"}
        )

    # Demo response (replace with fusion engine later)
    return {
        "status": "SUCCESS",
        "persona": persona,
        "text": f"[{persona}] Executed command: {cmd}"
    }

# -----------------------
# INLINE UI (HTML + JS)
# -----------------------
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>FTM-2077</title>
  <meta charset="utf-8"/>
  <style>
    body {
      background: #000;
      color: #00ffcc;
      font-family: monospace;
      padding: 20px;
    }
    button {
      background: #00ffcc;
      color: #000;
      border: none;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: bold;
    }
    input {
      background: #111;
      color: #00ffcc;
      border: 1px solid #00ffcc;
      padding: 8px;
      width: 300px;
    }
    pre {
      margin-top: 16px;
      background: #111;
      padding: 12px;
      border: 1px solid #00ffcc;
    }
  </style>
</head>
<body>

<h1>FTM-2077 OMEGA</h1>

<input id="cmd" placeholder="Enter command..." />
<button onclick="run()">EXECUTE</button>

<pre id="out"></pre>

<script>
async function run() {
  const cmd = document.getElementById("cmd").value;

  const res = await fetch("/api/execute", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      command: cmd,
      persona: "JARVIS"
    })
  });

  const data = await res.json();
  document.getElementById("out").innerText =
    JSON.stringify(data, null, 2);
}
</script>

</body>
</html>
"""

# -----------------------
# WEBSOCKET (OPTIONAL)
# -----------------------
@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"ACK: {msg}")
    except WebSocketDisconnect:
        pass
