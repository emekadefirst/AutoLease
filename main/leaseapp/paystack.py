# import statement
import os
import json
import requests
from dotenv import load_dotenv

# load dotenv
load_dotenv()

secret_key = os.getenv('SECRET_KEY')


# definition of API URLs
DOMAIN = 'https://api.paystack.co'
PAYMENT_PATH = 'transaction/initialize'

# definition of function in charge of payment
def make_payment(email, amount):
    # In the header you pass in your secret key
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    # In the body you pass in the data which is the email, and amount and remember that amount is multiplied by 100 because paystack calc in kobo
    body = {
        "amount": amount * 100,
        "email": email,
    }
    # our url
    url = f"{DOMAIN}/{PAYMENT_PATH}"
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        reference = data["data"]["reference"]
        url = data["data"]["authorization_url"]
        return {"reference": reference, "url": url}
    return response.status_code
