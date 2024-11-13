from datetime import datetime
from flask import redirect, request,url_for
from flask_restx import Namespace, Resource,fields

from services.db_service import add_task, delete_task, get_task_by_id, get_tasks_by_user_id, toggle_completed, update_task
from services.auth_service import get_user


api=Namespace("tasks",path="/api/v1/tasks",description="Task management operations")

task_model=api.model("task",{
    "id":fields.Integer,
    "userId":fields.String,
    "title":fields.String,
    "description":fields.String,
    "deadline":fields.DateTime,
    "is_completed":fields.Boolean,
    "category":fields.String,
    "created_date":fields.DateTime
})

@api.route("/",endpoint="tasks")
class Tasks(Resource):
    @api.doc("list all of the user's tasks")
    @api.param("sort_by",enum=["title","description","priority","deadline","category","is_completed","created_date"],required=False)
    @api.response(200,"returns a list of tasks",fields.List(fields.Nested(task_model)))
    @api.response(400,"wrong filter/sort")
    @api.response(401,"not authorized")
    def get(self):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401

        user=get_user(access_token)
        if user is None or "Username" not in user:
            return "not authorized",401
        else:
            user_id=user["Username"]
            tasks=get_tasks_by_user_id(user_id)
            if "sort_by" in request.args and request.args["sort_by"] is not None and request.args["sort_by"]!="default":
                if request.args["sort_by"] not in ["title","description","priority","deadline","category","is_completed","created_date"]:
                    return "wrong filter/sort",400
                tasks=sorted(tasks,key=lambda task: getattr(task,request.args["sort_by"]))
            return [task.as_dict() for task in tasks],200

    @api.doc("add a new task")
    @api.expect({
        "title":fields.String(required=True),
        "description":fields.String(required=False),
        "deadline":fields.DateTime(required=False),
        "deadlineDate":fields.Date(required=False),
        "deadlineTime":fields.DateTime(required=False),
        "category":fields.String(required=False),
        "priority":fields.Integer(required=False)
    })
    @api.response(200,"returns the created task (redirects to home if from form)",model=task_model)
    @api.response(400,"wrong body")
    @api.response(401,"not authorized")
    def post(self):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401
            

        user=get_user(access_token)
        if user is None or "Username" not in user:
            return "not authorized",400   
        user_id=user["Username"]
        
        if request.form and "title" in request.form:  #they used a form
            from_form=True
            data=request.form
        else:
            data=request.json
            from_form=False

        if "title" not in data:
            return "wrong body",400
        title=data["title"]
       
        description=data.get("description",None)
        category=data.get("category","default")
        priority=data.get("priority",0)

        if "deadline" in data:
            deadline=data["deadline"]
        elif "deadlineDate" in data and "deadlineTime" in data:
            deadline=datetime.combine(datetime.datetime(data["deadlineDate"]),datetime.datetime(data["deadlineTime"]))
        else:
            deadline=None

        result=add_task(user_id=user_id,title=title,description=description,deadline=deadline,category=category,priority=priority).as_dict()
        if from_form:
            return redirect(url_for("get tasks"))
        else:
            return result,200
        
@api.route("/<int:task_id>",endpoint="task details")
class Task(Resource):
    @api.doc("get a task")
    @api.response(200,"returns the task",model=task_model)
    @api.response(404,"task not found")
    @api.response(401,"not authorized")
    def get(self,task_id):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401

        user=get_user(access_token)
        if user is None or "Username" not in user:
            return "not authorized",401
        else:
            user_id=user["Username"]
            

        task,code=get_task_by_id(task_id,user_id)
        if code==404:
            return "task not found",404
        elif code==401:
            return "not authorized",401
        else:
            return task.as_dict(),200
        
    @api.doc("update a task")
    @api.expect({
        "title":fields.String(required=False),
        "description":fields.String(required=False),
        "deadline":fields.DateTime(required=False),
        "deadlineDate":fields.Date(required=False),
        "deadlineTime":fields.DateTime(required=False),
        "category":fields.String(required=False),
        "priority":fields.Integer(required=False)
    })
    @api.response(200,"task updated")
    @api.response(404,"task not found")
    @api.response(401,"not authorized")
    def post(self,task_id):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401

        user=get_user(access_token)

        if user is None or "Username" not in user:
            return "not authorized",401
        else:
            user_id=user["Username"]
            
        if request.form:
            data=request.form
            from_form=True
        else:
            data=request.json
            from_form=False

        title=None
        description=None
        deadline=None
        category=None
        priority=None
        
        if "title" in data:
            title=data["title"]
        if "description" in data:
            description=data["description"]
        if "deadline" in data:
            deadline=data["deadline"]
        elif "deadlineDate" in data and "deadlineTime" in data:
            deadline=datetime.combine(datetime.strptime(data["deadlineDate"], "%Y-%m-%d").date(),datetime.strptime(data["deadlineTime"], "%H:%M").time())
        if "category" in data:
            category=data["category"]
        if "priority" in data:
            priority=data["priority"]
        
        task,code=update_task(task_id,user_id,title=title,description=description,deadline=deadline,category=category,priority=priority)

        if code==404:
            return "task not found",404
        elif code==401:
            return "not authorized",401
        else:
            if from_form:
                return redirect(url_for("get tasks"))
            else:
                return task.as_dict(),200

@api.route("/<int:task_id>/delete",endpoint="delete task")
class DeleteTask(Resource):
    @api.doc("delete a task")
    @api.response(200,"task deleted")
    @api.response(404,"task not found")
    @api.response(401,"not authorized")
    def post(self,task_id):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401

        user=get_user(access_token)
        if user is None or "Username" not in user:
            return "not authorized",401
        else:
            user_id=user["Username"]
            
        code=delete_task(task_id,user_id)
        if code==404:
            return "task not found",404
        elif code==401:
            return "not authorized",401
        else:
            return redirect(url_for("get tasks"))
        
@api.route("/<int:task_id>/togle_complete",endpoint="toggle completion")
class ToggleCompletion(Resource):
    @api.doc("toggle completion")
    @api.response(200,"task toggled")
    @api.response(404,"task not found")
    @api.response(401,"not authorized")
    def post(self,task_id):
        if 'x-amzn-oidc-accesstoken' in request.headers:
            access_token = request.headers.get('x-amzn-oidc-accesstoken')
        elif "access_token" in request.cookies:
            access_token=request.cookies.get("access_token")
        else:
            return "not authorized",401

        user=get_user(access_token)
        if user is None or "Username" not in user:
            return "not authorized",401
        else:
            user_id=user["Username"]
            
        code=toggle_completed(task_id,user_id)

        if code==404:
            return "task not found",404
        elif code==401:
            return "not authorized",401
        else:
            return redirect(url_for("get tasks"))