from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import TeacherMarketingConfig, TeacherProfile, User
from utils.response import error, success

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _user_payload(user):
    data = user.to_dict()
    if user.role == "teacher":
        profile = TeacherProfile.query.filter_by(user_id=user.id).first()
        if profile:
            data["teacher_profile"] = {
                "status": profile.status,
                "real_name": profile.real_name,
                "expertise": profile.expertise,
                "bio": profile.bio,
            }
    return data


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    nickname = data.get("nickname", "新用户")
    role = data.get("role", "student")

    if not password or (not email and not phone):
        return error("INVALID_INPUT", "请提供邮箱或手机号及密码")

    if role not in ("student", "teacher"):
        role = "student"

    if email and User.query.filter_by(email=email).first():
        return error("EMAIL_EXISTS", "邮箱已注册")
    if phone and User.query.filter_by(phone=phone).first():
        return error("PHONE_EXISTS", "手机号已注册")

    user = User(
        email=email,
        phone=phone,
        nickname=nickname,
        password_hash=generate_password_hash(password),
        role=role,
        points=50,
    )
    db.session.add(user)
    db.session.flush()

    if role == "teacher":
        real_name = data.get("real_name") or nickname
        profile = TeacherProfile(
            user_id=user.id,
            real_name=real_name,
            expertise=data.get("expertise"),
            bio=data.get("bio"),
            status="pending",
        )
        db.session.add(profile)
        db.session.add(
            TeacherMarketingConfig(teacher_id=user.id, slug=f"teacher-{user.id}")
        )

    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return success({"user": _user_payload(user), "token": token}, "注册成功")


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    account = data.get("account") or data.get("email") or data.get("phone")
    password = data.get("password")

    if not account or not password:
        return error("INVALID_INPUT", "请输入账号和密码")

    user = User.query.filter(
        (User.email == account) | (User.phone == account)
    ).first()
    if not user or not check_password_hash(user.password_hash, password):
        return error("AUTH_FAILED", "账号或密码错误", 401)

    token = create_access_token(identity=str(user.id))
    return success({"user": _user_payload(user), "token": token})


@auth_bp.get("/me")
@jwt_required()
def get_me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return error("NOT_FOUND", "用户不存在", 404)
    return success(_user_payload(user))
