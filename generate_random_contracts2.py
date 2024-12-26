import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from faker import Faker

fake = Faker()

# Contract structure with logical section order
contract_structure = {
    "CDA": ["introduction", "confidentiality", "liability_cap", "dispute_resolution"],
    "CA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration", "dispute_resolution"],
    "MSA": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "archive_duration", "dispute_resolution"],
    "WO": ["introduction", "scope_of_services", "confidentiality", "payment_terms", "liability_cap", "dispute_resolution"]
}

# Parameters
contract_types = ["CDA", "CA", "MSA", "WO"]
jurisdictions = ["Germany", "USA", "Sweden", "France", "UK", "Canada", "Australia"]
currencies = ["USD", "EUR", "GBP", "SEK", "CAD"]
dispute_methods = ["court", "arbitration", "amicable settlement"]

# Clauses
clauses = {
    "introduction": [
        "This Agreement is entered into on {date} between {company} ('Client') and {counterparty} ('Consultant')."
    ],
    "scope_of_services": [
        "The Consultant agrees to provide the following services: {services_description}.",
        "The Client retains the Consultant to perform specific tasks, including {services_description}."
    ],
    "confidentiality": [
        "Both Parties agree to maintain confidentiality of all proprietary and sensitive information shared during the course of this Agreement.",
        "The Receiving Party shall protect and not disclose any Confidential Information without prior written consent from the Disclosing Party."
    ],
    "payment_terms": [
        "Invoices will be paid within {days} days. Late payments will incur interest at 1.5% per month.",
        "The Client shall remit payment within {days} days upon successful acceptance of deliverables."
    ],
    "liability_cap": [
        "The total liability of the Consultant is capped at {amount} {currency}, except in cases of gross negligence.",
        "Neither Party's liability shall exceed {amount} {currency}, except where legally prohibited."
    ],
    "archive_duration": [
        "Records related to this Agreement shall be retained for {years} years.",
        "Both Parties agree to maintain records for a minimum of {years} years, unless extended by law."
    ],
    "dispute_resolution": [
        "Any disputes will be resolved in accordance with the laws of {jurisdiction} in {method}.",
        "This Agreement is governed by {jurisdiction} law. Disputes shall be resolved through {method}."
    ]
}

def get_clause_content(section, **kwargs):
    """Fetch clause text with placeholders replaced."""
    template = random.choice(clauses[section])
    return template.format(**kwargs)

def generate_contract(output_folder, company_name, counterparty, contract_type, msa_date=None):
    """Generate a logically structured contract with enhancements."""
    # Set folder structure
    company_folder = os.path.join(output_folder, company_name.replace(" ", "_"))
    os.makedirs(company_folder, exist_ok=True)

    filename = f"{contract_type}_{company_name.replace(' ', '_')}.pdf"
    filepath = os.path.join(company_folder, filename)

    # Metadata
    date_str = datetime.now().strftime("%B %d, %Y")
    jurisdiction = random.choice(jurisdictions)
    currency = random.choice(currencies)
    liability_amount = random.randint(5000, 20000)
    archive_time = random.randint(2, 5)
    payment_days = random.choice([15, 30, 60])
    dispute_method = random.choice(dispute_methods)
    services_description = "consulting, advisory, and technical services."

    # Document setup
    doc = SimpleDocTemplate(filepath, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    # Title Section
    story.append(Paragraph(f"<b>{contract_type} - {company_name}</b>", styles['Title']))
    story.append(Paragraph(f"Counterparty: {counterparty}", styles['Normal']))
    story.append(Paragraph(f"Effective Date: {date_str}", styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    # Add Sections Dynamically
    section_counter = 1
    for section in contract_structure[contract_type]:
        story.append(Paragraph(f"<b>{section_counter}. {section.replace('_', ' ').title()}</b>", styles['Heading2']))

        if section == "introduction":
            content = get_clause_content(section, date=date_str, company=company_name, counterparty=counterparty)
        elif section == "scope_of_services":
            content = get_clause_content(section, services_description=services_description)
        elif section == "liability_cap":
            content = get_clause_content(section, amount=liability_amount, currency=currency)
        elif section == "archive_duration":
            content = get_clause_content(section, years=archive_time)
        elif section == "payment_terms":
            content = get_clause_content(section, days=payment_days)
        elif section == "dispute_resolution":
            content = get_clause_content(section, jurisdiction=jurisdiction, method=dispute_method)
        else:
            content = get_clause_content(section)

        # Add content
        story.append(Paragraph(content, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        section_counter += 1

    # Signatures
    story.append(PageBreak())
    story.append(Paragraph("<b>Signatures</b>", styles['Heading2']))
    story.append(Paragraph("IN WITNESS WHEREOF, the Parties have executed this Agreement.", styles['Normal']))
    for party in [company_name, counterparty]:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(f"<b>{party}</b>", styles['Heading3']))
        story.append(Paragraph(fake.name(), styles['Normal']))
        story.append(Paragraph(fake.job(), styles['Normal']))

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
            generate_contract(output_folder, company_name, counterparty, contract_type)

if __name__ == "__main__":
    main()

