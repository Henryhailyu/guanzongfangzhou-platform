from datetime import datetime

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from extensions import db
from models import Course, CourseEnrollment, Lesson, User, WrongQuestion
from utils.response import error, success

courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")
wrong_book_bp = Blueprint("wrong_book", __name__, url_prefix="/api/wrong-book")

SUBJECT_LABELS = {
    "math": "数学基础",
    "logic": "逻辑推理",
    "writing": "写作",
    "english": "英语二",
    "combo": "综合",
}


def _optional_user():
    verify_jwt_in_request(optional=True)
    uid = get_jwt_identity()
    if not uid:
        return None
    return User.query.get(int(uid))


def _enrollment(user, course_id):
    if not user:
        return None
    return CourseEnrollment.query.filter_by(user_id=user.id, course_id=course_id).first()


def _lesson_access(user, course, lesson, enrollment):
    if lesson.is_free:
        return {"can_watch": True, "mode": "preview"}
    if course.is_free or float(course.price or 0) == 0:
        return {"can_watch": True, "mode": "full"}
    if enrollment:
        return {"can_watch": True, "mode": "full"}
    return {"can_watch": False, "mode": "locked"}


def _lesson_payload(lesson, access):
    data = lesson.to_dict()
    data.update(access)
    if access["can_watch"]:
        data["play_url"] = lesson.vod_file_id or f"mock://lesson-{lesson.id}"
        data["is_mock_player"] = not lesson.vod_file_id
    return data


@courses_bp.get("")
def list_courses():
    subject = request.args.get("subject")
    q = Course.query.filter_by(status="published")
    if subject:
        q = q.filter_by(subject=subject)
    return success([c.to_dict() for c in q.all()])


@courses_bp.get("/enrolled")
@jwt_required()
def enrolled_courses():
    user_id = int(get_jwt_identity())
    items = []
    for e in CourseEnrollment.query.filter_by(user_id=user_id).order_by(
        CourseEnrollment.enrolled_at.desc()
    ):
        if not e.course:
            continue
        data = e.course.to_dict()
        data["enrolled_at"] = e.enrolled_at.isoformat() if e.enrolled_at else None
        data["progress_pct"] = float(e.progress_pct or 0)
        items.append(data)
    return success(items)


@courses_bp.get("/<int:course_id>")
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error("NOT_FOUND", "课程不存在", 404)
    if course.status != "published":
        user = _optional_user()
        if not user or (
            user.role != "admin"
            and course.teacher_id != user.id
        ):
            return error("NOT_FOUND", "课程不存在", 404)

    user = _optional_user()
    enrollment = _enrollment(user, course_id)
    data = course.to_dict()
    data["subject_label"] = SUBJECT_LABELS.get(course.subject, course.subject)
    data["enrolled"] = enrollment is not None
    data["progress_pct"] = float(enrollment.progress_pct or 0) if enrollment else 0

    lessons = []
    for lesson in course.lessons.order_by(Lesson.sort_order):
        access = _lesson_access(user, course, lesson, enrollment)
        lessons.append(_lesson_payload(lesson, access))
    data["lessons"] = lessons
    return success(data)


@courses_bp.post("/<int:course_id>/enroll-free")
@jwt_required()
def enroll_free(course_id):
    user = User.query.get(int(get_jwt_identity()))
    course = Course.query.get(course_id)
    if not course or course.status != "published":
        return error("NOT_FOUND", "课程不存在", 404)
    if not course.is_free and float(course.price or 0) > 0:
        return error("PAYMENT_REQUIRED", "该课程需要付费购买", 400)

    if _enrollment(user, course_id):
        return success({"enrolled": True}, "已加入课程")

    db.session.add(
        CourseEnrollment(user_id=user.id, course_id=course.id, teacher_id=course.teacher_id)
    )
    course.student_count = (course.student_count or 0) + 1
    db.session.commit()
    return success({"enrolled": True}, "已加入课程")


@courses_bp.get("/<int:course_id>/lessons/<int:lesson_id>")
def get_lesson(course_id, lesson_id):
    course = Course.query.get(course_id)
    lesson = Lesson.query.filter_by(id=lesson_id, course_id=course_id).first()
    if not course or not lesson:
        return error("NOT_FOUND", "课时不存在", 404)

    user = _optional_user()
    enrollment = _enrollment(user, course_id)
    access = _lesson_access(user, course, lesson, enrollment)
    if not access["can_watch"]:
        return error("FORBIDDEN", "请先购买课程或试看免费课时", 403)

    data = _lesson_payload(lesson, access)
    data["course_title"] = course.title
    all_lessons = [
        {
            "id": l.id,
            "title": l.title,
            "is_free": l.is_free,
            "sort_order": l.sort_order,
            "can_watch": _lesson_access(user, course, l, enrollment)["can_watch"],
        }
        for l in course.lessons.order_by(Lesson.sort_order)
    ]
    data["lessons"] = all_lessons
    return success(data)


@courses_bp.post("/<int:course_id>/lessons/<int:lesson_id>/progress")
@jwt_required()
def update_lesson_progress(course_id, lesson_id):
    user = User.query.get(int(get_jwt_identity()))
    course = Course.query.get(course_id)
    lesson = Lesson.query.filter_by(id=lesson_id, course_id=course_id).first()
    if not course or not lesson:
        return error("NOT_FOUND", "课时不存在", 404)

    enrollment = _enrollment(user, course_id)
    if not enrollment and not lesson.is_free and not course.is_free:
        return error("FORBIDDEN", "未购买课程", 403)

    if not enrollment and (lesson.is_free or course.is_free):
        enrollment = CourseEnrollment(
            user_id=user.id, course_id=course.id, teacher_id=course.teacher_id
        )
        db.session.add(enrollment)
        course.student_count = (course.student_count or 0) + 1

    total = course.lessons.count() or 1
    completed = lesson.sort_order or 1
    pct = min(100, round(completed / total * 100, 1))
    if enrollment:
        enrollment.progress_pct = max(float(enrollment.progress_pct or 0), pct)
        enrollment.last_active_at = datetime.utcnow()

    db.session.commit()
    return success({"progress_pct": float(enrollment.progress_pct) if enrollment else pct})


@wrong_book_bp.get("")
@jwt_required()
def wrong_book():
    user_id = int(get_jwt_identity())
    subject = request.args.get("subject")
    q = WrongQuestion.query.filter_by(user_id=user_id, is_mastered=False)
    items = []
    col = current_app.mongo_db.questions
    for w in q.order_by(WrongQuestion.last_wrong_at.desc()).all():
        doc = col.find_one({"question_id": w.question_id})
        if subject and doc and doc.get("subject") != subject:
            continue
        items.append(
            {
                "id": w.id,
                "question_id": w.question_id,
                "wrong_count": w.wrong_count,
                "last_wrong_at": w.last_wrong_at.isoformat() if w.last_wrong_at else None,
                "subject": doc.get("subject") if doc else None,
                "subject_label": SUBJECT_LABELS.get(doc.get("subject") if doc else None, ""),
                "stem": doc.get("content", {}).get("stem") if doc else None,
                "tag": doc.get("tags", {}).get("primary") if doc else None,
            }
        )
    return success(items)


@wrong_book_bp.delete("/<int:item_id>")
@jwt_required()
def master_wrong(item_id):
    user_id = int(get_jwt_identity())
    wq = WrongQuestion.query.filter_by(id=item_id, user_id=user_id).first()
    if not wq:
        return error("NOT_FOUND", "记录不存在", 404)
    wq.is_mastered = True
    db.session.commit()
    return success(None, "已标记为掌握")
