from pydantic import BaseModel, Field, field_validator

# Allowed personas
VALID_PERSONAS = {"JARVIS", "ULTRON", "GOD", "REAPER", "FRIDAY"}


class MissionRequest(BaseModel):
    command: str = Field(
        ...,
        min_length=2,
        description="User command or instruction to the AI system"
    )
    persona: str = Field(
        default="JARVIS",
        description="AI persona mode"
    )

    # -------- Persona Validator ----------
    @field_validator("persona", mode="before")
    @classmethod
    def normalize_persona(cls, v):
        if not v:
            return "JARVIS"

        v = str(v).upper().strip()
        return v if v in VALID_PERSONAS else "JARVIS"

    # -------- Command Validator ----------
    @field_validator("command", mode="before")
    @classmethod
    def clean_command(cls, v):
        if not v or not str(v).strip():
            raise ValueError("Command cannot be empty.")
        return str(v).strip()
