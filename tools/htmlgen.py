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
    """
    entries = [
        {
            "key": "83ihdjgfu3t7",
            "title": "Awesome post",
            "date": "04. July 2021",
            "excerpt": "This is a cool little test post."
        },
        {
            "key": "83284h3bb23b",
            "title": "Second awesome post",
            "date": "04. July 2021",
            "excerpt": "This is a cool, second, and of course, little test post."
        }
    ]
    """
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
            
            