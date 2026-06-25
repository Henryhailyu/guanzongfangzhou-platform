import secrets

from flask import Blueprint, request

from sqlalchemy import and_, func

from extensions import db
from models import (
    Course,
    CourseEnrollment,
    Lesson,
    Order,
    ReferralLink,
    TeacherMarketingConfig,
    TeacherProfile,
    User,
)
from utils.decorators import approved_teacher_required, role_required
from utils.response import error, success

teacher_bp = Blueprint("teacher", __name__, url_prefix="/api/teacher")


@teacher_bp.get("/profile")
@role_required("teacher")
def get_profile(user):
    profile = TeacherProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        return error("NOT_FOUND", "教师资料不存在", 404)
    return success(
        {
            "status": profile.status,
            "real_name": profile.real_name,
            "expertise": profile.expertise,
            "bio": profile.bio,
            "commission_rate": float(profile.commission_rate),
        }
    )


@teacher_bp.get("/dashboard")
@approved_teacher_required
def dashboard(user, profile):
    courses = Course.query.filter_by(teacher_id=user.id).count()
    students = CourseEnrollment.query.filter_by(teacher_id=user.id).count()
    orders = (
        db.session.query(func.coalesce(func.sum(Order.amount), 0))
        .join(Course, Order.product_id == Course.id)
        .filter(
            Order.product_type == "course",
            Order.status == "paid",
            Course.teacher_id == user.id,
        )
        .scalar()
    )
    return success(
        {
            "course_count": courses,
            "student_count": students,
            "total_revenue": float(orders or 0),
            "commission_rate": float(profile.commission_rate),
        }
    )


@teacher_bp.get("/courses")
@approved_teacher_required
def my_courses(user, profile):
    courses = Course.query.filter_by(teacher_id=user.id).all()
    return success([c.to_dict() for c in courses])


@teacher_bp.post("/courses")
@approved_teacher_required
def create_course(user, profile):
    data = request.get_json() or {}
    course = Course(
        title=data.get("title", "未命名课程"),
        subject=data.get("subject", "math"),
        description=data.get("description"),
        teacher_id=user.id,
        price=data.get("price", 0),
        original_price=data.get("original_price"),
        status=data.get("status", "draft"),
    )
    db.session.add(course)
    db.session.commit()
    return success(course.to_dict(), "课程已创建")


@teacher_bp.put("/courses/<int:course_id>")
@approved_teacher_required
def update_course(user, profile, course_id):
    course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
    if not course:
        return error("NOT_FOUND", "课程不存在", 404)
    data = request.get_json() or {}
    for field in ("title", "subject", "description", "price", "original_price", "status", "is_free"):
        if field in data:
            setattr(course, field, data[field])
    db.session.commit()
    return success(course.to_dict())


def _sync_lesson_count(course_id):
    course = Course.query.get(course_id)
    if course:
        course.total_lessons = Lesson.query.filter_by(course_id=course_id).count()
        db.session.commit()


@teacher_bp.get("/courses/<int:course_id>/lessons")
@approved_teacher_required
def list_lessons(user, profile, course_id):
    course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
    if not course:
        return error("NOT_FOUND", "课程不存在", 404)
    lessons = course.lessons.order_by(Lesson.sort_order).all()
    return success([l.to_dict() for l in lessons])


@teacher_bp.post("/courses/<int:course_id>/lessons")
@approved_teacher_required
def create_lesson(user, profile, course_id):
    course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
    if not course:
        return error("NOT_FOUND", "课程不存在", 404)
    data = request.get_json() or {}
    lesson = Lesson(
        course_id=course.id,
        title=data.get("title", "未命名课时"),
        sort_order=data.get("sort_order", course.lessons.count() + 1),
        is_free=data.get("is_free", False),
        preview_sec=data.get("preview_sec", 300),
        duration_sec=data.get("duration_sec"),
        vod_file_id=data.get("vod_file_id"),
    )
    db.session.add(lesson)
    db.session.flush()
    _sync_lesson_count(course.id)
    return success(lesson.to_dict(), "课时已创建")


@teacher_bp.put("/courses/<int:course_id>/lessons/<int:lesson_id>")
@approved_teacher_required
def update_lesson(user, profile, course_id, lesson_id):
    course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
    lesson = Lesson.query.filter_by(id=lesson_id, course_id=course_id).first()
    if not course or not lesson:
        return error("NOT_FOUND", "课时不存在", 404)
    data = request.get_json() or {}
    for field in ("title", "sort_order", "is_free", "preview_sec", "duration_sec", "vod_file_id"):
        if field in data:
            setattr(lesson, field, data[field])
    db.session.commit()
    return success(lesson.to_dict())


@teacher_bp.delete("/courses/<int:course_id>/lessons/<int:lesson_id>")
@approved_teacher_required
def delete_lesson(user, profile, course_id, lesson_id):
    course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
    lesson = Lesson.query.filter_by(id=lesson_id, course_id=course_id).first()
    if not course or not lesson:
        return error("NOT_FOUND", "课时不存在", 404)
    db.session.delete(lesson)
    _sync_lesson_count(course.id)
    return success(None, "课时已删除")


