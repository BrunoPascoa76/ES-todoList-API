from flask_restx import Namespace


api=Namespace("tasks",path="/api/v1/tasks",description="Task management operations")