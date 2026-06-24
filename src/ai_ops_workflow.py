import pandas as pd


def estimate_company_sector(company):
    company = str(company).lower()

    if any(keyword in company for keyword in ["tech", "teknoloji", "yazılım", "software", "data", "cloud", "digital"]):
        return "Technology / Software"
    elif any(keyword in company for keyword in ["bank", "finans", "finance", "pay", "sigorta"]):
        return "Finance / Fintech"
    elif any(keyword in company for keyword in ["academy", "school", "edu", "university", "öğren"]):
        return "Education"
    elif any(keyword in company for keyword in ["hospital", "health", "clinic", "sağlık"]):
        return "Healthcare"
    elif any(keyword in company for keyword in ["retail", "market", "store", "mağaza"]):
        return "Retail"

    return "General Business"


def estimate_company_size(company):
    company = str(company).lower()

    if any(keyword in company for keyword in ["holding", "bank", "global", "group"]):
        return "500+"
    elif any(keyword in company for keyword in ["tech", "teknoloji", "cloud", "data", "software", "yazılım"]):
        return "50-200"
    elif any(keyword in company for keyword in ["startup", "labs", "studio"]):
        return "11-50"

    return "50-200"


def lead_research_agent(row):
    title = str(row["title"]).lower()

    if "talent" in title or "recruitment" in title:
        return "Recruitment and candidate evaluation"
    elif "learning" in title or "development" in title:
        return "Employee learning and upskilling"
    elif "director" in title:
        return "Strategic HR and workforce development"
    elif "business partner" in title:
        return "Cross-functional HR support"

    return "General HR operations"


def get_role_specific_insight(title):
    title = str(title).lower()

    if "talent" in title or "recruitment" in title:
        return "aday görüşmelerinde İngilizce seviyesini yalnızca CV üzerinden değil, konuşma pratiğiyle de değerlendirme ihtiyacı doğabiliyor"

    elif "learning" in title or "development" in title:
        return "çalışan eğitimlerinde sürdürülebilirlik ve katılım oranı genelde en kritik iki konu oluyor"

    elif "people" in title or "culture" in title:
        return "çalışan bağlılığı ve gelişim kültürü tarafında pratik iletişim becerileri önemli bir kaldıraç olabiliyor"

    elif "business partner" in title:
        return "farklı departmanlarla çalışan HRBP rollerinde İngilizce iletişim, ekipler arası koordinasyonu doğrudan etkileyebiliyor"

    elif "director" in title:
        return "HR liderliği seviyesinde İngilizce gelişimi yalnızca eğitim değil, şirketin uluslararasılaşma kapasitesiyle de ilişkili olabiliyor"

    elif "manager" in title:
        return "ekiplerin günlük iş akışında İngilizceyi aktif kullanabilmesi, klasik eğitimlerden daha ölçülebilir bir gelişim alanı yaratabiliyor"

    return "çalışanların İngilizce konuşma pratiğini iş akışına entegre etmek HR ekipleri için ölçülebilir bir gelişim alanı yaratabiliyor"


def enrichment_agent(row, business_context):
    title = str(row["title"]).lower()

    if "director" in title:
        english_need_score = 9
        pain_point = "iş gücü gelişimini stratejik ölçekte yönetme"
        outreach_angle = "stratejik İngilizce iletişim programları"

    elif "talent" in title or "recruitment" in title:
        english_need_score = 8
        pain_point = "adayların İngilizce iletişim becerilerini değerlendirme"
        outreach_angle = "işe alım süreçlerinde İngilizce değerlendirme"

    elif "learning" in title or "development" in title:
        english_need_score = 8
        pain_point = "ölçeklenebilir çalışan eğitim programları tasarlama"
        outreach_angle = "çalışanlar için sürdürülebilir İngilizce gelişim programları"

    elif "manager" in title:
        english_need_score = 7
        pain_point = "ekip içi iletişimi ve çalışan gelişimini güçlendirme"
        outreach_angle = "ekiplere yönelik pratik İngilizce konuşma eğitimi"

    else:
        english_need_score = 6
        pain_point = "çalışan gelişimini destekleme"
        outreach_angle = "kurumsal İngilizce iletişim gelişimi"

    return {
        "business_context": business_context,
        "sector": estimate_company_sector(row["company"]),
        "company_size": estimate_company_size(row["company"]),
        "english_need_score": english_need_score,
        "pain_point": pain_point,
        "outreach_angle": outreach_angle,
        "role_specific_insight": get_role_specific_insight(row["title"])
    }


def scoring_agent(row):
    score = 0

    english_need_score = int(row["english_need_score"])
    title = str(row["title"]).lower()
    company_size = str(row["company_size"])

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

    if company_size == "500+":
        score += 25
    elif company_size == "50-200":
        score += 20
    elif company_size == "11-50":
        score += 15
    else:
        score += 10

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

{row["company"]} tarafındaki {row["title"]} rolünüz dikkatimi çekti.

Bu rolde {row["role_specific_insight"]}.

Bu yüzden {row["pain_point"]} tarafında Konuşarak Öğren'in {row["outreach_angle"]} yaklaşımının faydalı olabileceğini düşündüm.

Uygun olursa kısa bir bilgi paylaşmak isterim."""

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