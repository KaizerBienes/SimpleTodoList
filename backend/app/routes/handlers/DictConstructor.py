def construct_response(http_code, data={}):
    return {
        "http_code": http_code,
        "data": data
    }
