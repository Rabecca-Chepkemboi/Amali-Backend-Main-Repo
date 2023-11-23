from requests.auth import HTTPBasicAuth
import requests
from django.http import JsonResponse

def get_access_token():
    consumer_key = 'ctb9sQ3PAGGbwDgnDC2l2VZs9TbYwHlX'
    consumer_secret = 'yIcqx5jRMZvR2X53'
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    headers = {'Content-Type': 'application/json'}
    response = requests.get(access_token_url, headers=headers, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response.raise_for_status() 
    result = response.json()
    access_token = result.get('access_token', '')
    return access_token


