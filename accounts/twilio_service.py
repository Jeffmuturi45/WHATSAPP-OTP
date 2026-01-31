from twilio.rest import Client
from django.conf import settings

def send_whatsapp_otp(phone, otp):

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )

    message = f"Your verification code is: {otp}"
    client = client.messages.create(
        body=message,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{phone}"
    )

