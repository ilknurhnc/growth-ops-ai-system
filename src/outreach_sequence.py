import pandas as pd


def generate_connection_request(row):
    first_name = str(row["name"]).split()[0]
    company = row["company"]

    return (
        f"Merhaba {first_name}, {company} tarafındaki HR çalışmalarınızı "
        f"görünce bağlantı kurmak istedim."
    )


def generate_first_message(row):
    first_name = str(row["name"]).split()[0]

    return f"""Merhaba {first_name},

{row["company"]} tarafındaki {row["title"]} rolünüzü görünce, {row["pain_point"].lower()} konusunda İngilizce iletişimin önemli olabileceğini düşündüm.

Konuşarak Öğren olarak {row["outreach_angle"].lower()} konusunda HR ekiplerine destek oluyoruz.

Kısa bir bilgi paylaşmam uygun olur mu?"""


def generate_value_follow_up(row):
    first_name = str(row["name"]).split()[0]

    return f"""Merhaba {first_name},

Kısa bir ekleme yapmak istedim. Özellikle HR ekipleri için İngilizce gelişimi yalnızca dil eğitimi değil; işe alım, çalışan gelişimi ve uluslararası iletişim kalitesiyle de doğrudan ilişkili.

Bu yüzden {row["company"]} gibi ekiplerde bu ihtiyacın ölçülebilir hale getirilmesi değerli olabilir."""


def generate_final_follow_up(row):
    first_name = str(row["name"]).split()[0]

    return f"""Merhaba {first_name},

Rahatsız etmek istemem. Konu şu an öncelikli değilse sorun değil.

İleride çalışanların İngilizce konuşma pratiği veya kurumsal eğitim ihtiyaçları gündeme gelirse Konuşarak Öğren tarafında yardımcı olabiliriz."""


df = pd.read_csv("data/ai_ops_output.csv")

df["day_0_connection_request"] = df.apply(generate_connection_request, axis=1)
df["day_3_first_message"] = df.apply(generate_first_message, axis=1)
df["day_7_value_follow_up"] = df.apply(generate_value_follow_up, axis=1)
df["day_14_final_follow_up"] = df.apply(generate_final_follow_up, axis=1)

df.to_csv("data/outreach_sequence_output.csv", index=False)

print("Multi-step outreach sequence generated.")