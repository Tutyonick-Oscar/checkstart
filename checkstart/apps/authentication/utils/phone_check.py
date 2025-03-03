import requests
from intergeld.settings.settings import SINCH_API_KEY, SINCH_API_SECRET
from requests.auth import HTTPBasicAuth

# from twilio.base.exceptions import TwilioRestException
# from twilio.rest import Client
# from rest_framework.response import Response
# from hebridge.settings.settings import TWILIO_AUTH_TOKEN,TWILIO_SID,TWILIO_VERIFY_SERVICE_SID


# twilio_client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)

# def twilio_verification_check(sid,code):
#     try:
#         verification_check = twilio_client.verify.v2.services(
#             TWILIO_VERIFY_SERVICE_SID
#         ).verification_checks.create(verification_sid=sid,code=code)
#     except TwilioRestException as e:
#             return Response(e.__dict__,500)

#     if verification_check.status != 'approved':
#         return Response({
#             'verification_check.status' : verification_check.status,
#             'message' : 'wrong code given !'
#         })
#     else:
#         pass


# def twilio_verifcation(phone,channel='sms'):
#     verification = twilio_client.verify.v2.services(
#         TWILIO_VERIFY_SERVICE_SID
#     ).verifications.create(to=phone, channel=channel)

#     return {
#         'verification.sid' : verification.sid,
#         'verification.channel' :  verification.channel,
#         'verification.amount' : verification.amount,
#         'verification.date_created' : verification.date_created,
#         'verification.date_updated' : verification.date_updated,
#         'verification.send_code_attempts' :verification.send_code_attempts,
#         'verification.status' :  verification.status,
#         'verification.lookup' : verification.lookup
#     }
username = SINCH_API_KEY
password = SINCH_API_SECRET
headers = {"Content-Type": "application/json"}
basic_auth = HTTPBasicAuth(username, password)


def initiate_phone_verification(phone):
    url = "https://verification.api.sinch.com/verification/v1/verifications"
    payload = {"identity": {"type": "number", "endpoint": phone}, "method": "sms"}
    response = requests.post(
        url, json=payload, auth=basic_auth, headers=headers, timeout=180
    )
    return response.json()


def verify_code(code, url):
    payload = {"method": "sms", "sms": {"code": code}}
    response = requests.put(
        url, json=payload, auth=basic_auth, headers=headers, timeout=180
    )
    return response.json().get("status")
