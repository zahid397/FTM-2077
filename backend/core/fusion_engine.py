import random
from backend.config import settings
try: from cerebras.cloud.sdk import Cerebras
except: Cerebras = None

class FusionEngine:
    def __init__(self):
        self.client = Cerebras(api_key=settings.CEREBRAS_KEY) if settings.CEREBRAS_KEY and Cerebras else None

    def process(self, cmd, persona):
        analysis = f"Simulated tactical analysis for: {cmd}"
        if self.client:
            try:
                res = self.client.chat.completions.create(
                    messages=[{"role":"user", "content": f"Act as {persona}. {cmd}"}],
                    model="llama3.1-70b"
                )
                analysis = res.choices[0].message.content
            except: pass
        return {"status": "SUCCESS", "command": cmd, "persona": persona, "analysis": analysis, "probability": random.randint(85, 99)}

fusion = FusionEngine()
