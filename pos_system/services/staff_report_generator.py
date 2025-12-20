from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os


class StaffReportGenerator:
    """Generate PDF reports for staff daily work records"""
    
    def __init__(self, report_folder='reports'):
        self.report_folder = report_folder
        os.makedirs(report_folder, exist_ok=True)
    
    def generate_daily_report(self, staff_data: dict, date: str, work_records: dict):
        """Generate PDF report for staff daily work
        
        Args:
            staff_data: dict with staff info (id, full_name, username, role)
            date: Date string (YYYY-MM-DD)
            work_records: dict with invoices, bookings, customers data
        """
        
        # Create filename
        safe_name = staff_data['full_name'].replace(' ', '_')
        filename = f"Staff_Report_{safe_name}_{date}.pdf"
        filepath = os.path.join(self.report_folder, filename)
        
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
            spaceAfter=10,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.grey
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f538d'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        normal_style = styles["Normal"]
        
        # Header - Studio name
        story.append(Paragraph("Shine Art Studio", title_style))
        story.append(Paragraph("Staff Daily Work Report", subtitle_style))
        
        # Report info box
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", normal_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Staff info section
        story.append(Paragraph("Staff Information", heading_style))
        
        staff_info_data = [
            ['Staff Name:', staff_data['full_name']],
            ['Username:', f"@{staff_data['username']}"],
            ['Role:', staff_data.get('role', 'Staff')],
            ['Report Date:', date],
        ]
        
        staff_table = Table(staff_info_data, colWidths=[2*inch, 4*inch])
        staff_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(staff_table)
        
        # Summary section
        story.append(Paragraph("Daily Summary", heading_style))
        
        invoices = work_records.get('invoices', [])
        bookings = work_records.get('bookings', [])
        customers = work_records.get('customers', [])
        
        total_invoice_amount = sum(inv.get('total_amount', 0) for inv in invoices)
        total_paid = sum(inv.get('paid_amount', 0) for inv in invoices)
        total_booking_amount = sum(b.get('full_amount', 0) for b in bookings)
        total_advance = sum(b.get('advance_payment', 0) for b in bookings)
        
        summary_data = [
            ['Metric', 'Count', 'Amount (LKR)'],
            ['Invoices Created', str(len(invoices)), f"{total_invoice_amount:,.2f}"],
            ['Payments Received', '-', f"{total_paid:,.2f}"],
            ['Bookings Created', str(len(bookings)), f"{total_booking_amount:,.2f}"],
            ['Advance Collected', '-', f"{total_advance:,.2f}"],
            ['Customers Added', str(len(customers)), '-'],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f538d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(summary_table)
        
        # Invoices detail section
        if invoices:
            story.append(Paragraph("Invoices Created", heading_style))
            
            inv_data = [['#', 'Invoice No.', 'Customer', 'Total (LKR)', 'Paid (LKR)', 'Time']]
            for idx, inv in enumerate(invoices, 1):
                created_time = inv.get('created_at', '')
                if ' ' in created_time:
                    created_time = created_time.split(' ')[1][:5]  # Get HH:MM
                inv_data.append([
                    str(idx),
                    inv.get('invoice_number', '-'),
                    inv.get('customer_name', '-')[:20],
                    f"{inv.get('total_amount', 0):,.2f}",
                    f"{inv.get('paid_amount', 0):,.2f}",
                    created_time
                ])
            
            inv_table = Table(inv_data, colWidths=[0.4*inch, 1.2*inch, 1.8*inch, 1.2*inch, 1.2*inch, 0.8*inch])
            inv_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f5e9')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(inv_table)
        else:
            story.append(Paragraph("Invoices Created", heading_style))
            story.append(Paragraph("<i>No invoices created on this date.</i>", normal_style))
        
        # Bookings detail section
        if bookings:
            story.append(Paragraph("Bookings Created", heading_style))
            
            book_data = [['#', 'Customer', 'Category', 'Date', 'Amount (LKR)', 'Advance (LKR)']]
            for idx, b in enumerate(bookings, 1):
                book_data.append([
                    str(idx),
                    b.get('customer_name', '-')[:18],
                    b.get('photoshoot_category', '-')[:15],
                    b.get('booking_date', '-'),
                    f"{b.get('full_amount', 0):,.2f}",
                    f"{b.get('advance_payment', 0):,.2f}"
                ])
            
            book_table = Table(book_data, colWidths=[0.4*inch, 1.4*inch, 1.2*inch, 1*inch, 1.2*inch, 1.2*inch])
            book_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e3f2fd')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(book_table)
        else:
            story.append(Paragraph("Bookings Created", heading_style))
            story.append(Paragraph("<i>No bookings created on this date.</i>", normal_style))
        
        # Customers added section
        if customers:
            story.append(Paragraph("Customers Added", heading_style))
            
            cust_data = [['#', 'Customer Name', 'Mobile Number', 'Added At']]
            for idx, c in enumerate(customers, 1):
                created_time = c.get('created_at', '')
                if ' ' in created_time:
                    created_time = created_time.split(' ')[1][:5]
                cust_data.append([
                    str(idx),
                    c.get('full_name', '-'),
                    c.get('mobile_number', '-'),
                    created_time
                ])
            
            cust_table = Table(cust_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
            cust_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3e5f5')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(cust_table)
        else:
            story.append(Paragraph("Customers Added", heading_style))
            story.append(Paragraph("<i>No customers added on this date.</i>", normal_style))
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("─" * 60, ParagraphStyle('Line', alignment=TA_CENTER)))
        story.append(Paragraph(
            "This report was automatically generated by Shine Art Studio POS System",
            ParagraphStyle('Footer', parent=normal_style, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
        ))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def open_report(self, filepath):
        """Open report in default PDF viewer"""
        try:
            os.startfile(filepath)
            return True
        except Exception as e:
            print(f"Error opening report: {e}")
            return False
