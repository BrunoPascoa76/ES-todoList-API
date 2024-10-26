import os
import boto3
from flask import current_app


class AuthService():
    def __init__(self):
        self.cognito=boto3.client('cognito-idp',os.environ["AWS_REGION"])

    def login(self,email,password):
        try:
            return self.cognito.initiate_auth(
                    AuthFlow="USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME":email,
                        "PASSWORD":password
                    },
                    ClientId=current_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"]
                ),200
        except self.cognito.exceptions.NotAuthorizedException:
            return 401

    def sign_up(self,email,password):
        try:
            self.cognito.sign_up(
                ClientId=current_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"],
                Username=email,
                Password=password,
            )
            return "User created. Confirm registration via email",200
        except self.cognito.exceptions.UsernameExistsException:
            return "Username already exists",409 

    def confirm_sign_up(self,email,confirmation_code):
        try:
            self.cognito.confirm_sign_up(
                ClientId=current_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"],
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return "user confirmed",200
        except self.cognito.exceptions.CodeMismatchException:
            return "Wrong confirmation code",400
        except self.cognito.exceptions.ExpiredCodeException:
            return "Confirmation code expired",410

    def sign_out(self,access_token):
        try:
            self.cognito.global_sign_out(AccessToken=access_token)
            return "signed out successful",200
        except self.cognito.exceptions.NotAuthorizedException:
            return "Invalid access token",401

    def get_user_profile(self,access_token):
        pass