from flask import make_response, redirect, render_template, request, url_for
from flask_restx import Namespace, Resource

from services.db_service import get_task_by_id, get_tasks_by_user_id
from services.auth_service import get_user


api=Namespace("ui",description="UI-related endpoints")

@api.route("/",endpoint="get tasks")
class HomePage(Resource):
    def get(self):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return redirect(url_for("auth_login"))

        user=get_user(access_token)
        if user is None:
            return redirect(url_for("auth_login"))
        tasks=get_tasks_by_user_id(user["Username"])

        if "sort_by" in request.args and request.args["sort_by"] is not None and request.args["sort_by"]!="default":
            if request.args["sort_by"] not in ["title","description","priority","deadline","category","is_completed","created_date"]:
                return "wrong filter/sort",400
            tasks=sorted(tasks,key=lambda task: getattr(task,request.args["sort_by"]),reverse=request.args.get("order","asc")=="desc")

        if "category" in request.args and request.args["category"] is not None and request.args["category"]!="":
            tasks=[task for task in tasks if request.args["category"] in task.category]

        if "filter_is_completed" in request.args and len(request.args.getlist("filter_is_completed"))==1:
            is_completed_filter=request.args.getlist("filter_is_completed")[0]=="Completed"
            tasks=[task for task in tasks if task.is_completed==is_completed_filter]

        return make_response(render_template("homePage.html",tasks=tasks,sort_by=request.args.get("sort_by","default"),sort_order=request.args.get("order","desc"),category=request.args.get("category",""),order=request.args.get("order","desc"),filter_is_completed=request.args.getlist("filter_is_completed")),200,{"Content-type":"text/html"})
        
@api.route("/addTask",endpoint="add task")
class AddTask(Resource):
    def get(self):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return redirect(url_for("auth_login"))

        user=get_user(access_token)
        tasks=get_tasks_by_user_id(user["Username"])
        return make_response(render_template("addTask.html",tasks=tasks),200,{"Content-type":"text/html"})

@api.route("/task/<int:task_id>",endpoint="get task")
class GetTask(Resource):
    def get(self,task_id):    
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return redirect(url_for("auth_login"))

        user=get_user(access_token)
        task,_=get_task_by_id(task_id,user["Username"])
        return make_response(render_template("task.html",task=task),200,{"Content-type":"text/html"})