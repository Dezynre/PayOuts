import requests
import base64
import json

consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"

api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

r = requests.get(api_URL, auth=(consumer_key, consumer_secret))

access_token = json.loads(r.text)['access_token']

phone_number = "2547xxxxxxxx"
amount = "100"
transaction_description = "Test B2C transaction"
command_id = "SalaryPayment"
remarks = "Test remarks"

headers = {"Authorization": "Bearer %s" % access_token, "Content-Type": "application/json"}

api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

payload = {
    "InitiatorName": "test",
    "SecurityCredential": "test",
    "CommandID": command_id,
    "Amount": amount,
    "PartyA": phone_number,
    "PartyB": "600000",
    "Remarks": remarks,
    "QueueTimeOutURL": "http://example.com/timeout",
    "ResultURL": "http://example.com/result",
    "Occasion": "test"
}

response = requests.post(api_url, json=payload, headers=headers)

print(response.text)
