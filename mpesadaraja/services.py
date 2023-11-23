import json
from .stkPush import initiate_stk_push
from .models import Donation

class MpesaService:
    @staticmethod
    def initiate_donation(amount, phone, full_name, email):
        return initiate_stk_push(amount, phone, full_name, email)

    @staticmethod
    def process_webhook(webhook_data):
        try:
            

            donation = Donation(
                amount=webhook_data['amount'],
                full_name=webhook_data.get('full_name', ''),
                email=webhook_data.get('email', ''),
                phone_number=webhook_data.get('phone_number', '')
            )
            donation.save()

            return True  
        except Exception as e:
            print(f"Error processing webhook data: {e}")
            return False
