from flask_api import status
from flask import request, Response
import json

def construct_json_response(response):
    if response.get("http_code_only"):
        return Response(json.dumps({
            "message": construct_http_code_message(response.get("http_code"))
        }), status=int(response.get("http_code")), mimetype="application/json")
    else:
        return Response(json.dumps({
            "message": construct_http_code_message(response.get("http_code")),
            "data": response.get("data")
        }), status=int(response.get("http_code")), mimetype="application/json")


def construct_http_code_message(http_code):
    return {
        "code": http_code,
        "description": create_message(http_code)
    }


def create_message(http_code):
    error_code_switch = {
        status.HTTP_200_OK: "Operation successful",
        status.HTTP_201_CREATED: "Successfully created",
        status.HTTP_202_ACCEPTED: "Inputs were accepted",
        status.HTTP_401_UNAUTHORIZED: "Your given inputs were invalid",
        status.HTTP_403_FORBIDDEN: "You are not allowed to access this data",
        status.HTTP_404_NOT_FOUND: "Sorry, a record could not be fetched from your inputs",
        status.HTTP_406_NOT_ACCEPTABLE: "Given input has invalid parameters",
        status.HTTP_409_CONFLICT: "Given input has a conflict",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Something wrong with the server",
    }

    return error_code_switch.get(http_code, "")

