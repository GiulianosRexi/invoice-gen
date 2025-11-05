#!/usr/bin/env python3
"""
Invoice Generator
Generates professional invoices in PDF format with interactive or CLI argument modes.
"""

import argparse
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


class InvoiceNumberManager:
    """Manages sequential invoice numbering and invoice templates."""

    def __init__(self, data_file='invoice_data.json'):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self):
        """Load invoice data from JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {'last_invoice_number': 0, 'templates': {}}

    def _save_data(self):
        """Save invoice data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_next_invoice_number(self):
        """Get the next invoice number and increment the counter."""
        self.data['last_invoice_number'] += 1
        self._save_data()
        return f"{self.data['last_invoice_number']:04d}"

    def get_current_invoice_number(self):
        """Get the current invoice number without incrementing."""
        return f"{self.data['last_invoice_number']:04d}"

    def save_template(self, name, template_data):
        """Save an invoice template."""
        if 'templates' not in self.data:
            self.data['templates'] = {}
        self.data['templates'][name] = template_data
        self._save_data()

    def load_template(self, name):
        """Load an invoice template by name."""
        if 'templates' not in self.data:
            return None
        return self.data['templates'].get(name)

    def list_templates(self):
        """List all available template names."""
        if 'templates' not in self.data:
            return []
        return list(self.data['templates'].keys())


