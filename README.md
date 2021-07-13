<p align="center">
  <a href="https://imgbb.com/"><img src="https://i.ibb.co/wz12ysJ/githublogo-big.png" alt="githublogo-big" border="0"></a>
  <br>
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/berrysauce/microletter">
  <img alt="Libraries.io dependency status for GitHub repo" src="https://img.shields.io/librariesio/github/berrysauce/microletter">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/berrysauce/microletter">
  <img alt="GitHub CodeQL status" src="https://github.com/berrysauce/microletter/actions/workflows/codeql-analysis.yml/badge.svg">
</p>

# microletter
A micro newsletter service 📨

## Installation
1. Get a Deta project key at https://web.deta.sh
2. Get your Google Password or generate an App Password (like shown [here](https://support.google.com/accounts/answer/185833?hl=en)) if you're using 2 Factor Authentication
3. Clone this repository
4. Create a .env file with the following format in the same directory as the repository
```
DETA_TOKEN=YOURDETATOKEN
SMTP_PASSWORD=YOURGOOGLEPASSWORD
SMTP_EMAIL=YOURGMAILADDRESS
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```
5. Install all Python dependencies with `pip install -r requirements.txt` (make sure `pip -v` returns a version above 3.x - if not use `pip3 install -r requirements.txt`)
6. Run the code with `python main.py` (or with `python3 main.py` if `pip -v` returned a version under 3.x)

## How to use
Go to yourdomain.com/dashboard and you'll be redirected to your dashboard.

## Credits
- A part of the code in tools/mailer.py was found at https://realpython.com/python-send-email/
- Thanks to the makers and contributers of FastAPI - without you this wouldn't have been possible
- Thanks to lonaru for making EasyMDE (used as the Markdown Editor) Check it out here: https://github.com/Ionaru/easy-markdown-editor

## License
Currently, microletter is licensed under Copyright. This might change later.

© (Copyright) 2021, Paul Haedrich (berrysauce). All rights reserved. 
