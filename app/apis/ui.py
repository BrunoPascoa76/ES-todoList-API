from flask import make_response, redirect, render_template, request, url_for
from flask_restx import Namespace, Resource

from services.db_service import get_tasks_by_user_id
from services.auth_service import get_user


api=Namespace("ui",description="UI-related endpoints")

@api.route("/",endpoint="get tasks")
class HomePage(Resource):
    def get(self):
        if "access_token" in request.cookies:
            token=request.cookies.get("access_token")
            user=get_user(token)
            if user is None:
                return redirect(url_for("auth_login"))
            tasks=get_tasks_by_user_id(user["Username"])
            return make_response(render_template("homePage.html",tasks=tasks),200,{"Content-type":"text/html"})
        else:
            return redirect(url_for("auth_login"))
        
@api.route("/addTask",endpoint="add task")
class AddTask(Resource):
    def get(self):
        if "access_token" in request.cookies:
            token=request.cookies.get("access_token")
            user=get_user(token)
            tasks=get_tasks_by_user_id(user["Username"])
            return make_response(render_template("addTask.html",tasks=tasks),200,{"Content-type":"text/html"})
        else:
            return redirect(url_for("auth_login"))