class InvoiceGenerator:
    """Generates PDF invoices."""

    def __init__(self, invoice_data):
        self.invoice_data = invoice_data

    def generate_pdf(self, filename):
        """Generate the invoice PDF."""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        # Container for the 'Flowable' objects
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            spaceBefore=12
        )

        normal_style = styles['Normal']

        # Title
        title = Paragraph("INVOICE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        # Invoice header information
        header_data = [
            ['Invoice Number:', self.invoice_data['invoice_number']],
            ['Issue Date:', self.invoice_data['issue_date']],
            ['Currency:', 'USD']
        ]

        header_table = Table(header_data, colWidths=[2 * inch, 4 * inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(header_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Two-column layout for From/To
        from_to_data = []

        # Contractor (From) section
        from_section = []
        from_section.append(Paragraph("<b>From:</b>", heading_style))
        if self.invoice_data.get('contractor_name'):
            from_section.append(Paragraph(self.invoice_data['contractor_name'], normal_style))
        if self.invoice_data.get('contractor_cuil'):
            from_section.append(Paragraph(f"CUIL: {self.invoice_data['contractor_cuil']}", normal_style))
        if self.invoice_data.get('contractor_tax_status'):
            from_section.append(Paragraph(f"Tax Status: {self.invoice_data['contractor_tax_status']}", normal_style))

        # Bill To section
        to_section = []
        to_section.append(Paragraph("<b>Bill To:</b>", heading_style))
        if self.invoice_data.get('client_name'):
            to_section.append(Paragraph(self.invoice_data['client_name'], normal_style))
        if self.invoice_data.get('client_address'):
            to_section.append(Paragraph(self.invoice_data['client_address'], normal_style))
        if self.invoice_data.get('client_ein'):
            to_section.append(Paragraph(f"EIN: {self.invoice_data['client_ein']}", normal_style))

        # Add both sections if either has content
        if from_section or to_section:
            # Create a table with two columns for From and To
            from_cell = []
            for item in from_section:
                from_cell.append(item)
                from_cell.append(Spacer(1, 0.05 * inch))

            to_cell = []
            for item in to_section:
                to_cell.append(item)
                to_cell.append(Spacer(1, 0.05 * inch))

            # Manually add the sections
            for item in from_section:
                elements.append(item)

            elements.append(Spacer(1, 0.15 * inch))

            for item in to_section:
                elements.append(item)

            elements.append(Spacer(1, 0.2 * inch))

        # Line items
        line_items_heading = Paragraph("<b>Services</b>", heading_style)
        elements.append(line_items_heading)
        elements.append(Spacer(1, 0.1 * inch))

        # Line items table
        line_items_data = [
            ['Description', 'Amount (USD)']
        ]

        # Add the service line item
        description = self.invoice_data.get('service_description', 'Software engineering services')

        # Add service period if provided
        if self.invoice_data.get('service_period'):
            description = f"{description}\n{self.invoice_data['service_period']}"

        amount = f"${self.invoice_data['amount']:,.2f}"
        line_items_data.append([description, amount])

        line_items_table = Table(line_items_data, colWidths=[4.5 * inch, 1.5 * inch])
        line_items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e0e0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(line_items_table)
        elements.append(Spacer(1, 0.15 * inch))

        # Total
        total_data = [
            ['Total:', f"${self.invoice_data['amount']:,.2f}"]
        ]

        total_table = Table(total_data, colWidths=[4.5 * inch, 1.5 * inch])
        total_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        elements.append(total_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Remittance instructions
        remittance_heading = Paragraph("<b>Remittance Instructions</b>", heading_style)
        elements.append(remittance_heading)

        remittance_text = f"""
        <b>Dolarapp Account Information:</b><br/>
        Account Holder: {self.invoice_data['account_holder']}<br/>
        Dolartag: {self.invoice_data['dolartag']}
        """

        if self.invoice_data.get('additional_payment_info'):
            remittance_text += f"<br/>{self.invoice_data['additional_payment_info']}"

        remittance = Paragraph(remittance_text, normal_style)
        elements.append(remittance)
        elements.append(Spacer(1, 0.3 * inch))

        # Important note
        note_style = ParagraphStyle(
            'Note',
            parent=normal_style,
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            borderWidth=1,
            borderColor=colors.HexColor('#cccccc'),
            borderPadding=10,
            spaceAfter=12
        )

        note = Paragraph(
            "<b>Note:</b> Services performed outside the U.S.; no U.S. withholding applies.",
            note_style
        )
        elements.append(note)

        # Build PDF
        doc.build(elements)
        return filename


def interactive_mode():
    """Interactive mode to collect invoice details."""
    print("\n=== Invoice Generator - Interactive Mode ===\n")

    # Get invoice details
    client_name = input("Client name (optional, press Enter to skip): ").strip()
    client_address = input("Client address (optional, press Enter to skip): ").strip()

    # Service description with default
    service_description = input("Service description [Software engineering services]: ").strip()
    if not service_description:
        service_description = "Software engineering services"

    # Amount
    while True:
        try:
            amount_str = input("Invoice amount (USD): ").strip()
            amount = float(amount_str.replace(',', '').replace('$', ''))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    # Issue date with default
    issue_date_str = input(f"Issue date [today: {datetime.now().strftime('%Y-%m-%d')}]: ").strip()
    if not issue_date_str:
        issue_date = datetime.now().strftime('%Y-%m-%d')
    else:
        issue_date = issue_date_str

    # Payment information
    account_holder = input("Account holder name: ").strip()
    dolartag = input("Dolartag: ").strip()
    additional_payment_info = input("Additional payment info (optional, press Enter to skip): ").strip()

    # Output filename
    default_filename = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_filename = input(f"Output filename [{default_filename}]: ").strip()
    if not output_filename:
        output_filename = default_filename

    if not output_filename.endswith('.pdf'):
        output_filename += '.pdf'

    # Get next invoice number
    invoice_manager = InvoiceNumberManager()
    invoice_number = invoice_manager.get_next_invoice_number()

    # Prepare invoice data
    invoice_data = {
        'invoice_number': invoice_number,
        'issue_date': issue_date,
        'client_name': client_name,
        'client_address': client_address,
        'service_description': service_description,
        'amount': amount,
        'account_holder': account_holder,
        'dolartag': dolartag,
        'additional_payment_info': additional_payment_info
    }

    # Generate invoice
    generator = InvoiceGenerator(invoice_data)
    generator.generate_pdf(output_filename)

    print(f"\n✓ Invoice #{invoice_number} generated successfully: {output_filename}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate professional invoices in PDF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode (default):
    python invoice_generator.py

  Argument mode:
    python invoice_generator.py --amount 5000 --account-holder "John Doe" \\
        --dolartag "@johndoe" --client-name "Acme Corp" \\
        --client-address "123 Main St, New York, NY"
        """
    )

    # Optional arguments for CLI mode
    parser.add_argument('--amount', type=float, help='Invoice amount in USD')
    parser.add_argument('--account-holder', help='Account holder name for payment')
    parser.add_argument('--dolartag', help='Dolarapp dolartag')
    parser.add_argument('--client-name', help='Client name')
    parser.add_argument('--client-address', help='Client address')
    parser.add_argument('--client-ein', help='Client EIN (Employer Identification Number)')
    parser.add_argument('--contractor-name', help='Contractor name')
    parser.add_argument('--contractor-cuil', help='Contractor CUIL')
    parser.add_argument('--contractor-tax-status', help='Contractor Argentine tax status (monotributista/autónomo)')
    parser.add_argument('--service-description',
                       default='Contractor services - Software Engineer',
                       help='Service description (default: Contractor services - Software Engineer)')
    parser.add_argument('--service-period', help='Service period (e.g., "Services provided during October 2025")')
    parser.add_argument('--issue-date',
                       help='Issue date (YYYY-MM-DD format, default: today)')
    parser.add_argument('--additional-payment-info',
                       help='Additional payment information')
    parser.add_argument('--output', '-o',
                       help='Output filename (default: invoice_YYYYMMDD_HHMMSS.pdf)')
    parser.add_argument('--save-template', metavar='NAME',
                       help='Save current invoice details as a template with the given name')
    parser.add_argument('--use-template', metavar='NAME',
                       help='Load invoice details from a saved template')
    parser.add_argument('--list-templates', action='store_true',
                       help='List all saved templates and exit')

    args = parser.parse_args()

    # Initialize invoice manager
    invoice_manager = InvoiceNumberManager()

    # Handle --list-templates
    if args.list_templates:
        templates = invoice_manager.list_templates()
        if templates:
            print("\nAvailable templates:")
            for template_name in templates:
                print(f"  - {template_name}")
        else:
            print("\nNo templates saved yet.")
        return 0

    # Load template if specified
    template_data = {}
    if args.use_template:
        template_data = invoice_manager.load_template(args.use_template)
        if template_data is None:
            print(f"Error: Template '{args.use_template}' not found.")
            print("Use --list-templates to see available templates.")
            return 1
        print(f"Loaded template: {args.use_template}")

    # Check if we're in argument mode (at least amount, account_holder, and dolartag provided)
    # When using a template, these can come from the template
    required_from_template = template_data.get('account_holder') and template_data.get('dolartag')
    if (args.amount and args.account_holder and args.dolartag) or (args.amount and required_from_template):
        # Argument mode
        invoice_number = invoice_manager.get_next_invoice_number()

        # Set defaults
        issue_date = args.issue_date if args.issue_date else datetime.now().strftime('%Y-%m-%d')
        output_filename = args.output if args.output else f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        # Merge template data with command-line arguments (command-line takes precedence)
        invoice_data = {
            'invoice_number': invoice_number,
            'issue_date': issue_date,
            'client_name': args.client_name or template_data.get('client_name', ''),
            'client_address': args.client_address or template_data.get('client_address', ''),
            'client_ein': args.client_ein or template_data.get('client_ein', ''),
            'contractor_name': args.contractor_name or template_data.get('contractor_name', ''),
            'contractor_cuil': args.contractor_cuil or template_data.get('contractor_cuil', ''),
            'contractor_tax_status': args.contractor_tax_status or template_data.get('contractor_tax_status', ''),
            'service_description': args.service_description if args.service_description != 'Contractor services - Software Engineer' else template_data.get('service_description', args.service_description),
            'service_period': args.service_period or '',
            'amount': args.amount,
            'account_holder': args.account_holder or template_data.get('account_holder', ''),
            'dolartag': args.dolartag or template_data.get('dolartag', ''),
            'additional_payment_info': args.additional_payment_info or template_data.get('additional_payment_info', '')
        }

        generator = InvoiceGenerator(invoice_data)
        generator.generate_pdf(output_filename)

        print(f"✓ Invoice #{invoice_number} generated successfully: {output_filename}")

        # Save as template if requested
        if args.save_template:
            template_to_save = {
                'client_name': invoice_data['client_name'],
                'client_address': invoice_data['client_address'],
                'client_ein': invoice_data['client_ein'],
                'contractor_name': invoice_data['contractor_name'],
                'contractor_cuil': invoice_data['contractor_cuil'],
                'contractor_tax_status': invoice_data['contractor_tax_status'],
                'service_description': invoice_data['service_description'],
                'account_holder': invoice_data['account_holder'],
                'dolartag': invoice_data['dolartag'],
                'additional_payment_info': invoice_data['additional_payment_info']
            }
            invoice_manager.save_template(args.save_template, template_to_save)
            print(f"✓ Template saved as '{args.save_template}'")
    else:
        # Interactive mode (default)
        if any([args.amount, args.account_holder, args.dolartag]):
            print("Error: When using argument mode, --amount, --account-holder, and --dolartag are all required.")
            print("Use --help for more information, or run without arguments for interactive mode.\n")
            parser.print_help()
            return 1

        interactive_mode()


if __name__ == '__main__':
    main()
