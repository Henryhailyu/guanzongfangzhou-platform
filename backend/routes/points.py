from datetime import date, datetime, timedelta

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func

from extensions import db
from models import PointTransaction, User
from services.points_service import PointsService
from services.settings_service import get_int
from utils.response import error, success

points_bp = Blueprint("points", __name__, url_prefix="/api/points")

TYPE_LABELS = {
    "daily_checkin": "每日签到",
    "correct_answer": "答对奖励",
    "wrong_answer": "答错奖励",
    "answer_after_quota": "超额刷题",
    "ai_writing": "AI 写作批改",
    "ai_video_analysis": "AI 视频解析",
    "mock_exam": "模拟考试",
    "purchase_bonus": "购买赠送",
    "referral": "邀请奖励",
}


def _tx_item(t):
    return {
        "id": t.id,
        "amount": t.amount,
        "type": t.type,
        "type_label": TYPE_LABELS.get(t.type, t.type),
        "description": t.description,
        "balance": t.balance,
        "created_at": t.created_at.isoformat(),
    }


@points_bp.get("/rules")
def rules():
    return success(
        {
            "earn": [
                {"key": "daily_checkin", "label": "每日签到", "points": 10, "enabled": True},
                {"key": "correct_answer", "label": "答对一题", "points": 3, "enabled": True},
                {"key": "wrong_answer", "label": "答错一题", "points": 1, "enabled": True},
                {"key": "mock_exam", "label": "完成模拟卷", "points": 50, "enabled": False},
                {"key": "streak_7", "label": "连续登录 7 天", "points": 50, "enabled": False},
                {"key": "referral", "label": "邀请好友注册", "points": 30, "enabled": False},
            ],
            "spend": [
                {
                    "key": "answer_after_quota",
                    "label": "免费额度用尽后继续刷题",
                    "points": get_int("points_per_question_after_quota", 5),
                    "enabled": True,
                },
                {
                    "key": "ai_video_analysis",
                    "label": "AI 视频解析",
                    "points": get_int("ai_video_analysis_points", 10),
                    "enabled": False,
                },
                {
                    "key": "ai_writing",
                    "label": "AI 写作批改",
                    "points": get_int("ai_writing_points", 50),
                    "enabled": False,
                },
                {"key": "mock_paper", "label": "解锁真题模拟卷", "points": 100, "enabled": False},
            ],
            "quota": {
                "free_daily_questions": get_int("free_daily_questions", 20),
                "wrong_penalty": get_int("wrong_quota_penalty", 5),
                "max_wrong_before_quota": get_int("max_wrong_before_quota", 5),
                "description": "免费用户每日可刷题上限；答错累计达 5 道将提前用尽当日免费额度。",
            },
        }
    )


@points_bp.get("/overview")
@jwt_required()
def overview():
    user = User.query.get(int(get_jwt_identity()))
    checked_in = (
        PointTransaction.query.filter(
            PointTransaction.user_id == user.id,
            PointTransaction.type == "daily_checkin",
            func.date(PointTransaction.created_at) == date.today(),
        ).first()
        is not None
    )

    if PointsService.is_vip(user):
        quota_data = {"unlimited": True}
    else:
        quota = PointsService.get_or_create_quota(user.id)
        db.session.commit()
        cfg = current_app.config
        quota_data = {
            "unlimited": False,
            "free_done": quota.free_done,
            "wrong_count": quota.wrong_count,
            "quota_used": quota.quota_used,
            "free_limit": cfg["FREE_DAILY_QUESTIONS"],
            "remaining_free": max(0, cfg["FREE_DAILY_QUESTIONS"] - quota.free_done)
            if not quota.quota_used
            else 0,
        }

    return success(
        {
            "points": user.points,
            "level": user.level,
            "checked_in_today": checked_in,
            "quota": quota_data,
        }
    )


@points_bp.get("/balance")
@jwt_required()
def balance():
    user = User.query.get(int(get_jwt_identity()))
    return success({"points": user.points, "level": user.level})


@points_bp.get("/transactions")
@jwt_required()
def transactions():
    user_id = int(get_jwt_identity())
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 50)
    q = (
        PointTransaction.query.filter_by(user_id=user_id)
        .order_by(PointTransaction.created_at.desc())
        .paginate(page=page, per_page=page_size, error_out=False)
    )
    return success(
        [_tx_item(t) for t in q.items],
        pagination={"page": page, "page_size": page_size, "total": q.total},
    )


@points_bp.post("/checkin")
@jwt_required()
def checkin():
    user = User.query.get(int(get_jwt_identity()))
    existing = PointTransaction.query.filter(
        PointTransaction.user_id == user.id,
        PointTransaction.type == "daily_checkin",
        func.date(PointTransaction.created_at) == date.today(),
    ).first()
    if existing:
        return error("ALREADY_CHECKED_IN", "今日已签到")
    PointsService.add_points(user, 10, "daily_checkin", "每日签到")
    db.session.commit()
    return success({"points": user.points}, "签到成功 +10 积分")


@points_bp.get("/quota/today")
@jwt_required()
def quota_today():
    user = User.query.get(int(get_jwt_identity()))
    if PointsService.is_vip(user):
        return success({"unlimited": True})
    quota = PointsService.get_or_create_quota(user.id)
    db.session.commit()
    cfg = current_app.config
    return success(
        {
            "free_done": quota.free_done,
            "wrong_count": quota.wrong_count,
            "quota_used": quota.quota_used,
            "free_limit": cfg["FREE_DAILY_QUESTIONS"],
            "remaining_free": max(0, cfg["FREE_DAILY_QUESTIONS"] - quota.free_done)
            if not quota.quota_used
            else 0,
        }
    )
