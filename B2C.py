import requests

# Set up the API endpoint and headers
api_url = "https://api.safaricom.com/b2c/v1/paymentrequest"
headers = {
    "Authorization": "Bearer <your_access_token>",
    "Content-Type": "application/json"
}

# Define the payload for the API request
payload = {
    "InitiatorName": "<your_initiator_name>",
    "SecurityCredential": "<your_security_credential>",
    "CommandID": "BusinessPayment",
    "Amount": "<amount_to_transfer>",
    "PartyA": "<sender_phone_number>",
    "PartyB": "<receiver_phone_number>",
    "Remarks": "<transaction_remarks>",
    "QueueTimeOutURL": "<your_queue_timeout_url>",
    "ResultURL": "<your_result_url>",
    "Occasion": "<transaction_occasion>"
}

# Send the API request
response = requests.post(api_url, headers=headers, json=payload)

# Check the response status code
if response.status_code == 200:
    # Success - parse the response JSON
    response_json = response.json()
    transaction_id = response_json["TransactionID"]
    print("Transaction successful. ID: ", transaction_id)
else:
    # Error - print the response text
    print("Transaction failed. Error: ", response.text)
