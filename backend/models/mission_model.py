from pydantic import BaseModel, validator, Field
VALID_PERSONAS = {"JARVIS", "ULTRON", "GOD", "REAPER", "FRIDAY"}
class MissionRequest(BaseModel):
    command: str = Field(..., min_length=2)
    persona: str = Field("JARVIS")
    @validator("persona")
    def normalize(cls, v):
        v = v.upper().strip()
        return v if v in VALID_PERSONAS else "JARVIS"
