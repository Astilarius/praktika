import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Worker import Worker

def send_notification(worker: Worker):
    sender_email = "your_email@example.com"
    receiver_email = worker.email
    password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Напоминание о проверке"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Уважаемый {worker.name},

    Это напоминание о том, что вам необходимо пройти проверку до {worker.next_check_date}.
    
    С уважением,
    Ваш работодатель
    """
    
    html = f"""\
    <html>
      <body>
        <p>Уважаемый {worker.name},<br><br>
           Это напоминание о том, что вам необходимо пройти проверку до {worker.next_check_date}.<br><br>
           С уважением,<br>
           Ваш работодатель
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        server = smtplib.SMTP_SSL("smtp.example.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")
    finally:
        server.quit()
