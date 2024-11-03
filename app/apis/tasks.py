from flask_restx import Namespace


api=Namespace("tasks",path="/api/v1/task",description="Task management operations")