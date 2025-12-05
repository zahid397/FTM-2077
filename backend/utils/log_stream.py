from fastapi import WebSocket
from datetime import datetime

class LogStreamer:
    """
    Real-time WebSocket log streamer for FTM-2077.
    Supports: broadcast(), connect(), disconnect()
    Safe for Raindrop + Local deploy.
    """
    def __init__(self):
        self.active_clients = []

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket client."""
        if websocket in self.active_clients:
            self.active_clients.remove(websocket)

    async def broadcast(self, message: str, level: str = "INFO"):
        """Send log message to all active WebSocket clients."""
        log_packet = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": level.upper(),
            "message": message
        }

        # Loop through all active WebSockets
        dead_clients = []
        for client in self.active_clients:
            try:
                await client.send_json(log_packet)
            except Exception:
                dead_clients.append(client)

        # Remove dead clients
        for dc in dead_clients:
            if dc in self.active_clients:
                self.active_clients.remove(dc)


# Global instance
streamer = LogStreamer()
