from pydantic import BaseModel, validator, Field

# Allowed personas
VALID_PERSONAS = {"JARVIS", "ULTRON", "GOD", "REAPER", "FRIDAY"}

class MissionRequest(BaseModel):
    command: str = Field(..., min_length=2, description="User command to the AI")
    persona: str = Field("JARVIS", description="Selected AI persona")

    # -------- Persona Validator ----------
    @validator("persona")
    def normalize_persona(cls, v):
        if not v:
            return "JARVIS"

        v = v.upper().strip()
        return v if v in VALID_PERSONAS else "JARVIS"

    # -------- Command Validator ----------
    @validator("command")
    def clean_command(cls, v):
        if not v or not v.strip():
            raise ValueError("Command cannot be empty or whitespace.")
        return v.strip()
