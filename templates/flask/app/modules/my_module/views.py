from flask import Blueprint, request

from app.modules.my_module.services.myservice import hello


my_module_blueprint = Blueprint('my_module_blueprint', __name__)


@my_module_blueprint.route('/hello', methods=['GET'])
def myfunc():
    return hello(request)
