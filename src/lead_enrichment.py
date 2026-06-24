import pandas as pd


def enrich_lead(title, company):

    title = str(title).lower()

    # Varsayılan değerler

    sector = "Technology"
    company_size = "50-200"

    english_need_score = 6
    pain_point = "Employee development"
    outreach_angle = "Corporate English improvement"

    # Talent Acquisition

    if "talent" in title or "recruitment" in title:
        english_need_score = 9
        pain_point = "Finding qualified candidates"
        outreach_angle = "English assessment for hiring"

    # HR Manager

    elif "hr manager" in title:
        english_need_score = 8
        pain_point = "Managing employee development"
        outreach_angle = "Workplace communication skills"

    # HR Director

    elif "director" in title:
        english_need_score = 9
        pain_point = "International workforce management"
        outreach_angle = "Global communication training"

    # HRBP

    elif "business partner" in title:
        english_need_score = 8
        pain_point = "Supporting business growth"
        outreach_angle = "Cross-functional communication"

    # Learning & Development

    elif "learning" in title:
        english_need_score = 7
        pain_point = "Employee upskilling"
        outreach_angle = "Continuous English learning"

    return {
        "sector": sector,
        "company_size": company_size,
        "english_need_score": english_need_score,
        "pain_point": pain_point,
        "outreach_angle": outreach_angle
    }


# CSV oku

df = pd.read_csv("data/raw_leads.csv")

enriched_rows = []

for _, row in df.iterrows():

    enrichment = enrich_lead(
        row["title"],
        row["company"]
    )

    enriched_rows.append({
        "name": row["name"],
        "company": row["company"],
        "title": row["title"],
        "linkedin": row["linkedin"],

        "sector": enrichment["sector"],
        "company_size": enrichment["company_size"],
        "english_need_score": enrichment["english_need_score"],
        "pain_point": enrichment["pain_point"],
        "outreach_angle": enrichment["outreach_angle"]
    })

enriched_df = pd.DataFrame(enriched_rows)

enriched_df.to_csv(
    "data/enriched_leads.csv",
    index=False
)

print("Lead enrichment completed.")