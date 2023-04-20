import requests

# Replace with your API credentials and endpoint URL
url = "https://api.safaricom.com/path/to/endpoint"
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
shortcode = "your_shortcode"
passkey = "your_passkey"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {consumer_key}:{consumer_secret}"
}

payload = {
    "InitiatorName": "apiuser",
    "SecurityCredential": "your_security_credential",
    "CommandID": "BusinessPayment",
    "Amount": "100",
    "PartyA": shortcode,
    "PartyB": "254712345678",
    "Remarks": "Test payment",
    "QueueTimeOutURL": "https://example.com/timeout",
    "ResultURL": "https://example.com/result",
    "Occasion": "Test payment"
}

response = requests.post(url, headers=headers, json=payload, auth=(shortcode, passkey))

print(response.json())
