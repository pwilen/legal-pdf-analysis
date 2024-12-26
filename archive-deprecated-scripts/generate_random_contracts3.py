import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from faker import Faker

fake = Faker()

# Contract configurations
contract_structure = {
    "CDA": ["introduction", "confidentiality", "liability_cap", "dispute_resolution"],
    "CA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration", "dispute_resolution"],
    "MSA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration", "dispute_resolution"],
    "WO": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "dispute_resolution"]
}

contract_types = ["CDA", "CA", "MSA", "WO"]
jurisdictions = ["Germany", "USA", "Sweden", "France", "UK", "Canada", "Australia"]
currencies = ["USD", "EUR", "GBP", "SEK", "CAD"]
tones = ["neutral", "customer-friendly", "supplier-friendly"]

def get_tone_content(section, tone, **kwargs):
    """Generate content for a clause based on tone."""
    clauses = {
        "introduction": {
            "neutral": "This Agreement is entered into on {date} between {company} (Client) and {counterparty} (Consultant).",
            "customer-friendly": "This mutually beneficial Agreement is established on {date} between {company} (Client) and {counterparty} (Consultant).",
            "supplier-friendly": "This Agreement is effective as of {date} between {company} (Client) and {counterparty} (Consultant)."
        },
        "scope_of_services": {
            "neutral": "The Consultant agrees to provide professional services as described herein, including {services}.",
            "customer-friendly": "The Consultant will diligently deliver services, ensuring Client satisfaction, including {services}.",
            "supplier-friendly": "The Consultant will perform the agreed services as outlined, including {services}."
        },
        "confidentiality": {
            "neutral": "Both Parties shall maintain the confidentiality of all proprietary information shared during this Agreement.",
            "customer-friendly": "The Receiving Party shall take the highest care to protect all Confidential Information provided by the Disclosing Party.",
            "supplier-friendly": "The Receiving Party shall use reasonable efforts to maintain confidentiality of shared information."
        },
        "payment_terms": {
            "neutral": "All payments shall be made within {days} days of invoice receipt.",
            "customer-friendly": "Invoices shall be paid promptly within {days} days to support efficient business operations.",
            "supplier-friendly": "Invoices shall be paid within {days} days, ensuring reasonable processing time."
        },
        "liability_cap": {
            "neutral": "The total liability for claims shall not exceed {amount} {currency}.",
            "customer-friendly": "The Consultant's liability shall remain unlimited for gross negligence or willful misconduct.",
            "supplier-friendly": "The Consultant's total liability is capped at {amount} {currency} in all circumstances."
        },
        "archive_duration": {
            "neutral": "All records shall be retained for {years} years for compliance purposes.",
            "customer-friendly": "The Client agrees to maintain all records for {years} years to ensure regulatory compliance.",
            "supplier-friendly": "The Consultant shall retain all relevant records for {years} years, unless otherwise agreed."
        },
        "dispute_resolution": {
            "neutral": "Disputes shall be governed by the laws of {jurisdiction} and resolved amicably.",
            "customer-friendly": "All disputes shall be resolved in favor of achieving a fair and just outcome under {jurisdiction} law.",
            "supplier-friendly": "Any disputes shall be resolved through arbitration in {jurisdiction}."
        }
    }
    content = clauses[section][tone]
    return content.format(**kwargs)

def generate_contract(output_folder, company_name, counterparty, contract_type, tone):
    """Generate a logically structured contract PDF."""
    company_folder = os.path.join(output_folder, company_name.replace(" ", "_"))
    os.makedirs(company_folder, exist_ok=True)
    filename = f"{contract_type}_{company_name.replace(' ', '_')}.pdf"
    filepath = os.path.join(company_folder, filename)

    date_str = datetime.now().strftime("%B %d, %Y")
    jurisdiction = random.choice(jurisdictions)
    currency = random.choice(currencies)
    liability_amount = random.randint(5000, 20000)
    archive_years = random.randint(2, 5)
    payment_days = random.choice([15, 30, 60])
    services_description = "consulting, advisory, and technical support services"

    # Create document
    doc = SimpleDocTemplate(filepath, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"<b>{contract_type} - {company_name}</b>", styles['Title']))
    story.append(Paragraph(f"Counterparty: {counterparty}", styles['Normal']))
    story.append(Paragraph(f"Effective Date: {date_str}", styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    # Add sections dynamically
    for section in contract_structure[contract_type]:
        content = get_tone_content(
            section, tone, date=date_str, company=company_name, counterparty=counterparty,
            jurisdiction=jurisdiction, amount=liability_amount, currency=currency, years=archive_years,
            days=payment_days, services=services_description
        )
        story.append(Paragraph(f"<b>{section.replace('_', ' ').title()}</b>", styles['Heading2']))
        story.append(Paragraph(content, styles['Normal']))
        story.append(Spacer(1, 0.25 * inch))

    # Signatures
    story.append(PageBreak())
    story.append(Paragraph("<b>Signatures</b>", styles['Heading2']))
    story.append(Paragraph("IN WITNESS WHEREOF, the Parties have executed this Agreement.", styles['Normal']))
    for party in [company_name, counterparty]:
        story.append(Paragraph(f"<b>{party}</b>", styles['Heading3']))
        story.append(Paragraph(fake.name(), styles['Normal']))
        story.append(Paragraph(fake.job(), styles['Normal']))
        story.append(Spacer(1, 0.5 * inch))

    doc.build(story)
    print(f"Contract generated: {filepath}")

def main():
    output_folder = "generated_contracts"
    num_companies = int(input("Enter the number of companies: "))
    min_contracts = int(input("Enter the minimum contracts per company: "))
    max_contracts = int(input("Enter the maximum contracts per company: "))

    counterparty = fake.company()
    print(f"Counterparty: {counterparty}")

    for _ in range(num_companies):
        company_name = fake.company()
        num_contracts = random.randint(min_contracts, max_contracts)
        for _ in range(num_contracts):
            contract_type = random.choice(contract_types)
            tone = random.choice(tones)
            generate_contract(output_folder, company_name, counterparty, contract_type, tone)

if __name__ == "__main__":
    main()

