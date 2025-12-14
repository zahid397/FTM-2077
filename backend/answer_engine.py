import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_answer(command, persona="JARVIS"):
    system_prompt = f"""
You are {persona}.
You respond like a real intelligent system.
No logs. No brackets. No symbols.
Give direct human-like answers.
"""

    response = model.generate_content(
        system_prompt + "\nUser: " + command
    )

    return response.text
