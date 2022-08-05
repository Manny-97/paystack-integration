from urllib import response
from django.conf import settings
import requests

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transactions/verify/{ref}'

        #Request Headers
        headers = {
            'Authorization': f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'content-type': 'application/json'
        }
        url = self.base_url + path
        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response['data']

        response_data = response.json()
        return response_data['status'], response_data['message']
