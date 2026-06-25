from datetime import datetime

from extensions import db
from models import Course, CourseEnrollment, Order, ReferralLink, User
from services.points_service import PointsService

POINTS_PACKS = {
    1: {"name": "100 积分", "points": 100, "price": 6},
    2: {"name": "600 积分", "points": 600, "price": 30},
    3: {"name": "2000 积分", "points": 2000, "price": 88},
}

STATUS_LABELS = {
    "pending": "待支付",
    "paid": "已支付",
    "refunded": "已退款",
    "cancelled": "已取消",
}

PRODUCT_LABELS = {
    "course": "课程",
    "points_pack": "积分包",
    "live_class": "直播课",
    "vip": "VIP",
    "question_analysis": "题目解析",
}

PAYMENT_LABELS = {
    "wechat": "微信支付",
    "alipay": "支付宝",
    "points": "积分支付",
}


def resolve_referral(referral_code=None, referral_link_id=None, buyer_id=None):
    link = None
    if referral_link_id:
        link = ReferralLink.query.get(referral_link_id)
    elif referral_code:
        link = ReferralLink.query.filter_by(code=referral_code).first()
    if not link:
        return None, None
    if buyer_id and link.referrer_id == buyer_id:
        return None, None
    return link.referrer_id, link.id


def get_product_info(product_type, product_id):
    if product_type == "course":
        course = Course.query.get(product_id)
        if not course or course.status != "published":
            return None
        return {
            "title": course.title,
            "amount": float(course.price or 0),
            "teacher_id": course.teacher_id,
            "points_granted": max(1, int(float(course.price or 0) // 10)),
        }
    if product_type == "points_pack":
        pack = POINTS_PACKS.get(int(product_id))
        if not pack:
            return None
        return {
            "title": pack["name"],
            "amount": pack["price"],
            "teacher_id": None,
            "points_granted": pack["points"],
        }
    return None


def order_to_dict(order, include_user=False):
    product = get_product_info(order.product_type, order.product_id)
    data = {
        "id": order.id,
        "order_no": order.order_no,
        "user_id": order.user_id,
        "product_type": order.product_type,
        "product_type_label": PRODUCT_LABELS.get(order.product_type, order.product_type),
        "product_id": order.product_id,
        "product_title": product["title"] if product else None,
        "amount": float(order.amount or 0),
        "points_granted": order.points_granted or 0,
        "payment_method": order.payment_method,
        "payment_method_label": PAYMENT_LABELS.get(order.payment_method, order.payment_method),
        "status": order.status,
        "status_label": STATUS_LABELS.get(order.status, order.status),
        "referrer_id": order.referrer_id,
        "referral_link_id": order.referral_link_id,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }
    if include_user:
        user = User.query.get(order.user_id)
        data["user_nickname"] = user.nickname if user else None
    if order.product_type == "course" and product:
        data["teacher_id"] = product.get("teacher_id")
        teacher = User.query.get(product["teacher_id"]) if product.get("teacher_id") else None
        data["teacher_name"] = teacher.nickname if teacher else None
    return data


def fulfill_order(order):
    user = User.query.get(order.user_id)
    if not user:
        return False

    if order.product_type == "course":
        course = Course.query.get(order.product_id)
        if not course:
            return False
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
            course.student_count = (course.student_count or 0) + 1

    if order.points_granted and order.points_granted > 0:
        PointsService.add_points(
            user,
            order.points_granted,
            "purchase_bonus",
            f"订单 {order.order_no} 获赠积分",
        )

    return True


def complete_payment(order, payment_method=None):
    if order.status == "paid":
        return order
    if order.status != "pending":
        return None

    if payment_method:
        order.payment_method = payment_method
    order.status = "paid"
    order.paid_at = datetime.utcnow()
    fulfill_order(order)
    if order.referral_link_id:
        link = ReferralLink.query.get(order.referral_link_id)
        if link:
            link.convert_count = (link.convert_count or 0) + 1
    db.session.commit()
    return order
