from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os


class InvoiceGenerator:
    """Generate PDF invoices using ReportLab"""
    
    def __init__(self, invoice_folder='invoices'):
        self.invoice_folder = invoice_folder
        # Create invoices folder if it doesn't exist
        os.makedirs(invoice_folder, exist_ok=True)
    
    def generate_invoice(self, invoice_data, items, customer_data):
        """Generate PDF invoice"""
        
        # Create filename
        filename = f"{invoice_data['invoice_number']}.pdf"
        filepath = os.path.join(self.invoice_folder, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f538d'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f538d'),
            spaceAfter=12
        )
        
        normal_style = styles["Normal"]
        
        # Header - Studio name
        story.append(Paragraph("Shine Art Studio", title_style))
        story.append(Paragraph("Photography Services", ParagraphStyle(
            'Subtitle',
            parent=normal_style,
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20
        )))
        
        # Invoice details
        story.append(Paragraph(f"<b>Invoice Number:</b> {invoice_data['invoice_number']}", normal_style))
        story.append(Paragraph(f"<b>Date:</b> {invoice_data['created_at']}", normal_style))
        story.append(Paragraph(f"<b>Created By:</b> {invoice_data['created_by_name']}", normal_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # Customer details
        story.append(Paragraph("Customer Details", heading_style))
        story.append(Paragraph(f"<b>Name:</b> {customer_data['full_name']}", normal_style))
        story.append(Paragraph(f"<b>Mobile:</b> {customer_data['mobile_number']}", normal_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # Items table
        story.append(Paragraph("Invoice Items", heading_style))
        
        # Table data
        table_data = [['#', 'Item', 'Type', 'Qty', 'Unit Price (LKR)', 'Total (LKR)']]
        
        for idx, item in enumerate(items, 1):
            table_data.append([
                str(idx),
                item['item_name'],
                item['item_type'],
                str(item['quantity']),
                f"{item['unit_price']:.2f}",
                f"{item['total_price']:.2f}"
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1*inch, 0.7*inch, 1.3*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f538d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Payment details
        story.append(Paragraph("Payment Details", heading_style))
        
        payment_data = [
            ['Subtotal:', f"LKR {invoice_data['subtotal']:.2f}"],
            ['Discount:', f"LKR {invoice_data['discount']:.2f}"],
            ['<b>Total Amount:</b>', f"<b>LKR {invoice_data['total_amount']:.2f}</b>"],
            ['Paid Amount:', f"LKR {invoice_data['paid_amount']:.2f}"],
            ['<b>Balance:</b>', f"<b>LKR {invoice_data['balance_amount']:.2f}</b>"]
        ]
        
        payment_table = Table(payment_data, colWidths=[3*inch, 2*inch])
        payment_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
            ('LINEABOVE', (0, 4), (-1, 4), 1, colors.black),
        ]))
        
        story.append(payment_table)
        story.append(Spacer(1, 0.5 * inch))
        
        # Footer
        story.append(Paragraph("Thank you for your business!", ParagraphStyle(
            'Footer',
            parent=normal_style,
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def open_invoice(self, filepath):
        """Open invoice in default PDF viewer"""
        try:
            os.startfile(filepath)
            return True
        except Exception as e:
            print(f"Error opening invoice: {e}")
            return False
