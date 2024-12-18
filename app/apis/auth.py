import os
from urllib import response
import boto3
from flask import json, jsonify, redirect, request, url_for
from flask_restx import Namespace,Resource,fields
from services.auth_service import exchange_token, get_user
from secret import AWS_COGNITO_HOSTED_URL,API_URL, AWS_COGNITO_USER_POOL_CLIENT_ID, AWS_REGION
import jwt

api=Namespace("auth",path="/api/v1/auth",description="Authentication operations")

cognito=boto3.client('cognito-idp',AWS_REGION)

@api.route("/login")
class Login(Resource):
    @api.doc('login via hosted ui')
    def get(self):
        return redirect(f"{AWS_COGNITO_HOSTED_URL}&client_id={AWS_COGNITO_USER_POOL_CLIENT_ID}&redirect_uri={API_URL}/api/v1/auth/redirect")
        
@api.route("/sign_out")
class SignOut(Resource):
    @api.doc("sign out")
    @api.response(301,"redirecting to home page")
    def get(self):
        resp=redirect("/ui/")
        resp.delete_cookie("access_token")
        return resp
        
@api.route("/redirect")
class Redirect(Resource):
    @api.expect({
        "code":fields.String(required=True)
    })
    @api.response(400,"code not returned")
    @api.response(500,"error enchanging code")
    @api.response(301,"redirect to home page")
    def get(self):
        if "code" in request.args:
            token=exchange_token(request.args.get("code"))
            resp=redirect("/ui/")
            resp.set_cookie("access_token",token,httponly=True,secure=True)
            return resp
        else:
            return "code not returned",400
        
@api.route("/get_current_user") #this route can be used for testing
class GetCurrentUser(Resource):
    def get(self):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')         
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return redirect("/api/v1/auth/login")

        return get_user(access_token)

            