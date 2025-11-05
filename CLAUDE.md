# Instructions for Claude

This file provides context about the invoice generator system and how to assist users with setup and monthly invoice generation.

## System Overview

This is an invoice generator for contractors working with **Rexo, Inc.** It generates professional PDF invoices with:
- Sequential invoice numbering (0001, 0002, etc.)
- Contractor details (name, CUIL, payment info)
- Client details (Rexo, Inc. information)
- Service descriptions and periods
- Payment instructions via Dolarapp
- USD currency with "no U.S. withholding" disclaimer

## Default Client Information

**Rexo, Inc.** (default template client):
- Company Name: Rexo, Inc.
- Address: 251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808
- EIN: 33-2631448

## Repository Structure

```
invoice-gen/
├── CLAUDE.md                 # This file - instructions for Claude
├── README.md                 # User-facing documentation
├── invoice_generator.py      # Main invoice generation script
├── onboard.py               # Onboarding script for new users
├── requirements.txt         # Python dependencies (reportlab)
├── .gitignore              # Excludes personal data and generated PDFs
├── invoice_data.json       # User's personal data (created during onboarding)
└── venv/                   # Python virtual environment (local)
```

## Key Concepts

### Templates
Templates store recurring invoice details (contractor info, client info, payment details) so users only need to provide the changing details each month (amount, service period, date).

### Invoice Numbering
Sequential numbering is maintained in `invoice_data.json`. Each user maintains their own counter independently.

### Onboarding
New users must run `onboard.py` to set up their personal details and create their first template.

## When a User Clones This Repository

### First-Time Setup

If the user just cloned the repository and `invoice_data.json` doesn't exist:

1. **Check for virtual environment**:
   ```bash
   ls venv/
   ```

2. **If venv doesn't exist, create it**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **If venv exists, just activate it**:
   ```bash
   source venv/bin/activate
   ```

4. **Run onboarding** and ask for:
   - Starting invoice number (default: 1)
   - Full name
   - CUIL number
   - Dolarapp account holder name (default: same as full name)
   - Dolarapp dolartag (starts with $)
   - Argentine tax status (optional: monotributista/autónomo)

5. **Ask about Rexo template** (default: yes):
   "Would you like to create a template for Rexo, Inc.? This will save their client information for quick monthly invoice generation. [Y/n]"

   If yes (default), create template named "rexo" with:
   - Client info: Rexo, Inc. details from above
   - Contractor info: from onboarding
   - Service description: "Contractor services - Software Engineer"

6. **Show them how to generate their first invoice**:
   ```bash
   python invoice_generator.py \
     --use-template "rexo" \
     --amount 500 \
     --service-period "Services provided during [Month] 2025" \
     --issue-date "2025-[MM]-[DD]" \
     --output "invoice_[month]_2025.pdf"
   ```

### If User Has Existing invoice_data.json

If `invoice_data.json` exists, the user is already set up. Check if they want to:
- Generate a new invoice (most common)
- View their current invoice number
- Adjust their starting invoice number
- View/manage templates

## Monthly Invoice Generation

### Simple Prompt Pattern

When a user says something like:
- "Claude, generate this month's invoice for $500"
- "Generate my November invoice for 3500"
- "Create an invoice for $4200 for October"

**Your response should**:

1. **Check for setup**:
   - Virtual environment activated?
   - `invoice_data.json` exists?
   - If not, run onboarding first

2. **Determine the details**:
   - Amount: from user's message
   - Month: from user's message or current month if not specified
   - Service period: "Services provided during [Month] [Year]"
   - Issue date: Last day of the month or first day of next month (ask if unclear)
   - Output filename: `invoice_[month]_[year].pdf`

3. **Check for template**:
   - If "rexo" template exists (most common), use it
   - If not, ask if they want to use a template or provide full details

4. **Generate the invoice**:
   ```bash
   python invoice_generator.py \
     --use-template "rexo" \
     --amount [AMOUNT] \
     --service-period "Services provided during [Month] [Year]" \
     --issue-date "[YYYY-MM-DD]" \
     --output "invoice_[month]_[year].pdf"
   ```

5. **Confirm success** and tell them:
   - Invoice number generated
   - Filename
   - Location

### Example Interaction

```
User: Claude, generate this month's invoice for $500

You: I'll generate your invoice for November 2025.

[Run command]

✓ Invoice #0003 generated successfully: invoice_november_2025.pdf

Your invoice has been created with:
- Amount: $5,000 USD
- Period: Services provided during November 2025
- Issue Date: November 30, 2025
- Invoice Number: 0003
```

## Common Operations

### Generate Invoice
```bash
python invoice_generator.py \
  --use-template "rexo" \
  --amount 500 \
  --service-period "Services provided during January 2025" \
  --issue-date "2025-01-31" \
  --output "invoice_january_2025.pdf"
```

### List Templates
```bash
python invoice_generator.py --list-templates
```

### View Help
```bash
python invoice_generator.py --help
```

### Adjust Invoice Number

If user wants to set the invoice number (e.g., they already generated invoices elsewhere):

1. **Read current state**:
   ```bash
   cat invoice_data.json
   ```

2. **Explain**: The `last_invoice_number` field stores the last used number. To start at invoice #0005, set it to 4.

3. **Edit the file**:
   ```json
   {
     "last_invoice_number": 4,
     "templates": { ... }
   }
   ```

## Important Notes

### Security
- `invoice_data.json` contains personal details - never commit or share
- `.gitignore` already excludes it
- Generated PDFs are also excluded from git

### Invoice Numbers
- Sequential and auto-incrementing
- Stored per user (no conflicts between team members)
- Format: 0001, 0002, 0003, etc.

### Templates
- Save time on monthly invoices
- Store everything except: amount, service period, issue date
- Can have multiple templates for different clients
- "rexo" is the standard template name for Rexo, Inc.

### Date Formats
- Issue date: YYYY-MM-DD (e.g., 2025-01-31)
- Service period: Free text (e.g., "Services provided during January 2025")

## Troubleshooting

### "No module named 'reportlab'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Template 'rexo' not found"
User needs to run onboarding:
```bash
python onboard.py
```

### "Permission denied"
Make scripts executable:
```bash
chmod +x invoice_generator.py onboard.py
```

## Monthly Workflow Summary

For a user who's already set up:

1. User says: "Generate my invoice for $500"
2. You determine: month, dates, filename
3. You run: `python invoice_generator.py --use-template "rexo" --amount 500 --service-period "Services provided during [Month] [Year]" --issue-date "[YYYY-MM-DD]" --output "invoice_[month]_[year].pdf"`
4. You confirm: invoice number and filename

That's it! The whole process should take seconds.

## Proactive Behaviors

- If it's near the end of the month, you can remind them: "Would you like to generate this month's invoice?"
- If you notice they haven't generated an invoice for the current month yet, offer to help
- If they mention a payment or work period, offer to generate the corresponding invoice
