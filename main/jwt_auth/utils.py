import jwt
import uuid

# from mailjet_rest import Client
from django.conf import settings
from datetime import datetime, timedelta


def get_reset_token(email, secret_key):
    exp = datetime.utcnow() + timedelta(minutes=15)  # Token valid for 15 minutes
    iat = datetime.utcnow()
    jti = str(uuid.uuid4())

    payload = {
        'token_type': 'reset',
        'exp': exp,
        'iat': iat,
        'jti': jti,
        'email': email
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token


def send_password_reset_email(email, token):
    # mailjet = Client(auth=(settings.MAILJET_KEY, settings.MAILJET_SECRET), version='v3.1')

    data = {
        'Messages': [
            {
                'From': {
                    'Email': 'rbkd006@gmail.com',
                    'Name': 'Test'
                },
                'To': [
                    {
                        #'Email': email,
                        'Email': 'boukadidarami0@gmail.com',
                        'Name': email
                    }
                ],
                'Subject': 'Reset your password',
                'TextPart': 'Reset your password',
                'HTMLPart': f'<h3>Reset your password</h3><p>Your token : {token}</p><p>Click <a href="http://localhost:3000/jwt/reset/password/confirm/">here</a> to reset your password.</p>',

            }
        ]
    }

    # response = mailjet.send.create(data=data)
    return 200, {'message': 'Email sent successfully.'}
    # return response.status_code, response.json()
