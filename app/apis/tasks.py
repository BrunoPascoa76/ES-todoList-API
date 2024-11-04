from flask import redirect, request,url_for
from flask_restx import Namespace, Resource,fields

from services.db_service import add_task, get_tasks_by_user_id
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
    @api.response(200,"returns a list of tasks",fields.List(fields.Nested(task_model)))
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
            return [task.as_dict() for task in tasks],200

    @api.doc("add a new task")
    @api.expect({
        "title":fields.String(required=True),
        "description":fields.String(required=False),
        "deadline":fields.DateTime(required=False),
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
        deadline=data.get("deadline",None)
        category=data.get("category","default")
        priority=data.get("priority",0)

        result=add_task(user_id=user_id,title=title,description=description,deadline=deadline,category=category,priority=priority).as_dict()
        if from_form:
            return redirect(url_for("get tasks"))
        else:
            return result,200
        