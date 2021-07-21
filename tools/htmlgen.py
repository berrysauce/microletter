import jinja2
from datetime import datetime
from dotenv import load_dotenv
from deta import Deta
import os

load_dotenv()
deta = Deta()

subscribers = deta.Base("microletter-subscribers")
posts = deta.Base("microletter-posts")

def postcode():
    entries = posts.fetch(None).items
    if len(entries) == 0:
        posts_html = """<p>You have no posts</p>"""
    else:
        entries.sort(key = lambda x:x["date"])
        entries = entries[::-1]
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
    
    if len(entries) != 0:
        entries.sort(key = lambda x:x["subscribed_on"])
        entries = entries[::-1]
    
    for entry in entries:
        if month in entry["subscribed_on"]:
            monthly_subscribers += 1
        delete_link = "/dashboard/subscribers/delete/{0}".format(entry["key"])
        table_html = table_html + """
        <tr><td>{0}</td><td>{1}</td><td class="d-xxl-flex justify-content-xxl-end"><a class="btn btn-primary" role="button" style="background: var(--bs-red);border-color: var(--bs-red);border-radius: 5px;font-size: 12px;" href="{2}"><strong><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icon-tabler-trash" style="font-size: 20px;color: rgb(255,255,255);">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <line x1="4" y1="7" x2="20" y2="7"></line>
        <line x1="10" y1="11" x2="10" y2="17"></line>
        <line x1="14" y1="11" x2="14" y2="17"></line>
        <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path>
        <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path>
        </svg></strong></a></td></tr>
        """.format(entry["email"], entry["subscribed_on"], delete_link)
        
    return table_html, total_subscribers, monthly_subscribers  
            