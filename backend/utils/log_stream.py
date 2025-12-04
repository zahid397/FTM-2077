from fastapi import WebSocket
from datetime import datetime
class LogStreamer:
    def __init__(self): self.active = []
    async def connect(self, ws): await ws.accept(); self.active.append(ws)
    def disconnect(self, ws): self.active.remove(ws) if ws in self.active else None
    async def broadcast(self, msg, level="INFO"):
        payload = {"timestamp": datetime.now().strftime("%H:%M:%S"), "type": level.upper(), "message": msg}
        for ws in self.active: 
            try: await ws.send_json(payload)
            except: pass
streamer = LogStreamer()
