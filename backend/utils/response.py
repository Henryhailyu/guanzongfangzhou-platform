from flask import jsonify


def success(data=None, message="操作成功", pagination=None):
    payload = {"success": True, "data": data, "message": message}
    if pagination:
        payload["pagination"] = pagination
    return jsonify(payload)


def error(code, message, status=400):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status
