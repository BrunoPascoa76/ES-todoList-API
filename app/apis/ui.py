from flask import make_response, redirect, render_template, request, url_for
from flask_restx import Namespace, Resource

from secret import AWS_COGNITO_HOSTED_URL


api=Namespace("ui",description="UI-related endpoints")

@api.route("/")
class HomePage(Resource):
    def get(self):
        if "access_token" in request.cookies:
            return make_response(render_template("homePage.html"),200,{"Content-type":"text/html"})
        else:
            return redirect(url_for("auth_login"))