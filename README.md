# microletter
A micro newsletter service 📨

## Installation
1. Get a Deta project key at https://web.deta.sh
2. Get your Google Password or generate an App Password (like shown [here](https://support.google.com/accounts/answer/185833?hl=en)) if you're using 2 Factor Authentication
3. Clone this repository
4. Create a .env file with the following format in the same directory as the repository
```
DETA_TOKEN=YOURDETATOKEN
EMAIL_TOKEN=YOURGOOGLEPASSWORD
```
5. Install all Python dependencies with `pip install -r requirements.txt` (make sure `pip -v` returns a version above 3.x - if not use `pip3 install -r requirements.txt`)
6. Run the code with `python main.py` (or with `python3 main.py` if `pip -v` returned a version under 3.x)

## How to use
Go to yourdomain.com/dashboard and you'll be redirected to your dashboard.
