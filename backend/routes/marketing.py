import secrets
import uuid
from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import Course, CourseEnrollment, Order, ReferralLink, TeacherMarketingConfig, User
from utils.response import error, success

marketing_bp = Blueprint("marketing", __name__, url_prefix="/api")
orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@marketing_bp.get("/teachers/<slug>")
def teacher_public_page(slug):
    config = TeacherMarketingConfig.query.filter_by(slug=slug).first()
    if not config:
        return error("NOT_FOUND", "教师不存在", 404)
    teacher = User.query.get(config.teacher_id)
    courses = Course.query.filter_by(
        teacher_id=config.teacher_id, status="published"
    ).all()
    return success(
        {
            "teacher": {
                "id": teacher.id,
                "nickname": teacher.nickname,
                "slug": config.slug,
            },
            "courses": [c.to_dict() for c in courses],
        }
    )


@marketing_bp.get("/referral/resolve/<code>")
def resolve_referral(code):
    link = ReferralLink.query.filter_by(code=code).first()
    if not link:
        return error("NOT_FOUND", "推广码无效", 404)
    link.click_count += 1
    db.session.commit()
    return success(
        {
            "teacher_id": link.teacher_id,
            "course_id": link.course_id,
            "referrer_id": link.referrer_id,
        }
    )


@orders_bp.post("")
@jwt_required()
def create_order():
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json() or {}
    product_type = data.get("product_type", "course")
    product_id = data.get("product_id")
    referrer_id = data.get("referrer_id")

    if product_type == "course":
        course = Course.query.get(product_id)
        if not course:
            return error("NOT_FOUND", "课程不存在", 404)
        amount = course.price
    else:
        return error("NOT_IMPLEMENTED", "该商品类型暂未开放")

    order = Order(
        order_no=uuid.uuid4().hex,
        user_id=user.id,
        product_type=product_type,
        product_id=product_id,
        amount=amount,
        referrer_id=referrer_id,
        payment_method="wechat",
        status="pending",
    )
    db.session.add(order)
    db.session.commit()
    return success({"order_id": order.id, "order_no": order.order_no, "amount": float(amount)})


@orders_bp.post("/<int:order_id>/mock-pay")
@jwt_required()
def mock_pay(order_id):
    """开发环境模拟支付成功"""
    user = User.query.get(int(get_jwt_identity()))
    order = Order.query.filter_by(id=order_id, user_id=user.id).first()
    if not order:
        return error("NOT_FOUND", "订单不存在", 404)
    if order.status == "paid":
        return success(None, "已支付")

    order.status = "paid"
    order.paid_at = datetime.utcnow()

    if order.product_type == "course":
        course = Course.query.get(order.product_id)
        if course:
            course.student_count = (course.student_count or 0) + 1
            exists = CourseEnrollment.query.filter_by(
                user_id=user.id, course_id=course.id
            ).first()
            if not exists:
                db.session.add(
                    CourseEnrollment(
                        user_id=user.id,
                        course_id=course.id,
                        teacher_id=course.teacher_id,
                    )
                )
    db.session.commit()
    return success(None, "支付成功（模拟）")
