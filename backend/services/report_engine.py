from fpdf import FPDF
import os, uuid
from backend.config import settings
from datetime import datetime

class ReportEngine:
    def create_mission_report(self, data):
        rid = str(uuid.uuid4())[:8]
        command = data.get("command", "UNKNOWN")
        persona = data.get("persona", "UNKNOWN")
        analysis = data.get("analysis", "No analysis.")
        probability = data.get("probability", "N/A")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_title("FTM-2077 Tactical Report")

        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Tactical Mission Report — {rid}", ln=True, align='C')
        
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", ln=True)
        pdf.ln(5)

        # Body
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Mission Details:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"Command: {command}\nPersona: {persona}\nProbability: {probability}%")
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Analysis:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, analysis)

        path = os.path.join(settings.REPORT_DIR, f"{rid}.pdf")
        try:
            pdf.output(path)
        except Exception as e:
            print("PDF Error:", e)
            return {"path": None, "report_id": rid}

        return {"path": path, "report_id": rid}

report_engine = ReportEngine()
