import uuid
from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import Course, CourseEnrollment, Order, ReferralLink, TeacherMarketingConfig, TeacherProfile, User
from services.order_service import (
    POINTS_PACKS,
    complete_payment,
    get_product_info,
    order_to_dict,
    resolve_referral,
)
from utils.response import error, success

marketing_bp = Blueprint("marketing", __name__, url_prefix="/api")
orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")
webhooks_bp = Blueprint("webhooks", __name__, url_prefix="/api/webhooks")


SUBJECT_LABELS = {
    "math": "数学",
    "logic": "逻辑",
    "writing": "写作",
    "english": "英语二",
    "combo": "综合",
}


@marketing_bp.get("/teachers/<slug>")
def teacher_public_page(slug):
    config = TeacherMarketingConfig.query.filter_by(slug=slug).first()
    if not config:
        return error("NOT_FOUND", "教师不存在", 404)
    teacher = User.query.get(config.teacher_id)
    profile = TeacherProfile.query.filter_by(user_id=config.teacher_id).first()
    if not teacher or not profile or profile.status != "approved":
        return error("NOT_FOUND", "教师不存在", 404)

    courses = Course.query.filter_by(
        teacher_id=config.teacher_id, status="published"
    ).all()
    return success(
        {
            "teacher": {
                "id": teacher.id,
                "nickname": teacher.nickname,
                "real_name": profile.real_name,
                "bio": profile.bio,
                "expertise": profile.expertise,
                "slug": config.slug,
            },
            "stats": {
                "course_count": len(courses),
                "student_count": sum(c.student_count or 0 for c in courses),
            },
            "courses": [c.to_dict() for c in courses],
        }
    )


@marketing_bp.get("/referral/resolve/<code>")
def resolve_referral_code(code):
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
            "referral_link_id": link.id,
        }
    )


@orders_bp.get("/points-packs")
def list_points_packs():
    items = [
        {"id": pid, **pack}
        for pid, pack in POINTS_PACKS.items()
    ]
    return success(items)


@orders_bp.get("")
@jwt_required()
def list_my_orders():
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    q = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc())
    if status:
        q = q.filter_by(status=status)
    return success([order_to_dict(o) for o in q.limit(50).all()])


@orders_bp.get("/<int:order_id>")
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    order = Order.query.get(order_id)
    if not order:
        return error("NOT_FOUND", "订单不存在", 404)
    if order.user_id != user_id and user.role != "admin":
        return error("FORBIDDEN", "无权查看", 403)
    return success(order_to_dict(order))


@orders_bp.post("")
@jwt_required()
def create_order():
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json() or {}
    product_type = data.get("product_type", "course")
    product_id = data.get("product_id")
    payment_method = data.get("payment_method", "wechat")
    referral_code = data.get("referral_code")
    referral_link_id = data.get("referral_link_id")

    if payment_method not in ("wechat", "alipay"):
        return error("INVALID_INPUT", "暂仅支持微信或支付宝", 400)

    product = get_product_info(product_type, product_id)
    if not product:
        return error("NOT_FOUND", "商品不存在", 404)

    if product_type == "course":
        enrolled = CourseEnrollment.query.filter_by(
            user_id=user.id, course_id=product_id
        ).first()
        if enrolled:
            return error("ALREADY_PURCHASED", "您已购买该课程", 400)
        pending = Order.query.filter_by(
            user_id=user.id,
            product_type="course",
            product_id=product_id,
            status="pending",
        ).first()
        if pending:
            return success(order_to_dict(pending), "已有待支付订单")

    referrer_id, link_id = resolve_referral(
        referral_code, referral_link_id, buyer_id=user.id
    )

    order = Order(
        order_no=uuid.uuid4().hex,
        user_id=user.id,
        product_type=product_type,
        product_id=product_id,
        amount=product["amount"],
        points_granted=product["points_granted"],
        referrer_id=referrer_id,
        referral_link_id=link_id,
        payment_method=payment_method,
        status="pending",
    )
    db.session.add(order)
    db.session.commit()
    return success(order_to_dict(order))


@orders_bp.post("/<int:order_id>/pay")
@jwt_required()
def pay_order(order_id):
    """开发环境模拟支付；生产环境由微信/支付宝回调完成"""
    user = User.query.get(int(get_jwt_identity()))
    order = Order.query.filter_by(id=order_id, user_id=user.id).first()
    if not order:
        return error("NOT_FOUND", "订单不存在", 404)
    if order.status == "paid":
        return success(order_to_dict(order), "已支付")
    if order.status != "pending":
        return error("INVALID_STATE", "订单状态不可支付", 400)

    data = request.get_json() or {}
    payment_method = data.get("payment_method") or order.payment_method or "wechat"
    if payment_method not in ("wechat", "alipay"):
        return error("INVALID_INPUT", "支付方式无效", 400)

    result = complete_payment(order, payment_method)
    if not result:
        return error("INVALID_STATE", "支付失败", 400)
    return success(order_to_dict(result), "支付成功（模拟）")


@orders_bp.post("/<int:order_id>/mock-pay")
@jwt_required()
def mock_pay(order_id):
    """兼容旧接口"""
    return pay_order(order_id)


@orders_bp.post("/<int:order_id>/cancel")
@jwt_required()
def cancel_order(order_id):
    user = User.query.get(int(get_jwt_identity()))
    order = Order.query.filter_by(id=order_id, user_id=user.id).first()
    if not order:
        return error("NOT_FOUND", "订单不存在", 404)
    if order.status != "pending":
        return error("INVALID_STATE", "仅待支付订单可取消", 400)
    order.status = "cancelled"
    db.session.commit()
    return success(order_to_dict(order), "订单已取消")


@webhooks_bp.post("/wechat-pay")
def wechat_pay_webhook():
    """微信支付回调占位，生产环境需验签后调用 complete_payment"""
    return error("NOT_IMPLEMENTED", "微信支付回调待接入", 501)
