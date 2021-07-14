from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))
config = deta.Base("microletter-config")

def get(value):
    return config.fetch(None).items[0][value]