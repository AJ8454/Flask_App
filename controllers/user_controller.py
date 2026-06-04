from flask import Blueprint, request
from models.user_model import user_model

bp = Blueprint('user', __name__)
userObj = user_model() 

@bp.route('/user/getall')
def user_getall_controller():
    return userObj.user_getall_model()

@bp.route('/user/get/<int:id>')
def user_get_controller(id):
    return userObj.user_get_model(id)

@bp.route('/user/add', methods=['POST'])
def user_add_controller():
    return userObj.user_add_model(request.form)

@bp.route('/user/update', methods=['PUT'])
def user_update_controller():
    return userObj.user_update_model(request.form)

@bp.route('/user/delete/<int:id>', methods=['DELETE'])
def user_delete_controller(id):
    return userObj.user_delete_model(id)

@bp.route('/user/patch/<int:id>', methods=['PATCH'])
def user_patch_controller(id):
    return userObj.user_patch_model(id, request.form)

@bp.route('/user/getall/limit/<int:limit>/page/<int:page>', methods=['GET'])
def user_pagination_controller(limit, page):
    return userObj.user_pagination_model(limit, page)
