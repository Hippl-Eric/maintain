import os
import requests
from dotenv import load_dotenv


def call_car_md():
    load_dotenv()
    CAR_MD_AUTH = os.getenv("CAR_MD_AUTH")
    CAR_MD_PART = os.getenv("CAR_MD_PART")
    url = "http://api.carmd.com/v3.0/fields"
    headers = {
        "content-type":"application/json",
        "authorization":CAR_MD_AUTH,
        "partner-token":CAR_MD_PART
    }
    params = {
        "vin": "1GNALDEK9FZ108495"
    }
    r = requests.get(url, headers=headers, params=params)
    print(r.text)

def get_credits():
    load_dotenv()
    CAR_MD_AUTH = os.getenv("CAR_MD_AUTH")
    CAR_MD_PART = os.getenv("CAR_MD_PART")
    url = "http://api.carmd.com/v3.0/credits"
    headers = {
        "content-type":"application/json",
        "authorization":CAR_MD_AUTH,
        "partner-token":CAR_MD_PART
    }
    r = requests.get(url, headers=headers)
    print(r.text)