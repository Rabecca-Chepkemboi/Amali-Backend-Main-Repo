from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import MpesaService
from .generateAccesstoken import get_access_token
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .stkPush import initiate_stk_push
from .generateAccesstoken import get_access_token
from .query import query_stk_status
from .callback import process_stk_callback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Donation
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from .services import MpesaService


@csrf_exempt
def mpesawebhook(request):
    if request.method == 'POST':
        try:
            webhook_data = json.loads(request.body.decode('utf-8'))
            success = MpesaService.process_webhook(webhook_data)

            if success:
                return JsonResponse({'message': 'Webhook received and processed successfully'})
            else:
                return JsonResponse({'error': 'Error processing webhook data'}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data in webhook request'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class DarajaApiView(APIView):
    def get(self, request):
        donations = Donation.objects.all()
        response_data = {'donations': [{'id': donation.id, 'amount': donation.amount} for donation in donations]}
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        body = request.data
        phone = body.get('phone_number')
        full_name = body.get('full_name')
        email = body.get('email')
        amount = body.get('amount', 0)

        donation = Donation.objects.create(
            amount=amount,
            full_name=full_name,
            email=email,
            phone_number=phone
        )

        success = initiate_stk_push(amount, phone, full_name, email)

        if success:
            response_data = {'message': 'Donation initiated successfully'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            donation.delete()
            response_data = {'message': 'Donation initiation failed'}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
