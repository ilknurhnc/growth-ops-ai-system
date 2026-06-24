from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "ai_ops_output.csv"
OUTPUT_PATH = BASE_DIR / "data" / "outreach_messages.csv"
PREVIEW_PATH = BASE_DIR / "data" / "outreach_preview.txt"


def first_name(full_name):
    return str(full_name).split()[0]


def clean_value(value, fallback=""):
    if pd.isna(value):
        return fallback

    value = str(value).strip()

    if value.lower() in ["nan", "none", ""]:
        return fallback

    return value


def get_company_phrase(company):
    company = clean_value(company)

    if not company:
        return "kurumunuzdaki"

    return f"{company} tarafındaki"


def get_channel(row):
    email = clean_value(row.get("email", ""))

    if email:
        return "Email + LinkedIn"

    return "LinkedIn"


def generate_message(row):
    name = first_name(row["name"])
    company_phrase = get_company_phrase(row.get("company", ""))
    title = clean_value(row.get("title", "İnsan Kaynakları"))
    pain_point = clean_value(
        row.get("pain_point", "çalışan gelişimi ve iletişim süreçleri")
    ).lower()
    outreach_angle = clean_value(
        row.get("outreach_angle", "kurumsal İngilizce iletişim gelişimi")
    ).lower()
    lead_tier = clean_value(row.get("lead_tier", ""))

    if lead_tier == "A+ Lead":
        intro = (
            "Profilinizi incelerken stratejik HR, çalışan gelişimi ve "
            "organizasyonel dönüşüm tarafındaki odağınız dikkatimi çekti."
        )
    elif "recruitment" in title.lower() or "recruitment" in pain_point:
        intro = (
            "Profilinizi incelerken işe alım, aday deneyimi ve yetenek "
            "değerlendirme tarafındaki odağınız dikkatimi çekti."
        )
    elif "business partner" in title.lower() or "hrbp" in title.lower():
        intro = (
            "Profilinizi incelerken HRBP rolünüzün iş birimleriyle yakın "
            "çalışmayı ve çalışan gelişimini desteklediğini düşündüm."
        )
    else:
        intro = (
            "Profilinizi incelerken insan kaynakları ve çalışan gelişimi "
            "tarafındaki çalışmalarınız dikkatimi çekti."
        )

    return f"""Merhaba {name},

{intro}

{company_phrase} {title} rolünüz kapsamında özellikle {pain_point} konusunun önemli bir gündem olabileceğini düşündüm.

Konuşarak Öğren olarak {outreach_angle} konusunda kurumlara destek oluyoruz.

Uygun olursa bu alanda kısa bir fikir paylaşmak isterim."""


def write_preview_file(output_df):
    with open(PREVIEW_PATH, "w", encoding="utf-8") as file:
        file.write("GENERATED OUTREACH MESSAGES\n")
        file.write("=" * 80)
        file.write("\n\n")

        for _, row in output_df.iterrows():
            file.write("-" * 80)
            file.write("\n")
            file.write(f"Lead: {row['name']}\n")
            file.write(f"Company: {row['company']}\n")
            file.write(f"Tier: {row['lead_tier']}\n")
            file.write(f"Channel: {row['channel']}\n")
            file.write("-" * 80)
            file.write("\n\n")
            file.write(row["personalized_message"])
            file.write("\n\n")


def print_messages(output_df):
    print("\n" + "=" * 80)
    print("GENERATED OUTREACH MESSAGES")
    print("=" * 80)

    for _, row in output_df.iterrows():
        print("\n")
        print("-" * 80)
        print(f"Lead: {row['name']}")
        print(f"Company: {row['company']}")
        print(f"Tier: {row['lead_tier']}")
        print(f"Channel: {row['channel']}")
        print("-" * 80)
        print(row["personalized_message"])


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "data/ai_ops_output.csv bulunamadı. Önce ai_ops_workflow.py çalışmalı."
        )

    df = pd.read_csv(INPUT_PATH)

    required_columns = [
        "name",
        "company",
        "title",
        "pain_point",
        "outreach_angle",
        "lead_score",
        "lead_tier",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Eksik kolonlar: {missing_columns}")

    output_df = pd.DataFrame()

    output_df["name"] = df["name"]
    output_df["company"] = df["company"].fillna("")
    output_df["title"] = df["title"]
    output_df["linkedin"] = df.get("linkedin", "")
    output_df["email"] = df.get("email", "")
    output_df["lead_score"] = df["lead_score"]
    output_df["lead_tier"] = df["lead_tier"]
    output_df["channel"] = df.apply(get_channel, axis=1)
    output_df["personalized_message"] = df.apply(generate_message, axis=1)
    output_df["status"] = "Message Generated"

    output_df.to_csv(OUTPUT_PATH, index=False)
    write_preview_file(output_df)

    print("Personalized outreach messages generated.")
    print(f"CSV Output: {OUTPUT_PATH}")
    print(f"Preview Output: {PREVIEW_PATH}")

    print_messages(output_df)


if __name__ == "__main__":
    main()