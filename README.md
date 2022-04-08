<p align="center">
  <img src="https://i.ibb.co/wz12ysJ/githublogo-big.png" alt="microletter-logo" border="0">
  <br>
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/berrysauce/microletter">
  <img alt="Libraries.io dependency status for GitHub repo" src="https://img.shields.io/librariesio/github/berrysauce/microletter">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/berrysauce/microletter">
  <img alt="GitHub CodeQL status" src="https://github.com/berrysauce/microletter/actions/workflows/codeql-analysis.yml/badge.svg">
</p>

# microletter
A micro newsletter service 📨

* 🏠 **Homepage:** https://microletter.cc
* 📘 **Documentation:** https://docs.microletter.cc
* 🪐 **Install on Deta Space:** https://deta.space/discovery/microletter

## Installation
> ⚠ **WARNING:** All dashboard links are accessable by ANYONE currently if not installed on Deta Space. Sensitive information might be viewable by anyone.
1. Get a Deta project key at https://web.deta.sh
2. Get your Google Password or generate an App Password (like shown [here](https://support.google.com/accounts/answer/185833?hl=en)) if you're using 2 Factor Authentication
3. Clone this repository
4. Create a .env file with the following format in the same directory as the repository
```
DETA_PROJECT_KEY=YOURDETATOKEN
SMTP_PASSWORD=YOURGOOGLEPASSWORD
SMTP_USERNAME=YOURGMAILADDRESS
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```
5. Install all Python dependencies with `pip install -r requirements.txt` (make sure `pip -v` returns a version above 3.x - if not use `pip3 install -r requirements.txt`)
6. Run the code with `python main.py` (or with `python3 main.py` if `pip -v` returned a version under 3.x)

## How to use
Go to yourdomain.com/dashboard and you'll be redirected to your dashboard.

## Credits
- A part of the code in tools/mailer.py was found at https://realpython.com/python-send-email/
- Thanks to the makers and contributers of FastAPI - without you this wouldn't have been possible. Check it out here: https://github.com/tiangolo/fastapi
- Thanks to lonaru for making EasyMDE (used as the Markdown Editor) Check it out here: https://github.com/Ionaru/easy-markdown-editor

## License
microletter is a self-hostable Newsletter service.
Copyright (C) 2021 Paul Haedrich (berrysauce)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For questions, contact microletter@berrysauce.me.

<a href="https://deta.sh/?ref=microletter" target="_blank"><img src="https://eu2.contabostorage.com/d74bc97ec80c4b13b7f1db8d39948228:brry-cdn/deta-sponsor/D3263D63-638F-46C3-B9AB-9DC7C5CAB9BC.jpeg" alt="Sponsored by Deta"></a>
