import os
import wave
import struct
import math

from backend.config import settings

# Optional: ElevenLabs
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save
except:
    ElevenLabs = None


# -------------------------------
# PERSONA -> VOICE MAPPING
# -------------------------------
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
        
        # Ensure backend/audio directory exists
        os.makedirs(settings.AUDIO_DIR, exist_ok=True)

        # ElevenLabs client load
        if settings.ELEVENLABS_API_KEY and ElevenLabs:
            try:
                self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            except Exception as e:
                print(f"[AUDIO] ElevenLabs init failed → {e}")
                self.client = None


    # ------------------------------------------------
    # MAIN: Generate Persona Based Audio
    # ------------------------------------------------
    def generate_voice(self, text, persona="JARVIS"):
        persona = persona.upper()

        file_name = f"voice_{persona}.wav"
        file_path = os.path.join(settings.AUDIO_DIR, file_name)

        # -----------------------
        # 1️⃣ TRY REAL ELEVENLABS
        # -----------------------
        if self.client:
            try:
                voice_name = VOICE_MAP.get(persona, "Rachel")
                
                audio = self.client.generate(
                    text=text[:200],                   # Limit for safety
                    voice=voice_name,                  # Persona voice
                    model="eleven_turbo_v2"
                )

                save(audio, file_path)
                return f"/audio/{file_name}"

            except Exception as e:
                print(f"[AUDIO] ElevenLabs Error → {e}")
                # continue to synthetic fallback


        # -----------------------
        # 2️⃣ SYNTHETIC BACKUP AUDIO (NEVER FAILS)
        # -----------------------
        try:
            with wave.open(file_path, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)

                frames = []
                for i in range(44100):  # 1 second fallback tone
                    value = int(math.sin(i / 15) * 6000)
                    frames.append(struct.pack("<h", value))

                f.writeframes(b"".join(frames))

        except Exception as e:
            print(f"[AUDIO ERROR] Failed to write synthetic audio → {e}")
            return None

        return f"/audio/{file_name}"


# Global instance
audio_engine = AudioEngine()
