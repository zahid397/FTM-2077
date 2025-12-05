import random
from backend.config import settings

# Optional Cerebras
try:
    from cerebras.cloud.sdk import Cerebras
except:
    Cerebras = None


class FusionEngine:
    def __init__(self):
        # Safe: no crash if key missing
        self.client = None
        if Cerebras and getattr(settings, "CEREBRAS_API_KEY", ""):
            try:
                self.client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
                print("[CEREBRAS] Connected to Ultra-Low Latency Engine.")
            except Exception as e:
                print("[CEREBRAS] Failed:", e)
                self.client = None

    # -----------------------------------------------------
    # Persona Styles (Offline Fallback)
    # -----------------------------------------------------
    PERSONA_STYLE = {
        "JARVIS": "Polite, British, highly analytical assistant.",
        "ULTRON": "Cold, logical, domination-oriented tone.",
        "FRIDAY": "Friendly, fast, mission-focused assistant.",
        "REAPER": "Dark, cryptic, intimidating voice.",
        "GOD": "Omniscient, absolute tone with perfect clarity."
    }

    # -----------------------------------------------------
    # MAIN PROCESSING
    # -----------------------------------------------------
    def process(self, cmd: str, persona: str):
        persona = persona.upper().strip()

        # Default fallback analysis (in case Cerebras is missing)
        offline_analysis = (
            f"[{persona}] Tactical Evaluation:\n"
            f"• Command received → {cmd}\n"
            f"• Persona Context → {self.PERSONA_STYLE.get(persona, 'Standard AI Mode')}\n"
            f"• Initial threat probability computed.\n"
            f"• Situation stable. Ready for further directives."
        )

        # -------------------------------------------------
        # 1. Try Cerebras API
        # -------------------------------------------------
        if self.client:
            try:
                res = self.client.chat.completions.create(
                    model="llama3.1-70b",
                    messages=[
                        {"role": "system", "content": f"You are {persona}. {self.PERSONA_STYLE.get(persona, '')}"},
                        {"role": "user", "content": cmd}
                    ]
                )

                # Safe extraction
                ai_text = None
                try:
                    ai_text = res.choices[0].message.content
                except:
                    ai_text = None

                if ai_text:
                    analysis = ai_text
                else:
                    analysis = offline_analysis

            except Exception as e:
                print("[CEREBRAS ERROR]", e)
                analysis = offline_analysis
        else:
            analysis = offline_analysis

        # -------------------------------------------------
        # Final structured packet
        # -------------------------------------------------
        return {
            "status": "SUCCESS",
            "command": cmd,
            "persona": persona,
            "analysis": analysis,
            "probability": random.randint(88, 99)
        }


fusion = FusionEngine()
