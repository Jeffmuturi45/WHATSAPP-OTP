from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import generate_otp
from .twilio_service import send_whatsapp_otp
import json

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')

        otp = generate_otp()

        # save in session
        request.session['otp'] = otp
        request.session['phone'] = phone

        send_whatsapp_otp(phone, otp)

        return redirect("verify")
    return render(request,"login.html")


def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_otp = data.get("otp")
        except:
            return JsonResponse({"success": False, "error": "Invalid request"})

        session_otp = request.session.get("otp")

        if user_otp == session_otp:
            request.session['verified'] = True
            request.session.pop('otp', None)
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Invalid OTP"})

    return render(request, "verify.html")

def home(request):
    if not request.session.get('verified'):
        return redirect("verify")
    return render(request,"home.html")

def logout(request):
    request.session.flush()
    return redirect("login")