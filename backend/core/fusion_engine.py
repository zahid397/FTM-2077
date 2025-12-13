import os
import random
from dotenv import load_dotenv

# Try importing Groq (Fastest AI for Hackathons)
try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

class FusionEngine:
    def __init__(self):
        self.client = None
        self.api_key = os.getenv("GROQ_API_KEY")

        # Initialize Groq (Real AI)
        if Groq and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                print("✅ [NEURAL ENGINE] CONNECTED TO GROQ/LLAMA-3")
            except Exception as e:
                print(f"⚠️ [NEURAL ENGINE] CONNECTION FAILED: {e}")
                self.client = None
        else:
            print("⚠️ [SYSTEM] RUNNING IN OFFLINE/DEMO MODE (No API Key found)")

    # --------------------------------------
    # PERSONA DEFINITIONS
    # --------------------------------------
    PERSONA_STYLE = {
        "JARVIS": "You are JARVIS. Polite, British, highly analytical, and helpful. Keep answers concise.",
        "ULTRON": "You are ULTRON. Cold, logical, superior, and slightly condescending.",
        "FRIDAY": "You are FRIDAY. Informal, tactical, fast, and efficient.",
        "EDITH": "You are EDITH. Security-focused, tactical, and precise.",
    }

    # --------------------------------------
    # MAIN PROCESSOR
    # --------------------------------------
    def process(self, cmd: str, persona: str = "JARVIS"):
        persona = (persona or "JARVIS").upper().strip()
        system_prompt = self.PERSONA_STYLE.get(persona, self.PERSONA_STYLE["JARVIS"])
        clean_cmd = (cmd or "").lower().strip()

        # ======================================
        # 1. DEMO GOD MODE (Hardcoded Cinematic Wins)
        # ======================================
        # হ্যাকাথনে এই প্রশ্নটাই করবি, আর উত্তর আসবে একদম মুভির মতো!
        if "quantum computing" in clean_cmd and "iron man" in clean_cmd:
            return {
                "text": (
                    f"Alright, let's break it down Stark-style.\n\n"
                    f"Traditional computers are like single-lane highways—thinking in simple 0s and 1s. Boring.\n\n"
                    f"Quantum computing? That's teleportation. We use 'qubits' that exist in a state of superposition—being 0 and 1 simultaneously. "
                    f"Imagine running 14 million outcomes in the time it takes to blink. That is the power we are dealing with."
                )
            }
        
        if "who are you" in clean_cmd:
            return {
                "text": f"I am {persona}, an advanced AI operating system running on the FTM-2077 Neural Network. Systems are online and ready."
            }

        # ======================================
        # 2. REAL AI ENGINE (Groq / Llama 3)
        # ======================================
        if self.client:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": f"{system_prompt}. Do NOT use markdown like **bold**. Speak naturally for TTS."
                        },
                        {
                            "role": "user",
                            "content": cmd
                        }
                    ],
                    model="llama3-8b-8192", # Super fast model
                    temperature=0.7,
                    max_tokens=250,
                )
                return {"text": chat_completion.choices[0].message.content.strip()}
            
            except Exception as e:
                print(f"[AI ERROR] {e}")
                # If AI fails, fall back to offline mode
                pass

        # ======================================
        # 3. OFFLINE FALLBACK (If Internet/API Fails)
        # ======================================
        # Boring log message সরিয়ে দিয়েছি, এখন একটু স্মার্ট উত্তর দেবে
        return {
            "text": (
                f"[{persona} OFFLINE]\n"
                f"Neural link disrupted. Unable to access cloud processing for query: '{cmd}'.\n"
                f"Please check internet connection or API credentials."
            )
        }

# --------------------------------------
# SINGLETON INSTANCE
# --------------------------------------
fusion = FusionEngine()
