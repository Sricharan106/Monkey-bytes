import sqlite3
import os
from dotenv import load_dotenv
import psycopg2
import smtplib
from email.mime.text import MIMEText
load_dotenv()
# Newsletter sender credentials (your 2nd Gmail)
SENDER_EMAIL = "newsletter.monkeybytes@gmail.com"       # your second email
sender_password = 'idet fkqg lhqk czmj'


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def send_newsletter(subject, body, category, date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT name, email FROM users WHERE news_type = %s AND email IS NOT NULL", (category,))
    users = c.fetchall()
    if not users:
        print("❌ No users found for this category.")
        conn.close()
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, sender_password)

            for name, email in users:
                msg = MIMEText(body.replace("{name}", name))  # Personalize
                msg['Subject'] = subject
                msg['From'] = SENDER_EMAIL
                msg['To'] = email
                smtp.send_message(msg)
                print(f"✅ Sent to {email}")

                c.execute(
                    "CREATE TABLE IF NOT EXISTS archives (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, body TEXT, cat" \
                    "egory TEXT, sent_at TEXT)")
                c.execute("INSERT INTO archives (subject, body, category, sent_at) VALUES (?, ?, ?, ?)",
                          (subject, body, category, date))
                conn.commit()

    except Exception as e:
        print(f"❌ Error sending: {e}")
    finally:
        conn.close()
        

# 🧠 You type this when you want to send
if __name__ == "__main__":
    subject = input("Subject: ")
    print("Body (type your message, {name} will be replaced):")
    body_lines = []
    while True:
        line = input()
        if line.strip().lower() == "end":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)

    category = input("Send to which category? (tech, anime, both): ").strip().lower()
    date = input("Enter the date (YYYY-MM-DD): ")
    send_newsletter(subject, body, category, date)
