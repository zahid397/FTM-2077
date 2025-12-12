import os
import sys

# System Color Codes
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

structure = [
    # Config Files
    ".env",
    ".gitignore",
    "requirements.txt",
    "Dockerfile",
    
    # Backend Core
    "backend/__init__.py",
    "backend/main.py",
    "backend/config.py",
    "backend/core/__init__.py",
    "backend/core/fusion_engine.py",
    "backend/core/logic_engine.py",
    "backend/core/quantum_engine.py",
    
    # Services
    "backend/services/__init__.py",
    "backend/services/audio_engine.py",
    "backend/services/vultr_storage.py",
    "backend/services/security_engine.py",
    
    # Utils
    "backend/utils/__init__.py",
    "backend/utils/logger.py",
    "backend/utils/reaper.py",
    
    # Data Models
    "backend/models/mission_model.py",
    
    # Auto-Generated Folders (No files needed inside initially)
    "backend/logs/",
    "backend/audio/",
    
    # Frontend
    "frontend/index.html",
    "frontend/css/cyberpunk.css",
    "frontend/js/core.js",
    "frontend/assets/icons/",
    
    # Universe Data
    "universe/factions/",
    "universe/missions/",
    "universe/memory/"
]

def create_omega_system():
    print(f"{CYAN}[OMEGA] Initializing File System Construction...{RESET}")
    
    for path in structure:
        if path.endswith("/"):
            # It's a directory
            os.makedirs(path, exist_ok=True)
        else:
            # It's a file
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    # Write basic content for specific files
                    if "requirements.txt" in path:
                        f.write("fastapi\nuvicorn\npython-dotenv\nrequests\npydantic\ncolorama")
                    elif ".gitignore" in path:
                        f.write("__pycache__/\n.env\n*.log\n.DS_Store")
                    elif ".env" in path:
                        f.write("ELEVENLABS_KEY=your_key_here\nVULTR_KEY=your_key_here")
                    else:
                        f.write("") # Empty file
                print(f"{GREEN} [+] Created: {path}{RESET}")
            else:
                print(f" [.] Exists: {path}")

    print(f"\n{CYAN}[OMEGA] Construction Complete. System Ready.{RESET}")

if __name__ == "__main__":
    create_omega_system()
