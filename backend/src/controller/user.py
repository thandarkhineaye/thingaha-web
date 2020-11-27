"""API route for User API"""

from flask import request, current_app, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from common.error import SQLCustomError, RequestDataEmpty, ValidateFail
from controller.api import api, custom_error, post_request_empty, sub_admin, full_admin
from service.address.address_service import AddressService
from service.user.user_service import UserService

address_service = AddressService()
user_service = UserService()


@api.route("/users", methods=["GET"])
@jwt_required
@cross_origin()
def get_all_users():
    """
    get all users list
    """
    try:
        page = request.args.get("page", 1, type=int)
        role = request.args.get("role")
        country = request.args.get("country")
        users, count = user_service.get_all_users(page, role, country)
        current_app.logger.info("Get all users")
        return jsonify({
            "data": {
                "count": count,
                "users": users
            }}), 200
    except SQLCustomError as error:
        current_app.logger.error("Fail to get all users: %s", error)
        return jsonify({"errors": [error.__dict__]}), 400


@api.route("/users/<int:user_id>", methods=["GET"])
@jwt_required
@cross_origin()
def get_user_by_id(user_id: int):
    """
    get user by id
    :return:
    """
    try:
        current_app.logger.info("Get user_id: %s", user_id)
        return jsonify({
            "data": {
                "user": user_service.get_user_by_id(user_id)
            }}), 200
    except SQLCustomError as error:
        current_app.logger.error("Fail to get user_id: %s", user_id)
        return jsonify({"errors": [error.__dict__]}), 400


@api.route("/users", methods=["POST"])
@jwt_required
@sub_admin
@cross_origin()
def create_user():
    """
    create user by post body
    :return:
    """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        address_id = address_service.create_address({
            "division": data.get("division"),
            "district": data.get("district"),
            "township": data.get("township"),
            "street_address": data.get("street_address"),
            "type": "user"
        })
        user_id = user_service.create_user({
            "name": data.get("name"),
            "email": data.get("email"),
            "address_id": address_id,
            "password": data.get("password"),
            "role": data.get("role"),
            "country": data.get("country"),
            "donation_active": True if data.get("donation_active") else False
        })
        current_app.logger.info(
            "Create user success. user_name %s", data.get("name"))
        return get_user_by_id(user_id)
    except (RequestDataEmpty, SQLCustomError, ValidateFail) as error:
        current_app.logger.error("Create user fail. user_name %s, error: %s",
                                 data.get("name"), error)
        return jsonify({"errors": [error.__dict__]}), 400


@api.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required
@sub_admin
@cross_origin()
def update_user(user_id: int):
    """
    update user info by id
    """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            return custom_error("Invalid user id supplied.")

        updated = address_service.update_address_by_id(user["address"]["id"], {
            "division": data.get("division"),
            "district": data.get("district"),
            "township": data.get("township"),
            "street_address": data.get("street_address"),
            "type": "user"
        })

        if updated:
            user_update_status = user_service.update_user_by_id(user_id, {
                "name": data.get("name"),
                "email": data.get("email"),
                "address_id": int(user["address"]["id"]),
                "password": data.get("password"),
                "role": data.get("role"),
                "country": data.get("country"),
                "donation_active": True if data.get("donation_active") else False
            })
            if user_update_status:
                current_app.logger.info("Success user update for user_id: %s", user_id)
            else:
                current_app.logger.error("Fail user update for user_id: %s", user_id)
                return custom_error("Update fail for user_id: %s", user_id)
        return get_user_by_id(user_id)
    except ValueError as error:
        current_app.logger.error(
            "Value error for address id. error: %s", error)
        return jsonify({
            "errors": {[error.__dict__]}}), 400
    except (SQLCustomError, ValidateFail, RequestDataEmpty) as error:
        current_app.logger.error(
            "Fail to update user: %s, error: %s", user_id, error)
        return jsonify({"errors": [error.__dict__]}), 400


@api.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required
@full_admin
@cross_origin()
def delete_user(user_id: int):
    """
    delete user by id
    """
    try:
        current_app.logger.info("Delete user : user_id: %s", user_id)
        user_delete_status = False
        user = user_service.get_user_by_id(user_id)
        if len(user) == 0:
            current_app.logger.error("No user id to delete: {}".format(user_id))
            return jsonify({"errors": ["No user id to delete"]}), 404

        if user_service.delete_user_by_id(user_id):
            user_delete_status = address_service.delete_address_by_id(user["address"]["id"])
        return jsonify({
            "status": user_delete_status
        }), 200
    except SQLCustomError as error:
        current_app.logger.error("Fail to delete user : user_id: %s", user_id)
        return jsonify({"errors": [error.__dict__]}), 400


@api.route("/users/search", methods=["GET"])
@jwt_required
@cross_origin()
def search_user():
    """
    search user by name , email
    """
    query = request.args.get("query")
    try:
        current_app.logger.info("search user : query: %s", query)
        return jsonify({
            "data": user_service.get_users_by_query(query)
        }), 200
    except SQLCustomError as error:
        current_app.logger.error("Fail to search user : query: %s", query)
        return jsonify({"errors": [error.__dict__]}), 400
