from fpdf import FPDF
from datetime import datetime
import tempfile
import io
from fastapi import UploadFile

class PDFWithBackground(FPDF):
    def header(self):
        # Set full-page A4 background image
        self.image("app/assets/recipt_base.jpg", x=0, y=0, w=210, h=297)

def generate_receipt_pdf(project, data):
    """
    Generate a PDF receipt with enhanced formatting
    """
    # Extract the nested payload
    payload_data = data.get("payload", {})
    integrity = payload_data.get("integrity", [])[0] if payload_data.get("integrity") else {}

    # Generate PDF receipt
    pdf = PDFWithBackground()
    pdf.add_page()
    
    # Set starting position lower on the page
    pdf.set_y(37)
    
    # Title
    pdf.set_font("Arial", "B", size=16)  # B = Bold, larger font
    pdf.cell(0, 10, txt="Registration Receipt", ln=True, align='C')
    
    # Horizontal line
    pdf.line(20, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)  # Add small space after line
    
    # Date and basic info
    pdf.set_font("Arial", "", size=11)
    pdf.cell(0, 8, txt="Musicdibs guarantees that the following document has been registered in a blockchain.", ln=True)
    
    pdf.cell(37, 8, txt="Registerd at: ")
    pdf.multi_cell(0, 8, txt=datetime.now().strftime('%Y-%m-%d'))
    
    pdf.cell(37, 8, txt=f"Project name: ")
    pdf.multi_cell(0, 8, txt=project.name)
    
    # Get user name if possible
    if hasattr(project, 'user') and project.user:
        author = f"{project.user.first_name} {project.user.last_name}"
    else:
        author = f"ID: {project.user_id}"
    pdf.cell(37, 8, txt="Author: ")
    pdf.multi_cell(0, 8, txt=author) 

    pdf.cell(37, 8, txt=f"Project description: ")
    pdf.multi_cell(0, 8, txt=project.description)
    
    # Content data section
    pdf.ln(5)
    pdf.set_font("Arial", "B", size=13)
    pdf.cell(0, 10, txt="Content Data", ln=True)
    pdf.set_font("Arial", "", size=11)
    
    # Safely access the integrity data
    if integrity:
        pdf.cell(37, 8, txt="File name: ")
        pdf.multi_cell(0, 8, txt=integrity.get('name', 'N/A'))

        # For long checksums, use multi_cell which handles word wrapping
        pdf.cell(37, 8, txt="File checksum: ")
        checksum = integrity.get('checksum', 'N/A')
        current_x = pdf.get_x()
        current_y = pdf.get_y()
        pdf.multi_cell(0, 8, txt=checksum)
        
        # Algorithm info
        algo_text = f"{integrity.get('sanitizer', 'N/A')} {integrity.get('algorithm', 'N/A')}"
        pdf.cell(37, 8, txt="Algorithm: ")
        pdf.multi_cell(0, 8, txt=algo_text)
    
    # Blockchain section
    pdf.ln(5)
    pdf.set_font("Arial", "B", size=13)
    pdf.cell(0, 10, txt="Blockchain Registration Data", ln=True)
    pdf.set_font("Arial", "", size=11)
    
    # For transaction hash, use multi_cell for word wrapping
    pdf.cell(37, 8, txt="Transaction hash: ")
    tx_hash = data.get('certification_hash', 'N/A')
    current_x = pdf.get_x()
    current_y = pdf.get_y()
    pdf.multi_cell(0, 8, txt=tx_hash)
    
    # Network info
    pdf.cell(37, 8, txt="Blockchain network: ")
    pdf.multi_cell(0, 8, txt=data.get('network', 'N/A'))

    # Timestamp
    timestamp = data.get('certification_timestamp', '')
    if timestamp:
        cleaned = timestamp.split(".")[0]
        dt = datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%S")
        formatted_time = dt.strftime("%Y/%m/%d %H:%M:%S")
        pdf.cell(37, 8, txt="Timestamp: ")
        pdf.multi_cell(0, 8, txt=formatted_time)
    else:
        pdf.cell(37, 8, txt="Timestamp: ")
        pdf.multi_cell(0, 8, txt="N/A")
    
    # Add another horizontal line at the bottom
    pdf.ln(5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    
    # Footer with verification info
    pdf.ln(10)
    pdf.set_font("Arial", "I", size=9)  # I = Italic
    verification_url = data.get('checker_url', 'N/A')
    pdf.cell(0, 8, txt="Verify this registration at: ", ln=True)
    pdf.cell(0, 5, txt=verification_url)
    
    # Save PDF to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        pdf_path = temp_file.name
        pdf.output(pdf_path)
    
    # Create UploadFile object from the PDF
    with open(pdf_path, 'rb') as pdf_file:
        upload_file_obj = UploadFile(
            filename=f"receipt_{data.get('evidence_id', 'unknown')}.pdf",
            file=io.BytesIO(pdf_file.read()),
        )
    
    return upload_file_obj