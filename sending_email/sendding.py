import smtplib
from email.mime.text import MIMEText

# ================================
from database import db
# --------------------------------


async def sending_email(topic, text):
    result = await db.get_email(topic)
    server = None

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_where = result["email_where"]
    # куда ↑
    email_come = result["email_come"]
    # от куда ↑
    password = result["pass"]

    msg = MIMEText(text)
    msg["Subject"] = topic
    msg["From"] = email_come
    msg["To"] = email_where

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_come, password)
        server.sendmail(email_come, email_where, msg.as_string())
        print("Email отправлен ")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        server.quit()
