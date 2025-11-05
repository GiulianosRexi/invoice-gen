# Invoice Generator

A professional invoice generator for contractors working with Rexo, Inc. Generates PDF invoices with sequential numbering, contractor details, and payment information.

## Quick Start with Claude Code

This repository is optimized for use with Claude Code. Simply clone it and ask Claude to help you get started!

```bash
git clone <repository-url>
cd invoice-gen
```

Then in Claude Code, say:

> **"Claude, help me set up the invoice generator"**

Claude will read the `CLAUDE.md` file and guide you through:
1. Setting up your environment
2. Running onboarding to configure your personal details
3. Creating your first invoice

## Monthly Invoice Generation

Once set up, generating invoices each month is simple. Just tell Claude:

> **"Claude, generate this month's invoice for $500"**

Claude will automatically:
- Determine the current month and dates
- Use your saved template
- Generate the invoice with the correct numbering

## Features

- **Sequential Invoice Numbering**: Automatic 0001, 0002, 0003... format
- **Template System**: Save recurring details, only provide amount and period each month
- **Professional PDF Output**: Clean, formatted invoices ready to send
- **Dolarapp Integration**: Payment instructions with dolartag
- **USD Currency**: Clear currency labeling with "no U.S. withholding" disclaimer

## What's Included

- Invoice generator with CLI and interactive modes
- Onboarding script for first-time setup
- Template system for recurring invoices
- Sequential invoice numbering
- Professional PDF formatting

## Manual Setup (Without Claude)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Onboarding

```bash
python onboard.py
```

You'll be asked for:
- Starting invoice number
- Your full name
- Your CUIL number
- Your Dolarapp dolartag
- Your tax status (optional)

### 4. Generate Invoices

```bash
python invoice_generator.py \
  --use-template "rexo" \
  --amount 500 \
  --service-period "Services provided during January 2025" \
  --issue-date "2025-01-31" \
  --output "invoice_january_2025.pdf"
```

## Repository Structure

```
invoice-gen/
├── CLAUDE.md                # Instructions for Claude (context file)
├── README.md                # This file
├── invoice_generator.py     # Main invoice generation script
├── onboard.py              # Onboarding script
├── requirements.txt        # Python dependencies
├── .gitignore             # Excludes personal data
├── invoice_data.json      # Your personal data (created during onboarding)
└── venv/                  # Python virtual environment (local)
```

## Common Commands

### Generate Invoice
```bash
python invoice_generator.py \
  --use-template "rexo" \
  --amount 500 \
  --service-period "Services provided during November 2025" \
  --issue-date "2025-11-30" \
  --output "invoice_november_2025.pdf"
```

### List Templates
```bash
python invoice_generator.py --list-templates
```

### Get Help
```bash
python invoice_generator.py --help
```

## Invoice Details

Each invoice includes:
- Sequential invoice number (0001, 0002, etc.)
- Issue date
- Contractor information (name, CUIL, tax status)
- Client information (Rexo, Inc. details)
- Service description and period
- Amount in USD
- Payment instructions (Dolarapp with dolartag)
- "Services performed outside the U.S.; no U.S. withholding applies" disclaimer

## Security

- `invoice_data.json` contains your personal details and is excluded from git
- Generated PDFs are also excluded from git
- Each user maintains their own invoice counter (no conflicts between team members)

## Adjusting Invoice Number

If you need to change your starting invoice number (e.g., you already generated invoices elsewhere):

1. Edit `invoice_data.json`
2. Change `last_invoice_number` to one less than your desired next invoice
   - For invoice #0005, set it to 4
   - For invoice #0010, set it to 9

## Support

For questions or issues:
1. Ask Claude (if using Claude Code)
2. Check the `CLAUDE.md` file for detailed technical information
3. Review command-line help: `python invoice_generator.py --help`

## License

MIT