@teacher_bp.get("/students")
@approved_teacher_required
def my_students(user, profile):
    enrollments = (
        CourseEnrollment.query.filter_by(teacher_id=user.id)
        .order_by(CourseEnrollment.enrolled_at.desc())
        .all()
    )
    items = []
    for e in enrollments:
        items.append(
            {
                "user_id": e.user_id,
                "nickname": e.user.nickname if e.user else None,
                "course_id": e.course_id,
                "course_title": e.course.title if e.course else None,
                "progress_pct": float(e.progress_pct or 0),
                "enrolled_at": e.enrolled_at.isoformat() if e.enrolled_at else None,
            }
        )
    return success(items)


@teacher_bp.get("/orders")
@approved_teacher_required
def teacher_orders(user, profile):
    from services.order_service import order_to_dict

    orders = (
        db.session.query(Order)
        .join(Course, and_(Order.product_id == Course.id, Order.product_type == "course"))
        .filter(Course.teacher_id == user.id)
        .order_by(Order.created_at.desc())
        .limit(100)
        .all()
    )
    commission_rate = float(profile.commission_rate or 0.7)
    items = []
    for o in orders:
        d = order_to_dict(o, include_user=True)
        if o.status == "paid":
            amount = float(o.amount or 0)
            d["teacher_income"] = round(amount * commission_rate, 2)
            d["platform_fee"] = round(amount * (1 - commission_rate), 2)
        else:
            d["teacher_income"] = 0
            d["platform_fee"] = 0
        items.append(d)
    return success(items)


@teacher_bp.get("/marketing")
@approved_teacher_required
def get_marketing(user, profile):
    config = TeacherMarketingConfig.query.filter_by(teacher_id=user.id).first()
    links = ReferralLink.query.filter_by(teacher_id=user.id, referrer_id=user.id).all()
    courses = Course.query.filter_by(teacher_id=user.id, status="published").all()

    def link_path(link):
        if link.course_id:
            return f"/courses/{link.course_id}?ref={link.code}"
        if config:
            return f"/teachers/{config.slug}?ref={link.code}"
        return f"?ref={link.code}"

    link_items = [
        {
            "id": l.id,
            "code": l.code,
            "course_id": l.course_id,
            "course_title": next((c.title for c in courses if c.id == l.course_id), "全店主页"),
            "click_count": l.click_count or 0,
            "convert_count": l.convert_count or 0,
            "url": link_path(l),
            "channel": l.channel,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }
        for l in links
    ]

    return success(
        {
            "slug": config.slug if config else None,
            "homepage_url": f"/teachers/{config.slug}" if config else None,
            "stats": {
                "total_clicks": sum(l.click_count or 0 for l in links),
                "total_conversions": sum(l.convert_count or 0 for l in links),
                "link_count": len(links),
            },
            "courses": [{"id": c.id, "title": c.title} for c in courses],
            "links": link_items,
        }
    )


@teacher_bp.put("/marketing")
@approved_teacher_required
def update_marketing(user, profile):
    import re

    config = TeacherMarketingConfig.query.filter_by(teacher_id=user.id).first()
    if not config:
        return error("NOT_FOUND", "营销配置不存在", 404)

    data = request.get_json() or {}
    slug = data.get("slug")
    if slug is not None:
        slug = slug.strip().lower()
        if not re.match(r"^[a-z0-9][a-z0-9-]{1,48}[a-z0-9]$", slug):
            return error("INVALID_INPUT", "主页地址仅支持小写字母、数字和连字符", 400)
        taken = TeacherMarketingConfig.query.filter(
            TeacherMarketingConfig.slug == slug,
            TeacherMarketingConfig.teacher_id != user.id,
        ).first()
        if taken:
            return error("SLUG_EXISTS", "该主页地址已被占用", 400)
        config.slug = slug

    db.session.commit()
    return success({"slug": config.slug, "homepage_url": f"/teachers/{config.slug}"})


@teacher_bp.post("/marketing/links")
@approved_teacher_required
def create_link(user, profile):
    data = request.get_json() or {}
    course_id = data.get("course_id")
    config = TeacherMarketingConfig.query.filter_by(teacher_id=user.id).first()
    if course_id:
        course = Course.query.filter_by(id=course_id, teacher_id=user.id).first()
        if not course:
            return error("NOT_FOUND", "课程不存在", 404)
    code = secrets.token_urlsafe(6)[:8].upper()
    link = ReferralLink(
        teacher_id=user.id,
        course_id=course_id,
        referrer_id=user.id,
        referrer_type="teacher",
        code=code,
        channel=data.get("channel", "link"),
    )
    db.session.add(link)
    db.session.commit()

    path = (
        f"/courses/{course_id}?ref={code}"
        if course_id
        else f"/teachers/{config.slug}?ref={code}" if config else f"?ref={code}"
    )
    return success(
        {"code": code, "id": link.id, "url": path},
        "推广链接已生成",
    )
