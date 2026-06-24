import pandas as pd


def generate_linkedin_message(row):
    name = row["name"].split()[0]
    company = row["company"]
    title = row["title"]
    pain_point = row["pain_point"]
    outreach_angle = row["outreach_angle"]

    message = f"""Merhaba {name} Hanım/Bey,

{company} tarafında {title} rolünüzü görünce, özellikle "{pain_point}" konusunda İngilizce iletişimin önemli olabileceğini düşündüm.

Konuşarak Öğren olarak {outreach_angle.lower()} konusunda HR ekiplerine destek oluyoruz.

Uygun olursa kısa bir bilgi paylaşmak isterim."""

    return message


df = pd.read_csv("data/scored_leads.csv")

df["linkedin_message"] = df.apply(generate_linkedin_message, axis=1)

df.to_csv("data/final_leads_with_messages.csv", index=False)

print("Personalized outreach messages generated.")