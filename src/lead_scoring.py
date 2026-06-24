import pandas as pd


def calculate_score(row):
    score = 0

    english_need_score = int(row["english_need_score"])

    if english_need_score >= 8:
        score += 40
    elif english_need_score >= 6:
        score += 25
    else:
        score += 10

    title = str(row["title"]).lower()

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

    company_size = str(row["company_size"])

    if company_size in ["200-500", "500+"]:
        score += 25
    elif company_size == "50-200":
        score += 20
    else:
        score += 10

    return score


def assign_lead_tier(score):
    if score >= 85:
        return "A Lead"
    elif score >= 65:
        return "B Lead"
    return "C Lead"


df = pd.read_csv("data/enriched_leads.csv")

df["lead_score"] = df.apply(calculate_score, axis=1)
df["lead_tier"] = df["lead_score"].apply(assign_lead_tier)

df = df.sort_values(by="lead_score", ascending=False)

df.to_csv("data/scored_leads.csv", index=False)

print("Lead scoring completed.")