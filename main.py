import uvicorn
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional
import markdown
import html2text
import jinja2
from tools import mailer, htmlgen
from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
deta = Deta(os.getenv("DETA_TOKEN"))

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/unsubscribe/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/verify/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/dashboard/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")
subscribers = deta.Base("microletter-subscribers")
posts = deta.Base("microletter-posts")
config = deta.Base("microletter-config")

subscribed = []

"""
# MARKDOWN TO TEXT
from BeautifulSoup import BeautifulSoup
from markdown import markdown

html = markdown(some_html_string)
text = ''.join(BeautifulSoup(html).findAll(text=True))

# REPLACE DIVS WITH TABLES FOR NEWSLETTER TEMPLATE
"""



"""
--------------------------------------------------------------------------------------
                                USER FRONT END
--------------------------------------------------------------------------------------
"""

@app.get("/", response_class=HTMLResponse)
async def get_root():
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/subscribe")
async def post_subscribe(request: Request, email: str = Form(...)):
    if len(subscribers.fetch({"email": email}).items) != 0:
        title = "You're already subscribed!"
        description = "This email is already on our list. Even if you love this newsletter, you can't subscribe two times!"
        return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})
        
    entry = subscribers.insert({
            "email": email,
            "subscribed_on": str(datetime.now().strftime("%d. %B %Y")),
            "verified": False
    })
    if mailer.verify(email, entry["key"]) is True:
        title = "Last step: Confirm your email"
        description = "You should've received a confirmation email. Click on the link in the email to confirm your subscription. If you can't find it, look in your spam folder or try again."
        return templates.TemplateResponse("success.html", {"request": request, "title": title, "description": description})
    else:
        title = "Email confirmation failed"
        description = "There was a problem with sending your verification Email."
        return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})

@app.get("/verify/{key}")
async def get_verify(request: Request, key: str):
    try:
        entry = subscribers.get(key)
        if entry["verified"] is True:
            title = "Your email is already verified!"
            description = "You don't need to verify your email twice! It's already marked as verified."
            return templates.TemplateResponse("success.html", {"request": request, "title": title, "description": description})
        subscribers.update(key=key, updates={
            "email": entry["email"],
            "subscribed_on": entry["subscribed_on"],
            "verified": True
        })
        title = "Your email was confirmed!"
        description = "You successfully verified your email. You'll now receive all new posts in your inbox. Don't worry, you can also unsubscribe any time at the bottom of the newsletter."
        return templates.TemplateResponse("success.html", {"request": request, "title": title, "description": description})
    except:
        title = "The verification failed!"
        description = "Your email couldn't be verified. Please try again later by clicking on the link in the verification email you've received."
        return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})

@app.get("/unsubscribe/{key}")
async def get_unsubscribe(request: Request, key: str, finalize: Optional[bool] = False):
    if finalize is True: 
        try:
            subscribers.delete(key)
            title = "Successfully unsubscribed!"
            description = "We're sorry to see you go! Your email was removed from our database."
            return templates.TemplateResponse("success.html", {"request": request, "title": title, "description": description})
        except:
            title = "There was a problem with unsubscribing you"
            description = "There was an error while unsubscribing you. Try again later or contact the newsletter owner to get unsubscribed manually."
            return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})
    entry = subscribers.get(key)
    return templates.TemplateResponse("unsubscribe.html", {"request": request, "email": entry["email"], "date": entry["subscribed_on"]})

    

"""
--------------------------------------------------------------------------------------
                               ADMIN FRONT END
--------------------------------------------------------------------------------------
"""

@app.get("/subscribers")
async def get_subscribers(verified: Optional[bool] = True):
    if verified is True:
        subscribed = subscribers.fetch({"verified": True}).items
    else:
        subscribed = subscribers.fetch({"verified": False}).items
    return subscribed

@app.get("/dashboard")
async def get_dashboard():
    return RedirectResponse("/dashboard/home")

@app.get("/dashboard/home", response_class=HTMLResponse)
async def get_home(request: Request, show: Optional[str] = None):
    if show == "success":
        popup_html = """<div role="alert" class="alert alert-success" style="margin-top: 10px;margin-bottom: 10px;"><span><strong>Done!</strong><br /></span></div>"""
    elif show == "error":
        popup_html = """<div role="alert" class="alert alert-danger" style="margin-top: 10px;margin-bottom: 10px;"><span><strong>Error</strong><br /></span></div>"""
    else:
        popup_html = """"""
        
    return templates.TemplateResponse("dashboard.html", {"request": request, "popup": popup_html, "posts": htmlgen.postcode()})

@app.get("/dashboard/editor", response_class=HTMLResponse)
async def get_editor():
    with open("templates/editor.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/dashboard/editor/create", response_class=HTMLResponse)
async def post_create(request: Request, title: str = Form(None), content: Optional[str] = Form(None)):
    if content is None or title is None:
        title = "Your post can't be empty!"
        description = "Sorry, but you can't create a post without content. Please go back and fill out the content field to send your post."
        return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})
    
    date = str(datetime.now().strftime("%d. %B %Y"))
    html_content = markdown.markdown(content)
    converter = html2text.HTML2Text()
    # Ignore converting links from HTML
    converter.ignore_links = True
    text_content = converter.handle(html_content)
    excerpt = text_content[:50] + "..."
    email_data={
        "post_title": title,
        "post_date": date,
        "post_content": html_content
    }
    
    if mailer.send(email_data) is not True:
        title = "There was an error with sending your email"
        description = "Sorry, but the email couldn't be sent. Please try again later."
        return templates.TemplateResponse("error.html", {"request": request, "title": title, "description": description})
    
    posts.insert({
        "title": title,
        "date": date,
        "html_content": html_content,
        "text_content": text_content,
        "excerpt": excerpt
    })
    
    return RedirectResponse(url="/dashboard/home/?show=success", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/dashboard/subscribers", response_class=HTMLResponse)
async def get_subscribers(request: Request):
    return templates.TemplateResponse("newsletter.html", newsletter_data)



"""
--------------------------------------------------------------------------------------
                                    BACK END
--------------------------------------------------------------------------------------
"""

@app.get("/dashboard/subscribers/delete/{key}")
async def get_subscriber_delete(key: str):
    subscribers.delete(key)
    return RedirectResponse(url="/dashboard/subscribers/?show=success", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/dashboard/home/delete/{key}")
async def get_home_delete(key: str):
    posts.delete(key)
    return RedirectResponse(url="/dashboard/home/?show=success", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)