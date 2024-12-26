import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from faker import Faker

# Initialize Faker for generating company and counterparty names
fake = Faker()

# Define contract structure with clause categories
contract_structure = {
    "CDA": ["introduction", "confidentiality"],
    "CA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration"],
    "MSA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration"],
    "WO": ["introduction", "scope_of_services", "confidentiality", "payment_terms"]
}

# Contract types, jurisdictions, currencies, and tones
contract_types = ["CDA", "CA", "MSA", "WO"]
jurisdictions = ["Germany", "USA", "Sweden", "France", "UK", "Canada", "Australia"]
currencies = ["USD", "EUR", "GBP", "SEK", "CAD"]
tones = ["neutral", "customer-friendly", "supplier-friendly"]

# Clauses with extensive variations
clauses = {
    "introduction": [
        "This Agreement is entered into on {date} between {company} ('Client') and {counterparty} ('Consultant').",
        "On this day, {date}, {company} (the 'Client') and {counterparty} (the 'Consultant') formalize their Agreement.",
        "This document, dated {date}, outlines the terms agreed upon by {company} and {counterparty}."
    ],
    "scope_of_services": [
        "The Consultant agrees to provide the following services: {services_description}.",
        "The services to be provided by the Consultant include: {services_description}, as outlined in this Agreement.",
        "This Agreement defines the services as {services_description}, to be delivered by the Consultant."
    ],
    "confidentiality": {
        "neutral": [
            "The Receiving Party agrees to use reasonable measures to protect all Confidential Information disclosed during this Agreement.",
            "The Receiving Party shall maintain the confidentiality of all disclosed proprietary information and limit access to authorized personnel."
        ],
        "customer-friendly": [
            "The Receiving Party shall implement the strictest measures to safeguard Confidential Information, ensuring no unauthorized access or disclosure.",
            "The Receiving Party is obligated to apply rigorous controls to protect all Confidential Information shared under this Agreement."
        ],
        "supplier-friendly": [
            "The Receiving Party shall take reasonable efforts to protect Confidential Information but shall not be held liable for inadvertent disclosures.",
            "The Receiving Party will make commercially reasonable efforts to ensure confidentiality of the shared information."
        ]
    },
    "payment_terms": {
        "neutral": [
            "All invoices shall be paid within {days} days of receipt. Late payments will incur interest at 1.5% per month.",
            "Invoices are payable within {days} days. Delayed payments may result in interest penalties as stipulated in this Agreement."
        ],
        "customer-friendly": [
            "The Client agrees to process invoices within {days} days to avoid delays, ensuring prompt payment.",
            "The Client will prioritize timely payments, ensuring invoices are processed within {days} days of receipt."
        ],
        "supplier-friendly": [
            "The Client shall remit payment within {days} days. Any disputes must be raised within 7 days of invoice receipt.",
            "Payment must be made within {days} days, and undisputed invoices shall be considered accepted if not contested within 7 days."
        ]
    },
    "liability_cap": {
        "neutral": [
            "The total liability under this Agreement shall not exceed {amount} {currency}. Neither Party shall be liable for consequential damages.",
            "The liability of each Party is limited to {amount} {currency}, with no responsibility for indirect damages."
        ],
        "customer-friendly": [
            "The Consultant’s liability is unlimited in cases of gross negligence, willful misconduct, or confidentiality breaches.",
            "The Consultant will bear full liability for any instances of gross negligence or breaches of confidentiality."
        ],
        "supplier-friendly": [
            "The Consultant’s total liability is capped at {amount} {currency}, irrespective of the nature of the claim.",
            "The Consultant’s liability is strictly limited to {amount} {currency}, regardless of circumstances."
        ]
    },
    "archive_duration": {
        "neutral": [
            "All records under this Agreement shall be retained for {years} years or as required by law.",
            "The Parties agree to maintain all relevant records for a minimum of {years} years."
        ],
        "customer-friendly": [
            "The Client agrees to maintain all records for {years} years to ensure compliance and transparency.",
            "The Client will retain Agreement-related records for {years} years to fulfill audit and compliance obligations."
        ],
        "supplier-friendly": [
            "The Consultant will preserve relevant documentation for {years} years, unless a longer period is mandated by law.",
            "The Consultant shall archive necessary records for {years} years, in line with legal requirements."
        ]
    }
}

def get_clause_content(clause_name, tone, **kwargs):
    """Generate clause content dynamically based on tone."""
    if clause_name in clauses and isinstance(clauses[clause_name], dict):
        clause_variants = clauses[clause_name][tone]
    else:
        clause_variants = clauses[clause_name]
    content = random.choice(clause_variants)
    return content.format(**kwargs)

def generate_contract(output_folder, company_name, counterparty, contract_type):
    """Generate a single contract with structured clauses and tones."""
    company_folder = os.path.join(output_folder, company_name.replace(" ", "_"))
    os.makedirs(company_folder, exist_ok=True)
    filename = f"{contract_type}_{company_name.replace(' ', '_')}.pdf"
    filepath = os.path.join(company_folder, filename)

    date_str = datetime.now().strftime("%B %d, %Y")
    jurisdiction = random.choice(jurisdictions)
    currency = random.choice(currencies)
    liability_amount = random.randint(5000, 20000)
    archive_time = random.randint(2, 5)
    payment_days = random.choice([15, 30, 60])
    services_description = "Consulting, advisory, and technical services as agreed between the Parties."

    # Randomly assign tones for each clause
    selected_tones = {section: random.choice(tones) for section in contract_structure[contract_type]}
    print(f"Generating {contract_type} for {company_name} with tones: {selected_tones}")

    doc = SimpleDocTemplate(filepath, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    # Title and metadata
    story.append(Paragraph(f"<b>{contract_type} - {company_name}</b>", styles['Title']))
    story.append(Paragraph(f"Counterparty: {counterparty}", styles['Normal']))
    story.append(Paragraph(f"Effective Date: {date_str}", styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    # Sections with dynamic content
    for section in contract_structure[contract_type]:
        tone = selected_tones[section]
        if section == "introduction":
            content = get_clause_content(section, tone, date=date_str, company=company_name, counterparty=counterparty)
        elif section == "scope_of_services":
            content = get_clause_content(section, tone, services_description=services_description)
        elif section == "payment_terms":
            content = get_clause_content(section, tone, days=payment_days)
        elif section == "liability_cap":
            content = get_clause_content(section, tone, amount=liability_amount, currency=currency)
        elif section == "archive_duration":
            content = get_clause_content(section, tone, years=archive_time)
        else:
            content = get_clause_content(section, tone)

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
        story.append(Paragraph(fake.address().replace('\n', ', '), styles['Normal']))
        story.append(Spacer(1, 0.5 * inch))

    doc.build(story)
    print(f"Contract generated: {filepath}")

def main():
    """Main function to generate random contracts."""
    output_folder = "generated_contracts"
    num_companies = int(input("Enter the number of companies: "))
    min_contracts = int(input("Enter the minimum contracts per company: "))
    max_contracts = int(input("Enter the maximum contracts per company: "))

    counterparty = fake.company()
    print(f"Counterparty for all contracts: {counterparty}")

    for _ in range(num_companies):
        company_name = fake.company()
        num_contracts = random.randint(min_contracts, max_contracts)
        for _ in range(num_contracts):
            contract_type = random.choice(contract_types)
            generate_contract(output_folder, company_name, counterparty, contract_type)

if __name__ == "__main__":
    main()

