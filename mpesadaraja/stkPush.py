import requests
import json
import base64
from datetime import datetime
from django.http import JsonResponse
from .generateAccesstoken import get_access_token

def initiate_stk_push(amount, phone, full_name, email):
    if amount is None or phone is None:
        return False

    access_token = get_access_token()
    if access_token == "":
        return False
    else:
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        business_short_code = '174379'
        process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
        party_a = phone
        transaction_desc = 'stkpush test'

        stk_push_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        stk_push_payload = {
            'BusinessShortCode': business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': party_a,
            'PartyB': business_short_code,
            'PhoneNumber': party_a,
            'CallBackURL': 'https://d029-41-80-118-37.ngrok.io/mpesadaraja/callback',
            'AccountReference': "Amali",
            'TransactionDesc': transaction_desc
        }
        response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
        print(response.text)
        response.raise_for_status()


        response_data = response.json()
        checkout_request_id = response_data.get('CheckoutRequestID', '')
        response_code = response_data.get('ResponseCode', 0)

        response_code = int(response_code)
        if response_code == 0:
            return True
        else:
            return False



