from datetime import datetime

# Optional color support (local only)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR_ENABLED = True
except:
    COLOR_ENABLED = False


class LogStreamer:
    """WebSocket-based real-time log broadcaster (FTM-2077)."""
    def __init__(self):
        self.active = []

    async def connect(self, ws):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        packet = {
            "timestamp": timestamp,
            "type": level.upper(),
            "message": msg
        }

        # Send to all live sockets
        for ws in self.active:
            try:
                await ws.send_json(packet)
            except:
                pass


streamer = LogStreamer()


class SystemLogger:
    """Unified logger → prints to terminal + sends to WebSocket"""

    async def async_log(self, source, message, level="INFO"):
        """Used when called inside async functions (FastAPI)"""
        self._print_log(source, message, level)
        await streamer.broadcast(message, level)

    def log(self, source, message, level="INFO"):
        """Sync version (normal Python functions)"""
        self._print_log(source, message, level)

    def _print_log(self, source, message, level):
        timestamp = datetime.now().strftime("%H:%M:%S")
        src = source.upper()

        if COLOR_ENABLED:
            color = (
                Fore.CYAN if src == "CORE"
                else Fore.RED if level.upper() == "ERROR"
                else Fore.GREEN
            )
            print(f"{Style.DIM}[{timestamp}]{Style.RESET_ALL} "
                  f"{color}[{src}]{Style.RESET_ALL} > {message}")
        else:
            print(f"[{timestamp}] [{src}] > {message}")


sys_log = SystemLogger()
