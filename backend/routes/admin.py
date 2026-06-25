from datetime import datetime, timedelta

from flask import Blueprint, current_app, request
from sqlalchemy import func

from extensions import db
from models import Course, Order, TeacherProfile, User
from services.order_service import order_to_dict
from services.settings_service import as_response, set_values
from utils.decorators import role_required
from utils.response import error, success

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

SUBJECT_LABELS = {
    "math": "数学",
    "logic": "逻辑",
    "writing": "写作",
    "english": "英语二",
}

ROLE_LABELS = {"student": "学生", "teacher": "教师", "admin": "管理员"}


@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard(user):
    revenue = (
        db.session.query(func.coalesce(func.sum(Order.amount), 0))
        .filter(Order.status == "paid")
        .scalar()
    )
    return success(
        {
            "user_count": User.query.count(),
            "teacher_count": TeacherProfile.query.filter_by(status="approved").count(),
            "pending_teachers": TeacherProfile.query.filter_by(status="pending").count(),
            "course_count": Course.query.filter_by(status="published").count(),
            "order_count": Order.query.filter_by(status="paid").count(),
            "total_revenue": float(revenue or 0),
        }
    )


@admin_bp.get("/analytics")
@role_required("admin")
def analytics(user):
    since = datetime.utcnow() - timedelta(days=7)
    revenue_7d = (
        db.session.query(func.coalesce(func.sum(Order.amount), 0))
        .filter(Order.status == "paid", Order.paid_at >= since)
        .scalar()
    )
    new_users_7d = User.query.filter(User.created_at >= since).count()
    orders_7d = Order.query.filter(Order.status == "paid", Order.paid_at >= since).count()

    col = current_app.mongo_db.questions
    question_stats = []
    for subject in ("math", "logic", "writing", "english"):
        question_stats.append(
            {
                "subject": subject,
                "subject_label": SUBJECT_LABELS.get(subject, subject),
                "count": col.count_documents({"subject": subject}),
            }
        )

    recent_orders = Order.query.filter_by(status="paid").order_by(
        Order.paid_at.desc()
    ).limit(5).all()

    return success(
        {
            "revenue_7d": float(revenue_7d or 0),
            "new_users_7d": new_users_7d,
            "orders_7d": orders_7d,
            "question_stats": question_stats,
            "recent_orders": [order_to_dict(o, include_user=True) for o in recent_orders],
        }
    )


@admin_bp.get("/users")
@role_required("admin")
def list_users(user):
    role = request.args.get("role")
    q = request.args.get("q")
    query = User.query
    if role:
        query = query.filter_by(role=role)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (User.nickname.like(like))
            | (User.email.like(like))
            | (User.phone.like(like))
        )
    users = query.order_by(User.created_at.desc()).limit(100).all()
    return success([u.to_dict() for u in users])


@admin_bp.put("/users/<int:user_id>/role")
@role_required("admin")
def update_user_role(user, user_id):
    if user_id == user.id:
        return error("FORBIDDEN", "不能修改自己的角色", 403)
    target = User.query.get(user_id)
    if not target:
        return error("NOT_FOUND", "用户不存在", 404)
    data = request.get_json() or {}
    role = data.get("role")
    if role not in ROLE_LABELS:
        return error("INVALID_INPUT", "无效角色", 400)
    target.role = role
    db.session.commit()
    return success(target.to_dict(), "角色已更新")


@admin_bp.get("/teachers")
@role_required("admin")
def list_teachers(user):
    status = request.args.get("status")
    profiles = TeacherProfile.query
    if status:
        profiles = profiles.filter_by(status=status)
    items = []
    for p in profiles.all():
        u = User.query.get(p.user_id)
        items.append(
            {
                "user_id": p.user_id,
                "nickname": u.nickname if u else None,
                "email": u.email if u else None,
                "real_name": p.real_name,
                "status": p.status,
                "expertise": p.expertise,
                "bio": p.bio,
                "commission_rate": float(p.commission_rate),
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "approved_at": p.approved_at.isoformat() if p.approved_at else None,
            }
        )
    items.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return success(items)


@admin_bp.put("/teachers/<int:user_id>/commission")
@role_required("admin")
def update_teacher_commission(user, user_id):
    profile = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return error("NOT_FOUND", "教师不存在", 404)
    data = request.get_json() or {}
    rate = data.get("commission_rate")
    if rate is None:
        return error("INVALID_INPUT", "请提供分成比例", 400)
    rate = float(rate)
    if rate < 0 or rate > 1:
        return error("INVALID_INPUT", "分成比例须在 0~1 之间", 400)
    profile.commission_rate = rate
    db.session.commit()
    return success({"commission_rate": float(profile.commission_rate)}, "分成比例已更新")


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
    status = request.args.get("status")
    q = Order.query.order_by(Order.created_at.desc())
    if status:
        q = q.filter_by(status=status)
    orders = q.limit(100).all()
    return success([order_to_dict(o, include_user=True) for o in orders])


@admin_bp.get("/questions")
@role_required("admin")
def list_questions(user):
    subject = request.args.get("subject")
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 50)
    query = {}
    if subject:
        query["subject"] = subject

    col = current_app.mongo_db.questions
    total = col.count_documents(query)
    items = []
    for doc in col.find(query).skip((page - 1) * page_size).limit(page_size):
        items.append(
            {
                "question_id": doc.get("question_id"),
                "subject": doc.get("subject"),
                "subject_label": SUBJECT_LABELS.get(doc.get("subject"), doc.get("subject")),
                "question_type": doc.get("question_type"),
                "difficulty": doc.get("difficulty"),
                "tag": doc.get("tags", {}).get("primary"),
                "stem": doc.get("content", {}).get("stem"),
                "correct_answer": doc.get("content", {}).get("correct_answer"),
                "stats": doc.get("stats", {}),
            }
        )
    return success(
        items,
        pagination={"page": page, "page_size": page_size, "total": total},
    )


@admin_bp.get("/settings")
@role_required("admin")
def get_settings(user):
    return success(as_response())


@admin_bp.put("/settings")
@role_required("admin")
def update_settings(user):
    data = request.get_json() or {}
    flat = {}
    if "quota" in data:
        q = data["quota"]
        flat.update(
            {
                k: q[k]
                for k in (
                    "free_daily_questions",
                    "wrong_quota_penalty",
                    "max_wrong_before_quota",
                    "points_per_question_after_quota",
                )
                if k in q
            }
        )
    if "ai" in data:
        ai = data["ai"]
        if "writing_points" in ai:
            flat["ai_writing_points"] = ai["writing_points"]
        if "video_analysis_points" in ai:
            flat["ai_video_analysis_points"] = ai["video_analysis_points"]
    if "referral" in data:
        r = data["referral"]
        mapping = {
            "default_commission_rate": "default_referral_commission_rate",
            "max_commission_rate": "max_commission_rate",
            "withdraw_min_amount": "withdraw_min_amount",
        }
        for src, dst in mapping.items():
            if src in r:
                flat[dst] = r[src]
    set_values(flat)
    return success(as_response(), "系统配置已更新")


@admin_bp.put("/settings/referral")
@role_required("admin")
def update_referral_settings(user):
    data = request.get_json() or {}
    flat = {}
    if "default_commission_rate" in data:
        flat["default_referral_commission_rate"] = data["default_commission_rate"]
    if "max_commission_rate" in data:
        flat["max_commission_rate"] = data["max_commission_rate"]
    if "withdraw_min_amount" in data:
        flat["withdraw_min_amount"] = data["withdraw_min_amount"]
    set_values(flat)
    return success(as_response()["referral"], "分销规则已更新")
