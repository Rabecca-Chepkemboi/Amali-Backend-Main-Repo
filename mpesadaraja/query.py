import requests
import json
import base64
from datetime import datetime
from django.http import JsonResponse
from .generateAccesstoken import get_access_token

def query_stk_status(request):
    access_token_response = get_access_token(request)
    
    if isinstance(access_token_response, JsonResponse):
        try:
            access_token_json = access_token_response.json()
            access_token = access_token_json.get('access_token')
            
            if access_token:
                query_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
                business_short_code = '174379'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                checkout_request_id = 'ws_CO_04072023004444401768168060'
                
                query_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
                
                query_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'CheckoutRequestID': checkout_request_id
                }
                
                response = requests.post(query_url, headers=query_headers, json=query_payload)
                response.raise_for_status()  
                
                response_data = response.json()
                result_code = response_data.get('ResultCode', '')
                
                if result_code == '1037':
                    message = "1037 Timeout in completing transaction"
                elif result_code == '1032':
                    message = "1032 Transaction has been canceled by the user"
                elif result_code == '1':
                    message = "1 The balance is insufficient for the transaction"
                elif result_code == '0':
                    message = "0 The transaction was successful"
                else:
                    message = "Unknown result code: " + result_code
                
                return JsonResponse({'message': message})
            
            else:
                return JsonResponse({'error': 'Access token not found.'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error: ' + str(e)}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Error decoding JSON: ' + str(e)}, status=500)
    
    else:
        return access_token_response  
