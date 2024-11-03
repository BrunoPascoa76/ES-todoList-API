from flask import redirect, render_template, request
from flask_restx import Namespace, Resource

from secret import AWS_COGNITO_HOSTED_URL


api=Namespace("ui",description="UI-related endpoints")

@api.route("/")
class HomePage(Resource):
    def get(self):
        if "access_token" in request.cookies:
            return render_template("homePage.html")
        else:
            return redirect(AWS_COGNITO_HOSTED_URL)