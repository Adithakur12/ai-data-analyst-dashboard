from fpdf import FPDF
import datetime

class ReportGenerator:
    def generate(self, query, insight, df, fig):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AI Business Intelligence Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, f"Query: {query}\n\nInsight: {insight}")
        
        fig.write_image("temp_chart.png")
        pdf.image("temp_chart.png", x=10, w=180)
        
        path = "data/business_report.pdf"
        pdf.output(path)
        return path