import json
from django.test import TestCase, Client
from accounts.utils import generate_otp

class OTPFlowTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.phone = "+254712345678"

    def test_otp_login_flow(self):
        # Step 1: Login POST should generate OTP and store in session
        response = self.client.post("/login/", {"phone": self.phone})
        self.assertEqual(response.status_code, 302)  # redirect to verify

        # Get session OTP
        session = self.client.session
        otp = session.get("otp")
        self.assertIsNotNone(otp, "OTP should be set in session")

        # Step 2: Verify OTP via JSON POST
        response = self.client.post(
            "/verify/",
            data=json.dumps({"otp": otp}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"), "OTP verification should succeed")

        # Step 3: Access home page after verification
        session = self.client.session
        session["verified"] = True
        session.save()
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OTP Verified")
