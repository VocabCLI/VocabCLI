from fpdf import FPDF
from datetime import datetime
from Database import createConnection
from ImportExport import PDF


def learning_rate():
    pass

def generate_text_report():
    pdf=PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica","", size=12)
    conn= createConnection()
    c=conn.cursor()
    pdf.output("TextReport.pdf")

def generate_graph_report():
    pdf=PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica","", size=12)
    conn= createConnection()
    c=conn.cursor()
    pdf.output("TextReport.pdf")
    pdf.output("GraphReport.pdf")
    


generate_graph_report()
generate_text_report()