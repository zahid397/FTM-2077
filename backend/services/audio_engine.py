import os
import wave
import struct
import math
from backend.config import settings

# ElevenLabs Import (Optional)
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save
except:
    ElevenLabs = None

# Persona-wise Voice Mapping
VOICE_MAP = {
    "JARVIS": "Rachel",
    "ULTRON": "Adam",
    "FRIDAY": "Bella",
    "REAPER": "Sam",
    "GOD": "Brian"
}

class AudioEngine:
    def __init__(self):
        self.client = None
        if settings.ELEVEN_KEY and ElevenLabs:
            try:
                self.client = ElevenLabs(api_key=settings.ELEVEN_KEY)
            except:
                self.client = None

    def generate_voice(self, text, persona):
        persona = persona.upper()
        fname = f"voice_{persona}.wav"
        path = os.path.join(settings.AUDIO_DIR, fname)

        # 1. Real Voice Engine
        if self.client:
            try:
                voice_name = VOICE_MAP.get(persona, "Rachel")
                audio = self.client.generate(
                    text=text[:200],
                    voice=voice_name,
                    model="eleven_turbo_v2"
                )
                save(audio, path)
                return f"/audio/{fname}"
            except Exception as e:
                print(f"[AUDIO ERROR] ElevenLabs failed → {e}")

        # 2. Fallback Synthetic Tone
        try:
            with wave.open(path, 'w') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)
                tone = [struct.pack('<h', int(math.sin(i / 12) * 8000)) for i in range(44100)]
                f.writeframes(b"".join(tone))
        except Exception as e:
            print(f"[FALLBACK AUDIO ERROR] {e}")

        return f"/audio/{fname}"

audio_engine = AudioEngine()
