import random
from backend.config import settings

# --------------------------------------
# Optional Cerebras LLM
# --------------------------------------
try:
    from cerebras.cloud.sdk import Cerebras
except Exception:
    Cerebras = None


class FusionEngine:
    def __init__(self):
        self.client = None

        if Cerebras and getattr(settings, "CEREBRAS_API_KEY", ""):
            try:
                self.client = Cerebras(
                    api_key=settings.CEREBRAS_API_KEY
                )
                print("[CEREBRAS] Connected to Ultra-Low Latency Engine.")
            except Exception as e:
                print("[CEREBRAS] Connection failed:", e)
                self.client = None

    # --------------------------------------
    # PERSONA DEFINITIONS
    # --------------------------------------
    PERSONA_STYLE = {
        "JARVIS": "Polite, British, highly analytical assistant.",
        "ULTRON": "Cold, ruthless, logical, domination-oriented intelligence.",
        "FRIDAY": "Friendly, fast, tactical mission assistant.",
        "REAPER": "Dark, cryptic, intimidating presence.",
        "GOD": "Omniscient, absolute, calm authority with perfect clarity."
    }

    # --------------------------------------
    # MAIN PROCESSOR
    # --------------------------------------
    def process(self, cmd: str, persona: str = "JARVIS"):
        persona = (persona or "JARVIS").upper().strip()
        persona_desc = self.PERSONA_STYLE.get(
            persona, "Advanced artificial intelligence."
        )

        clean_cmd = (cmd or "").lower().strip()

        # ======================================
        # QUICK INTENT HANDLERS (NO LLM)
        # ======================================
        greetings = ["hi", "hello", "hey", "yo"]
        wellbeing = [
            "how are you",
            "how r u",
            "how are you doing"
        ]
        thanks = ["thanks", "thank you"]
        status = ["status", "system status"]

        if clean_cmd in greetings:
            return {
                "text": f"Hello. {persona} online and operational. How may I assist you?"
            }

        if clean_cmd in wellbeing:
            return {
                "text": "All systems are running within optimal parameters."
            }

        if clean_cmd in thanks:
            return {
                "text": "Acknowledged. Standing by for further instructions."
            }

        if clean_cmd in status:
            return {
                "text": (
                    f"[{persona} STATUS]\n"
                    f"• Core systems: ONLINE\n"
                    f"• Security layer: ACTIVE\n"
                    f"• Persona mode: {persona}\n"
                    f"• Intelligence: STABLE"
                )
            }

        # ======================================
        # DEFAULT OFFLINE FALLBACK
        # ======================================
        text = (
            f"[{persona} ONLINE]\n\n"
            f"Command acknowledged.\n\n"
            f"▸ Input: {cmd}\n"
            f"▸ Mode: {persona_desc}\n\n"
            f"System analysis complete.\n"
            f"Awaiting further instructions."
        )

        # ======================================
        # CEREBRAS LLM (IF AVAILABLE)
        # ======================================
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

                text = res.choices[0].message.content.strip()

            except Exception as e:
                print("[CEREBRAS ERROR]", e)

        return {
            "text": text
        }


# --------------------------------------
# SINGLETON (USE EVERYWHERE)
# --------------------------------------
fusion = FusionEngine()
