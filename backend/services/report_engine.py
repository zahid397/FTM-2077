import os
import uuid
from fpdf import FPDF
from datetime import datetime
from backend.config import settings


class ReportEngine:

    def __init__(self):
        # Ensure report folder exists
        os.makedirs(settings.REPORT_DIR, exist_ok=True)

    def create_mission_report(self, data):
        # -------------------------------
        # 1. SAFE DATA EXTRACT
        # -------------------------------
        rid = str(uuid.uuid4())[:8]
        command = data.get("command", "UNKNOWN COMMAND")
        persona = data.get("persona", "UNKNOWN")
        analysis = data.get("analysis", "No analysis available.")
        probability = data.get("probability", "N/A")

        # -------------------------------
        # 2. PDF OBJECT
        # -------------------------------
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=12)
        pdf.add_page()

        # Safe fallback font (Latin only)
        pdf.set_font("Arial", size=12)

        # -------------------------------
        # 3. HEADER
        # -------------------------------
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, f"FTM-2077 // Tactical Report [{rid}]", ln=True, align="C")

        pdf.set_font("Arial", size=11)
        pdf.ln(4)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", style="B", size=13)
        pdf.cell(0, 10, "Mission Summary", ln=True)

        # -------------------------------
        # 4. MISSION INFO
        # -------------------------------
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8,
            f"Command Input: {command}\n"
            f"Persona Used: {persona}\n"
            f"Prediction Probability: {probability}%"
        )

        pdf.ln(4)
        pdf.set_font("Arial", style="B", size=13)
        pdf.cell(0, 10, "AI Analysis", ln=True)

        # -------------------------------
        # 5. ANALYSIS TEXT
        # -------------------------------
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 7, analysis)

        # -------------------------------
        # 6. SAVE FILE
        # -------------------------------
        file_path = os.path.join(settings.REPORT_DIR, f"{rid}.pdf")

        try:
            pdf.output(file_path)
        except Exception as e:
            print(f"[PDF ERROR] {e}")
            return {"path": None, "report_id": rid, "error": str(e)}

        return {"path": file_path, "report_id": rid}


# Global instance
report_engine = ReportEngine()
