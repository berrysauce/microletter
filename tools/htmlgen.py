import jinja2
from datetime import datetime
from dotenv import load_dotenv
from deta import Deta
import os

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))

subscribers = deta.Base("microletter-subscribers")
posts = deta.Base("microletter-posts")

def postcode():
    entries = posts.fetch(None).items
    if len(entries) == 0:
        posts_html = """<p>You have no posts</p>"""
    else:
        posts_html = """"""
        with open("templates/elements/post_card.html", "r") as f:
            posts_html_template = jinja2.Template(f.read())
        for entry in entries:
            data = {
                "title": entry["title"],
                "date": entry["date"],
                "excerpt": entry["excerpt"],
                "delete_link": "/dashboard/home/delete/{0}".format(entry["key"])
            }
            posts_html = posts_html + posts_html_template.render(data)
    return posts_html

def subscribertable():
    entries = subscribers.fetch({"verified": True}).items
    month = str(datetime.now().strftime("%B %Y"))
    total_subscribers = len(entries)
    monthly_subscribers = 0
    table_html = """"""
    
    for entry in entries:
        if month in entry["subscribed_on"]:
            monthly_subscribers += 1
        delete_link = "/dashboard/subscribers/delete/{0}".format(entry["key"])
        table_html = table_html + """<tr><td>{0}</td><td>{1}</td><td class="d-xxl-flex justify-content-xxl-end"><a class="btn btn-primary" role="button" style="background: var(--bs-red);border-color: var(--bs-red);border-radius: 5px;font-size: 12px;" href="{2}"><strong>REMOVE</strong></a></td></tr>""".format(entry["email"], entry["subscribed_on"], delete_link)
        
    return table_html, total_subscribers, monthly_subscribers  
            