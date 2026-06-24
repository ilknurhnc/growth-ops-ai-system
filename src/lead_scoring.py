import pandas as pd


INPUT_PATH = "data/enriched_leads.csv"
OUTPUT_PATH = "data/scored_leads.csv"


def calculate_score(row):
    score = 0

    english_need_score = int(row["english_need_score"])

    if english_need_score >= 10:
        score += 45
    elif english_need_score >= 8:
        score += 40
    elif english_need_score >= 6:
        score += 25
    else:
        score += 10

    title = str(row["title"]).lower()

    if "director" in title or "group manager" in title:
        score += 35
    elif "manager" in title:
        score += 30
    elif "business partner" in title:
        score += 30
    elif "talent" in title or "recruitment" in title:
        score += 25
    elif "executive" in title:
        score += 20
    elif "specialist" in title:
        score += 15
    else:
        score += 10

    company_size = str(row["company_size"])

    if company_size in ["10000+", "5000+", "1000+"]:
        score += 25
    elif company_size in ["500+", "201-1000", "200-500"]:
        score += 20
    elif company_size in ["51-200", "50-200", "11-50"]:
        score += 15
    else:
        score += 10

    email = str(row.get("email", "")).strip()

    if email and email.lower() not in ["nan", "none"]:
        score += 5

    return min(score, 99)


def assign_lead_tier(score):
    if score >= 95:
        return "A+ Lead"
    elif score >= 85:
        return "A Lead"
    return "B Lead"


def main():
    df = pd.read_csv(INPUT_PATH)

    df["lead_score"] = df.apply(calculate_score, axis=1)
    df["lead_tier"] = df["lead_score"].apply(assign_lead_tier)

    df = df.sort_values(by="lead_score", ascending=False)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Lead scoring completed.")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()