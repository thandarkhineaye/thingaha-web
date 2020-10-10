"""API route for extrafund API"""
from flask import request, current_app, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from common.error import SQLCustomError, RequestDataEmpty, ValidateFail
from controller.api import api, post_request_empty
from service.extrafund.extrafund_service import ExtrafundService

extrafund_service = ExtrafundService()


@api.route("/extrafund/<int:extrafund_id>", methods=["GET"])
@jwt_required
@cross_origin()
def get_extrafund_by_id(extrafund_id: int):
    """
    get extrafund by id
    :param extrafund_id:
    :return:
    """
    try:
        extrafund = extrafund_service.get_extrafund_by_id(extrafund_id)
        current_app.logger.info("Return data for extrafund_id: {}".format(extrafund_id))
        return jsonify({
            "data": {
                "extrafund": extrafund
            }}), 200
    except SQLCustomError as error:
        current_app.logger.error("Return error for extrafund_id: {}".format(extrafund_id))
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400



@api.route("/extrafund", methods=["POST"])
@jwt_required
@cross_origin()
def create_extrafund():
    """
     create extrafund data
     :return:
     """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        current_app.logger.info("create extrafund")
        extrafund_id = extrafund_service.create_extrafund({
            "extrafund_id": data.get("extrafund_id"),
            "mmk_amount": data.get("mmk_amount"),
            "tranfer_id": data.get("tranfer_id"),
        })
        current_app.logger.info("create extrafund success. extrafund %s", data.get("street_extrafund"))
        return get_extrafund_by_id(extrafund_id)
    except (SQLCustomError, ValidateFail, RequestDataEmpty) as error:
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400

@api.route("/extrafund/<int:extrafund_id>", methods=["PUT"])
@jwt_required
@cross_origin()
def update_extrafund(extrafund_id: int):
    """
    update extrafund data
    :param extrafund_id:
    :return:
    """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        current_app.logger.info("update extrafund for extrafund_id: %s", extrafund_id)
        return jsonify({
            "status": extrafund_service.update_extrafund_by_id(extrafund_id, data)
        }), 200
    except (SQLCustomError, ValidateFail, RequestDataEmpty) as error:
        current_app.logger.error("update extrafund fail: extrafund_id: %s", extrafund_id)
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400


@api.route("/extrafund/<int:extrafund_id>", methods=["DELETE"])
@jwt_required
@cross_origin()
def delete_extrafund(extrafund_id: int):
    """
    delete extrafund by id
    :param extrafund_id:
    :return:
    """
    try:
        current_app.logger.info("delete extrafund : extrafund_id: %s", extrafund_id)
        return jsonify({
            "status": extrafund_service.delete_extrafund_by_id(extrafund_id)
        }), 200
    except SQLCustomError as error:
        current_app.logger.error("fail to delete extrafund : extrafund_id: %s", extrafund_id)
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400
    
@api.route("/extrafund", methods=["GET"])
@jwt_required
@cross_origin()
def get_all_extrafund():
    """
    get all extrafund list
    :return:
    """
    try:
        extrafund = extrafund_service.get_all_extrafund()
        current_app.logger.info("get all extrafund Amount")
        return jsonify({
            "data": {
                "count": len(extrafund),
                "extrafund": extrafund
            }}), 200
    except SQLCustomError as error:
        current_app.logger.error("fail to get all extrafund: %s", error)
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400