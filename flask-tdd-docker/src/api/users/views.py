from http import HTTPStatus

from flask import request
from flask_restx import Resource, fields, Namespace

from src.api.users.crud import (
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)

users_namespace = Namespace("users")

user_model = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @users_namespace.expect(user_model, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, HTTPStatus.BAD_REQUEST

        add_user(username, email)

        response_object["message"] = f"{email} was added!"
        return response_object, HTTPStatus.CREATED

    @users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        return get_all_users(), HTTPStatus.OK


class Users(Resource):
    @users_namespace.marshal_with(user_model)
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(
                HTTPStatus.NOT_FOUND, f"User {user_id} does not exist"
            )
        return user, HTTPStatus.OK

    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(
                HTTPStatus.NOT_FOUND, f"User {user_id} does not exist"
            )

        delete_user(user)

        response_object["message"] = f"{user.email} was removed!"
        return response_object, HTTPStatus.OK

    @users_namespace.expect(user_model, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(user, username, email)

        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")