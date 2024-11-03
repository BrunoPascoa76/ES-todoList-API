import base64
import os
import sys
import boto3
import requests

from secret import API_URL, AWS_COGNITO_USER_POOL_CLIENT_ID, AWS_COGNITO_USER_POOL_CLIENT_SECRET, AWS_REGION, TOKEN_URL


cognito=boto3.client('cognito-idp',AWS_REGION)

#lazy create: the user is added to the database the first time it is needed
def get_user(authorization_token):
    try:
        return cognito.get_user(AccessToken=authorization_token)
    except cognito.exceptions.NotAuthorizedException:
        return None

def exchange_token(authorization_code):
    message = bytes(f"{AWS_COGNITO_USER_POOL_CLIENT_ID}:{AWS_COGNITO_USER_POOL_CLIENT_SECRET}",'utf-8')
    secret_hash = base64.b64encode(message).decode()
    payload = {
        "grant_type": 'authorization_code',
        "client_id": AWS_COGNITO_USER_POOL_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": f"{API_URL}/api/v1/auth/redirect"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {secret_hash}"}
           
    response = requests.post(TOKEN_URL, params=payload, headers=headers)
    if response.status_code==200:
        tokens = response.json()
        return tokens.get("access_token")
    else:
        return None
