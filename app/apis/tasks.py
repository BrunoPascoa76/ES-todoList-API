from flask import request
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

@api.route("/")
class Tasks(Resource):
    @api.doc("list all of the user's tasks")
    @api.response(200,"returns a list of tasks",fields.List(fields.Nested(task_model)))
    @api.response(401,"not authorized")
    def get(self):
        if "access_token" in request.cookies:
            token=request.cookies.get("access_token")
            user=get_user(token)
            if user is None or "Username" not in user:
                return "not authorized",401
            else:
                user_id=user["Username"]
                tasks=get_tasks_by_user_id(user_id)
                return [task.as_dict() for task in tasks],200
        else:
            return "not authorized",401

    @api.doc("add a new task")
    @api.expect({
        "title":fields.String(required=True),
        "description":fields.String(required=False),
        "deadline":fields.DateTime(required=False),
        "category":fields.String(required=False),
        "priority":fields.Integer(required=False)
    })
    @api.response(200,"returns the created task",model=task_model)
    @api.response(400,"wrong body")
    @api.response(401,"not authorized")
    def post(self):
        if "access_token" not in request.cookies:
            return "not authorized",400
        
        token=request.cookies.get("access_token")
        user=get_user(token)
        if user is None or "Username" not in user:
            return "not authorized",400   
        user_id=user["Username"]

        data=request.json
        if "title" not in data:
            return "wrong body",400
        title=data["title"]
       
        description=data.get("description",None)
        deadline=data.get("deadline",None)
        category=data.get("category","default")
        priority=data.get("priority",0)

        return add_task(title=title,description=description,deadline=deadline,category=category,priority=priority).as_dict(),200