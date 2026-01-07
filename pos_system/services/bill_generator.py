from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import datetime
import os


class BillGenerator:
    """Generate thermal receipt style bills (black & white only)"""
    
    def __init__(self, bills_folder='bills'):
        self.bills_folder = bills_folder
        os.makedirs(bills_folder, exist_ok=True)
    
    def generate_bill(self, bill_data, items, customer_data):
        """Generate thermal style receipt bill - black & white only"""
        
        filename = f"BILL_{bill_data['bill_number']}.pdf"
        filepath = os.path.join(self.bills_folder, filename)
        
        # Thermal receipt size: narrow width (80mm)
        page_width = 80 * mm
        page_height = 297 * mm
        
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=(page_width, page_height),
            leftMargin=5*mm,
            rightMargin=5*mm,
            topMargin=5*mm,
            bottomMargin=5*mm
        )
        
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Header style - black text only
        header_style = ParagraphStyle(
            'BillHeader',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=2,
            fontName='Helvetica-Bold'
        )
        
        subheader_style = ParagraphStyle(
            'BillSubheader',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=1
        )
        
        normal_style = ParagraphStyle(
            'BillNormal',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            leading=10
        )
        
        bold_style = ParagraphStyle(
            'BillBold',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            leading=10
        )
        
        # Logo - Black & White version
        logo_path = os.path.join('assets', 'logos', 'App logo.jpg')
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=30*mm, height=30*mm)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 2*mm))
            except:
                pass
        
        # Studio name
        story.append(Paragraph("<b>SHINE ART STUDIO</b>", header_style))
        story.append(Paragraph("Photography Services", subheader_style))
        
        # Address and phone (replace with actual values)
        story.append(Paragraph("Address: [Your Address Here]", subheader_style))
        story.append(Paragraph("Phone: [Your Phone]", subheader_style))
        story.append(Spacer(1, 3*mm))
        
        # Separator
        story.append(Paragraph("=" * 40, subheader_style))
        story.append(Spacer(1, 2*mm))
        
        # Bill info
        story.append(Paragraph(f"<b>Bill No: {bill_data['bill_number']}</b>", bold_style))
        story.append(Paragraph(f"Date: {bill_data['created_at']}", normal_style))
        story.append(Paragraph(f"Customer: {customer_data['full_name']}", normal_style))
        
        if customer_data.get('mobile_number') and customer_data['mobile_number'] != 'Guest Customer':
            story.append(Paragraph(f"Mobile: {customer_data['mobile_number']}", normal_style))
        
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("-" * 40, subheader_style))
        story.append(Spacer(1, 2*mm))
        
        # Items
        for idx, item in enumerate(items, 1):
            item_name = item['item_name']
            qty = item['quantity']
            price = item['unit_price']
            total = item['total_price']
            
            story.append(Paragraph(f"<b>{item_name}</b>", bold_style))
            story.append(Paragraph(f"  {qty} x Rs.{price:.2f} = Rs.{total:.2f}", normal_style))
        
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("-" * 40, subheader_style))
        story.append(Spacer(1, 2*mm))
        
        # Totals
        subtotal = bill_data['subtotal']
        service_charge = bill_data.get('service_charge', 0) or 0
        discount = bill_data['discount']
        total = bill_data['total_amount']
        
        story.append(Paragraph(f"Subtotal: Rs.{subtotal:.2f}", normal_style))
        
        if service_charge > 0:
            story.append(Paragraph(f"Service Charge: Rs.{service_charge:.2f}", normal_style))
        
        if discount > 0:
            story.append(Paragraph(f"Discount: Rs.{discount:.2f}", normal_style))
        
        story.append(Paragraph(f"<b>Total: Rs.{total:.2f}</b>", bold_style))
        
        # Cash handling (display only)
        cash_given = bill_data.get('cash_given', 0) or 0
        if cash_given > 0:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph(f"Cash Given: Rs.{cash_given:.2f}", normal_style))
            
            balance = cash_given - total
            if balance > 0:
                story.append(Paragraph(f"Balance: Rs.{balance:.2f}", normal_style))
            elif balance < 0:
                story.append(Paragraph(f"Balance Due: Rs.{abs(balance):.2f}", normal_style))
        
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph("=" * 40, subheader_style))
        story.append(Spacer(1, 2*mm))
        
        # Footer
        footer_style = ParagraphStyle(
            'BillFooter',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("Thank you! Come again.", footer_style))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(f"Served by: {bill_data.get('created_by_name', 'Staff')}", subheader_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def open_bill(self, filepath):
        """Open bill in default PDF viewer"""
        try:
            os.startfile(filepath)
            return True
        except Exception as e:
            print(f"Error opening bill: {e}")
            return False
    
    def print_bill(self, filepath):
        """Print the bill using system default printer"""
        try:
            os.startfile(filepath, 'print')
            return True
        except Exception as e:
            print(f"Error printing bill: {e}")
            return False
