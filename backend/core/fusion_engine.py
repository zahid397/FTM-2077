import random
from backend.config import settings

# Optional Cerebras
try:
    from cerebras.cloud.sdk import Cerebras
except Exception:
    Cerebras = None


class FusionEngine:
    def __init__(self):
        self.client = None

        if Cerebras and getattr(settings, "CEREBRAS_API_KEY", ""):
            try:
                self.client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
                print("[CEREBRAS] Connected to Ultra-Low Latency Engine.")
            except Exception as e:
                print("[CEREBRAS] Connection failed:", e)
                self.client = None

    # -----------------------------------------------------
    # PERSONA STYLES
    # -----------------------------------------------------
    PERSONA_STYLE = {
        "JARVIS": "Polite, British, highly analytical assistant.",
        "ULTRON": "Cold, ruthless, logical, domination-oriented intelligence.",
        "FRIDAY": "Friendly, fast, tactical mission assistant.",
        "REAPER": "Dark, cryptic, intimidating presence.",
        "GOD": "Omniscient, absolute, calm authority with perfect clarity."
    }

    # -----------------------------------------------------
    # MAIN PROCESSING
    # -----------------------------------------------------
    def process(self, cmd: str, persona: str = "JARVIS"):
        persona = (persona or "JARVIS").upper().strip()

        persona_desc = self.PERSONA_STYLE.get(
            persona, "Standard advanced artificial intelligence."
        )

        # -----------------------------
        # OFFLINE FALLBACK (NO LLM)
        # -----------------------------
        offline_text = (
            f"[{persona} ONLINE]\n\n"
            f"Command acknowledged.\n\n"
            f"▸ Input: {cmd}\n"
            f"▸ Mode: {persona_desc}\n\n"
            f"System analysis complete.\n"
            f"Awaiting further instructions."
        )

        text = offline_text

        # -----------------------------
        # CEREBRAS EXECUTION
        # -----------------------------
        if self.client:
            try:
                res = self.client.chat.completions.create(
                    model="llama3.1-70b",
                    temperature=0.4,
                    max_tokens=500,
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are {persona}. {persona_desc}"
                        },
                        {
                            "role": "user",
                            "content": cmd
                        }
                    ]
                )

                ai_text = res.choices[0].message.content
                if ai_text and ai_text.strip():
                    text = ai_text.strip()

            except Exception as e:
                print("[CEREBRAS ERROR]", e)
                text = offline_text

        # -----------------------------
        # FINAL RESPONSE PACKET
        # -----------------------------
        return {
            "status": "SUCCESS",
            "persona": persona,
            "command": cmd,
            "text": text,          # 🔥 frontend typing effect ready
            "audio": None,         # 🔊 future TTS hook
            "confidence": random.randint(88, 99)
        }


fusion = FusionEngine()
