from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from models import TeacherProfile, User
from utils.response import error


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return error("FORBIDDEN", "无权访问", 403)
            return fn(user, *args, **kwargs)

        return wrapper

    return decorator


def approved_teacher_required(fn):
    @wraps(fn)
    @role_required("teacher")
    def wrapper(user, *args, **kwargs):
        profile = TeacherProfile.query.filter_by(user_id=user.id).first()
        if not profile or profile.status != "approved":
            return error("TEACHER_NOT_APPROVED", "教师账号未通过审核", 403)
        return fn(user, profile, *args, **kwargs)

    return wrapper
