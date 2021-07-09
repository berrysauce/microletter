import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jinja2
from datetime import datetime
from dotenv import load_dotenv
from deta import Deta
import os

# See https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637602533738157783-185148397&rd=1
# Credit/Thanks to RealPython

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))
deta_url = "https://" + str(os.getenv("DETA_PATH")) + ".deta.dev"

subscribers = deta.Base("microletter-subscribers")

def verify(email: str, key: str):
    sender_email = str(os.getenv("EMAIL_ADDRESS"))                                   # REPLACE WITH CONFIG DATA 
    receiver_email = email
    password = str(os.getenv("EMAIL_TOKEN"))
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your Email - {0}".format("Paul's Newsletter")     # REPLACE WITH CONFIG DATA
    message["From"] = sender_email
    message["To"] = receiver_email
    
    email_data={
        "newsletter_title": "Paul's Newsletter",                                   # REPLACE WITH CONFIG DATA
        "subscribe_link": "{0}/verify/{1}".format(deta_url, key),
        "footer_address": "Musterstr. 1a, 01234 Musterstadt, Musterland",          # REPLACE WITH CONFIG DATA
        "footer_year": str(datetime.now().strftime("%Y"))
    }

    with open("templates/emails/verification.html", "r") as f:
        html_content = jinja2.Template(f.read())
    part1 = MIMEText(html_content.render(email_data), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return True

def send(data):
    sender_email = str(os.getenv("EMAIL_ADDRESS"))                                   # REPLACE WITH CONFIG DATA 
    password = str(os.getenv("EMAIL_TOKEN"))
    message = MIMEMultipart("alternative")
    message["Subject"] = "{0} | {1}".format(data["post_title"], "Paul's Newsletter") # REPLACE WITH CONFIG DATA
    
    entries = subscribers.fetch({"verified": True}).items
    with open("templates/emails/newsletter.html", "r") as f:
            html_content = jinja2.Template(f.read())
    
    for entry in entries:
        receiver_email = entry["email"]
        message["From"] = sender_email
        message["To"] = receiver_email
        
        email_data={
            "newsletter_title": "Paul's Newsletter",
            "newsletter_tagline": "Just a weekly ramble.",
            "post_title": data["post_title"],
            "post_date": data["post_date"],
            "post_content": data["post_content"],
            "footer_unsubscribe": "{0}/unsubscribe/{1}".format(deta_url, entry["key"]),
            "footer_address": "Musterstr. 1a, 01234 Musterstadt, Musterland",           # REPLACE WITH CONFIG DATA
            "footer_year": str(datetime.now().strftime("%Y"))
        }

        part1 = MIMEText(html_content.render(email_data), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    return True