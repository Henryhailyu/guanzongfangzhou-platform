from datetime import datetime

from flask import Blueprint, request

from extensions import db
from models import Course, Order, TeacherProfile, User
from utils.decorators import role_required
from utils.response import error, success

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard(user):
    return success(
        {
            "user_count": User.query.count(),
            "teacher_count": TeacherProfile.query.filter_by(status="approved").count(),
            "pending_teachers": TeacherProfile.query.filter_by(status="pending").count(),
            "course_count": Course.query.filter_by(status="published").count(),
            "order_count": Order.query.filter_by(status="paid").count(),
        }
    )


@admin_bp.get("/users")
@role_required("admin")
def list_users(user):
    users = User.query.order_by(User.created_at.desc()).limit(100).all()
    return success([u.to_dict() for u in users])


@admin_bp.get("/teachers")
@role_required("admin")
def list_teachers(user):
    profiles = TeacherProfile.query.all()
    items = []
    for p in profiles:
        u = User.query.get(p.user_id)
        items.append(
            {
                "user_id": p.user_id,
                "nickname": u.nickname if u else None,
                "real_name": p.real_name,
                "status": p.status,
                "expertise": p.expertise,
                "commission_rate": float(p.commission_rate),
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
        )
    return success(items)


@admin_bp.put("/teachers/<int:user_id>/reject")
@role_required("admin")
def reject_teacher(user, user_id):
    profile = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return error("NOT_FOUND", "教师不存在", 404)
    profile.status = "rejected"
    db.session.commit()
    return success(None, "已拒绝该教师申请")


@admin_bp.put("/teachers/<int:user_id>/approve")
@role_required("admin")
def approve_teacher(user, user_id):
    profile = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return error("NOT_FOUND", "教师不存在", 404)
    profile.status = "approved"
    profile.approved_by = user.id
    profile.approved_at = datetime.utcnow()
    u = User.query.get(user_id)
    if u:
        u.role = "teacher"
    db.session.commit()
    return success(None, "教师已审核通过")


@admin_bp.put("/teachers/<int:user_id>/suspend")
@role_required("admin")
def suspend_teacher(user, user_id):
    profile = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return error("NOT_FOUND", "教师不存在", 404)
    profile.status = "suspended"
    db.session.commit()
    return success(None, "教师已暂停")


@admin_bp.get("/courses")
@role_required("admin")
def list_courses(user):
    courses = Course.query.order_by(Course.created_at.desc()).limit(100).all()
    items = []
    for c in courses:
        d = c.to_dict()
        d["lesson_count"] = c.lessons.count()
        items.append(d)
    return success(items)


@admin_bp.put("/courses/<int:course_id>/status")
@role_required("admin")
def set_course_status(user, course_id):
    course = Course.query.get(course_id)
    if not course:
        return error("NOT_FOUND", "课程不存在", 404)
    data = request.get_json() or {}
    status = data.get("status")
    if status not in ("draft", "published", "archived"):
        return error("INVALID_INPUT", "无效状态", 400)
    course.status = status
    db.session.commit()
    return success(course.to_dict(), "课程状态已更新")


@admin_bp.get("/orders")
@role_required("admin")
def list_orders(user):
    orders = Order.query.order_by(Order.created_at.desc()).limit(100).all()
    from services.order_service import order_to_dict

    return success([order_to_dict(o, include_user=True) for o in orders])
