import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jinja2
from datetime import datetime
from dotenv import load_dotenv
from deta import Deta
import os
from tools import configuration

# See https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637602533738157783-185148397&rd=1
# Credit/Thanks to RealPython

load_dotenv()
deta = Deta()

subscribers = deta.Base("microletter-subscribers")

def deta_url():
    if os.getenv("DETA_SPACE_APP"):
        return "https://" + str(os.getenv("DETA_PATH")) + ".deta.app"
    else:
        return "https://" + str(os.getenv("DETA_PATH")) + ".deta.dev"
    
def get_env():
    try:
        load_dotenv()
        smtp_email = str(os.getenv("SMTP_USERNAME"))
        smtp_password = str(os.getenv("SMTP_PASSWORD"))
        smtp_server = str(os.getenv("SMTP_SERVER"))
        smtp_port = int(os.getenv("SMTP_PORT"))
        return smtp_email, smtp_password, smtp_server, smtp_port
    except:
        raise Exception("The enviroment variables are empty.") 

def verify(email: str, key: str):
    smtp_email, smtp_password, smtp_server, smtp_port = get_env()
    sender_email = smtp_email
    receiver_email = email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your Email - {0}".format(configuration.get("newsletter-title"))
    message["From"] = sender_email
    message["To"] = receiver_email
    
    email_data={
        "newsletter_title": configuration.get("newsletter-title"),
        "subscribe_link": "{0}/verify/{1}".format(deta_url(), key),
        "footer_address": configuration.get("privacy-address"),
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
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return True

def unsubscribe(email: str, key: str):
    smtp_email, smtp_password, smtp_server, smtp_port = get_env()
    sender_email = smtp_email
    receiver_email = email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirm that you want to unsubscribe from {0}".format(configuration.get("newsletter-title"))
    message["From"] = sender_email
    message["To"] = receiver_email
    
    email_data={
        "newsletter_title": configuration.get("newsletter-title"),
        "unsubscribe_link": "{0}/unsubscribe/?key={1}".format(deta_url(), key),
        "footer_address": configuration.get("privacy-address"),
        "footer_year": str(datetime.now().strftime("%Y"))
    }

    with open("templates/emails/unsubscribe.html", "r") as f:
        html_content = jinja2.Template(f.read())
    part1 = MIMEText(html_content.render(email_data), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return True

def send(data):
    smtp_email, smtp_password, smtp_server, smtp_port = get_env()
    sender_email = smtp_email
    message = MIMEMultipart("alternative")
    message["Subject"] = "{0} | {1}".format(data["post_title"], configuration.get("newsletter-title"))
    
    entries = subscribers.fetch({"verified": True}).items
    with open("templates/emails/newsletterv2.html", "r") as f:
            html_content = jinja2.Template(f.read())
            
    receivers = []
    for entry in entries:
        receivers.append(entry["email"])
    
    message["From"] = sender_email
    message["To"] = sender_email
    
    # RE-ADD FOR NEWSLETTER TEMPLATE V1
    #"fade1": configuration.get("color-fade1"),
    #"fade2": configuration.get("color-fade2"),
    #"titlecolor": configuration.get("color-title"),
        
    email_data={
        "newsletter_title": configuration.get("newsletter-title"),
        "newsletter_tagline": configuration.get("newsletter-tagline"),
        "post_title": data["post_title"],
        "post_date": data["post_date"],
        "post_content": data["post_content"],
        "footer_unsubscribe": "{0}/unsubscribe".format(deta_url()),
        "footer_address": configuration.get("privacy-address"),
        "footer_year": str(datetime.now().strftime("%Y"))
    }

    part1 = MIMEText(html_content.render(email_data), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receivers, message.as_string())

    return True