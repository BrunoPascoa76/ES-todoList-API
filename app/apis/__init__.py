from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('apis', __name__)

api = Api(version="1.0",title="Todo List",description="TodoList for the individual project",prefix="/")

from .auth import api as api_auth
from .ui import api as api_ui
from .tasks import api as api_tasks

api.add_namespace(api_auth)
api.add_namespace(api_ui)
api.add_namespace(api_tasks)