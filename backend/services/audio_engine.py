import os
import wave
import struct
import math
from datetime import datetime

from backend.config import settings

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save
except:
    ElevenLabs = None


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

        os.makedirs(settings.AUDIO_DIR, exist_ok=True)

        # ✅ IMPORTANT: config এ যেটা আছে সেটা ব্যবহার কর
        api_key = getattr(settings, "ELEVENLABS_KEY", "") or getattr(settings, "ELEVENLABS_API_KEY", "")

        if api_key and ElevenLabs:
            try:
                self.client = ElevenLabs(api_key=api_key)
            except Exception as e:
                print(f"[AUDIO] ElevenLabs init failed → {e}")
                self.client = None

    def generate_voice(self, text: str, persona="JARVIS"):
        persona = (persona or "JARVIS").upper()
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # ✅ ElevenLabs এ mp3 safe
        mp3_name = f"voice_{persona}_{ts}.mp3"
        mp3_path = os.path.join(settings.AUDIO_DIR, mp3_name)

        # 1) Try ElevenLabs
        if self.client:
            try:
                voice_name = VOICE_MAP.get(persona, "Rachel")

                audio = self.client.generate(
                    text=(text or "")[:600],
                    voice=voice_name,
                    model="eleven_turbo_v2"
                )

                save(audio, mp3_path)
                return f"/audio/{mp3_name}"

            except Exception as e:
                print(f"[AUDIO] ElevenLabs Error → {e}")

        # 2) Fallback wav (never fails)
        wav_name = f"fallback_{persona}_{ts}.wav"
        wav_path = os.path.join(settings.AUDIO_DIR, wav_name)

        try:
            framerate = 44100
            duration = 0.7
            frequency = 880

            with wave.open(wav_path, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(framerate)

                frames = []
                for i in range(int(duration * framerate)):
                    value = int(8000 * math.sin(2 * math.pi * frequency * i / framerate))
                    frames.append(struct.pack("<h", value))

                f.writeframes(b"".join(frames))

            return f"/audio/{wav_name}"

        except Exception as e:
            print(f"[AUDIO ERROR] Failed fallback wav → {e}")
            return None


audio_engine = AudioEngine()
