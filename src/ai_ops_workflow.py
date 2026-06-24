import pandas as pd


def lead_research_agent(row):
    title = str(row["title"]).lower()

    if "talent" in title or "recruitment" in title:
        business_context = "Recruitment and candidate evaluation"
    elif "learning" in title or "development" in title:
        business_context = "Employee learning and upskilling"
    elif "director" in title:
        business_context = "Strategic HR and workforce development"
    elif "business partner" in title:
        business_context = "Cross-functional HR support"
    else:
        business_context = "General HR operations"

    return business_context


def enrichment_agent(row, business_context):
    title = str(row["title"]).lower()

    if "director" in title:
        english_need_score = 9
        pain_point = "Managing workforce development at scale"
        outreach_angle = "Strategic English communication programs"
    elif "talent" in title or "recruitment" in title:
        english_need_score = 8
        pain_point = "Assessing candidate communication skills"
        outreach_angle = "English evaluation for hiring processes"
    elif "learning" in title or "development" in title:
        english_need_score = 8
        pain_point = "Designing scalable employee training programs"
        outreach_angle = "Continuous English learning for employees"
    elif "manager" in title:
        english_need_score = 7
        pain_point = "Improving team communication and development"
        outreach_angle = "Practical English training for teams"
    else:
        english_need_score = 6
        pain_point = "Supporting employee development"
        outreach_angle = "Corporate English improvement"

    return {
        "business_context": business_context,
        "sector": "Estimated from company research",
        "company_size": "Estimated / To be enriched",
        "english_need_score": english_need_score,
        "pain_point": pain_point,
        "outreach_angle": outreach_angle
    }


def scoring_agent(row):
    score = 0

    english_need_score = int(row["english_need_score"])
    title = str(row["title"]).lower()

    if english_need_score >= 8:
        score += 40
    elif english_need_score >= 6:
        score += 25
    else:
        score += 10

    if "director" in title:
        score += 35
    elif "manager" in title:
        score += 30
    elif "business partner" in title:
        score += 25
    elif "talent" in title or "recruitment" in title:
        score += 20
    else:
        score += 10

    score += 20

    if score >= 85:
        tier = "A Lead"
    elif score >= 65:
        tier = "B Lead"
    else:
        tier = "C Lead"

    return score, tier


def outreach_agent(row):
    first_name = str(row["name"]).split()[0]

    message = f"""Merhaba {first_name},

{row["company"]} tarafındaki {row["title"]} rolünüzü görünce, {row["pain_point"].lower()} konusunda İngilizce iletişimin önemli olabileceğini düşündüm.

Konuşarak Öğren olarak {row["outreach_angle"].lower()} konusunda HR ekiplerine destek oluyoruz.

Kısa bir bilgi paylaşmam uygun olur mu?"""

    return message


def crm_agent(row):
    return {
        "status": "New",
        "channel": "LinkedIn",
        "next_action": "Send connection request",
        "follow_up_day": "Day 3"
    }


df = pd.read_csv("data/raw_leads.csv")

processed_rows = []

for _, row in df.iterrows():
    business_context = lead_research_agent(row)
    enrichment = enrichment_agent(row, business_context)

    enriched_row = {
        **row.to_dict(),
        **enrichment
    }

    score, tier = scoring_agent(enriched_row)
    enriched_row["lead_score"] = score
    enriched_row["lead_tier"] = tier
    enriched_row["linkedin_message"] = outreach_agent(enriched_row)

    crm_data = crm_agent(enriched_row)
    enriched_row.update(crm_data)

    processed_rows.append(enriched_row)


output_df = pd.DataFrame(processed_rows)
output_df.to_csv("data/ai_ops_output.csv", index=False)

print("AI Ops workflow completed.")