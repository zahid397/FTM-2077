from datetime import datetime
try: from colorama import Fore, Style, init; init(autoreset=True); COLOR=True
except: COLOR=False
class SystemLogger:
    def log(self, src, msg, level="INFO"):
        t = datetime.now().strftime("%H:%M:%S")
        if COLOR:
            c = Fore.CYAN if src=="CORE" else Fore.GREEN
            print(f"{Style.DIM}[{t}]{Style.RESET_ALL} {c}[{src}]{Style.RESET_ALL} > {msg}")
        else: print(f"[{t}] [{src}] > {msg}")
sys_log = SystemLogger()
