#!/usr/bin/env python3
"""
Onboarding script for new invoice generator users.
Sets up personal details and creates a template for Rexo, Inc.
"""

import json
import os
import sys


def main():
    print("\n" + "="*60)
    print("   Invoice Generator - Onboarding")
    print("="*60)
    print("\nWelcome! This script will help you set up your invoice generator.")
    print("We'll collect your personal details and create a template for")
    print("generating invoices for Rexo, Inc.\n")

    # Check if invoice_data.json exists
    data_file = 'invoice_data.json'
    if os.path.exists(data_file):
        print(f"⚠️  Found existing {data_file}")
        response = input("Do you want to overwrite it? This will reset your invoice counter. (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Onboarding cancelled.")
            return

    # Collect starting invoice number
    print("\n" + "-"*60)
    print("STEP 1: Invoice Numbering")
    print("-"*60)
    while True:
        try:
            start_num = input("\nWhat should your first invoice number be? (e.g., 1 for 0001): ").strip()
            start_num = int(start_num)
            if start_num < 0:
                print("Please enter a non-negative number.")
                continue
            # We store one less because the system increments before generating
            last_invoice_number = start_num - 1
            break
        except ValueError:
            print("Invalid number. Please enter a whole number.")

    # Collect personal details
    print("\n" + "-"*60)
    print("STEP 2: Your Contractor Information")
    print("-"*60)

    contractor_name = input("\nYour full name: ").strip()
    while not contractor_name:
        print("Name is required.")
        contractor_name = input("Your full name: ").strip()

    contractor_cuil = input("Your CUIL number: ").strip()
    while not contractor_cuil:
        print("CUIL is required.")
        contractor_cuil = input("Your CUIL number: ").strip()

    # Payment details
    print("\n" + "-"*60)
    print("STEP 3: Payment Information (Dolarapp)")
    print("-"*60)

    account_holder = input(f"\nDolarapp account holder name [{contractor_name}]: ").strip()
    if not account_holder:
        account_holder = contractor_name

    dolartag = input("Your Dolarapp dolartag (e.g., $username): ").strip()
    while not dolartag:
        print("Dolartag is required.")
        dolartag = input("Your Dolarapp dolartag (e.g., $username): ").strip()

    if not dolartag.startswith('$'):
        print(f"Note: Adding $ prefix to dolartag: ${dolartag}")
        dolartag = f"${dolartag}"

    # Optional tax status
    print("\n" + "-"*60)
    print("STEP 4: Argentine Tax Status (Optional)")
    print("-"*60)
    print("\nOptions: monotributista, autónomo, or leave blank")
    contractor_tax_status = input("Your tax status (optional): ").strip()

    # Create the data structure
    print("\n" + "-"*60)
    print("STEP 5: Creating Template")
    print("-"*60)

    template_data = {
        "client_name": "Rexo, Inc.",
        "client_address": "251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808",
        "client_ein": "33-2631448",
        "contractor_name": contractor_name,
        "contractor_cuil": contractor_cuil,
        "contractor_tax_status": contractor_tax_status,
        "service_description": "Contractor services - Software Engineer",
        "account_holder": account_holder,
        "dolartag": dolartag,
        "additional_payment_info": ""
    }

    invoice_data = {
        "last_invoice_number": last_invoice_number,
        "templates": {
            "rexo": template_data
        }
    }

    # Save to file
    with open(data_file, 'w') as f:
        json.dump(invoice_data, f, indent=2)

    print(f"\n✓ Template 'rexo' created successfully!")
    print(f"✓ Next invoice will be #{start_num:04d}")

    # Show summary
    print("\n" + "="*60)
    print("   Setup Complete!")
    print("="*60)
    print("\nYour configuration:")
    print(f"  Contractor: {contractor_name}")
    print(f"  CUIL: {contractor_cuil}")
    print(f"  Dolartag: {dolartag}")
    print(f"  Next Invoice: #{start_num:04d}")

    # Show usage examples
    print("\n" + "="*60)
    print("   How to Generate Invoices")
    print("="*60)

    print("\n1. Generate a monthly invoice using your template:")
    print("\n   python invoice_generator.py \\")
    print("     --use-template \"rexo\" \\")
    print("     --amount 5000 \\")
    print("     --service-period \"Services provided during January 2025\" \\")
    print("     --issue-date \"2025-01-31\" \\")
    print("     --output \"invoice_january_2025.pdf\"")

    print("\n2. List your templates:")
    print("\n   python invoice_generator.py --list-templates")

    print("\n3. For help:")
    print("\n   python invoice_generator.py --help")

    print("\n" + "="*60)
    print("You're all set! Generate your first invoice using the command above.")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
