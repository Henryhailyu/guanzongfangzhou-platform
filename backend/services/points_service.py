from datetime import date, datetime, timedelta

from flask import current_app

from extensions import db
from models import DailyQuota, PointTransaction, WrongQuestion
from services.settings_service import get_int


class PointsService:
    @staticmethod
    def add_points(user, amount, tx_type, description):
        user.points += amount
        tx = PointTransaction(
            user_id=user.id,
            amount=amount,
            type=tx_type,
            description=description,
            balance=user.points,
        )
        db.session.add(tx)
        return tx

    @staticmethod
    def deduct_points(user, amount, tx_type, description):
        if user.points < amount:
            return False
        user.points -= amount
        tx = PointTransaction(
            user_id=user.id,
            amount=-amount,
            type=tx_type,
            description=description,
            balance=user.points,
        )
        db.session.add(tx)
        return tx

    @staticmethod
    def is_vip(user):
        return user.vip_expires_at and user.vip_expires_at > datetime.utcnow()

    @staticmethod
    def get_or_create_quota(user_id):
        today = date.today()
        quota = DailyQuota.query.filter_by(user_id=user_id, date=today).first()
        if not quota:
            quota = DailyQuota(user_id=user_id, date=today)
            db.session.add(quota)
            db.session.flush()
        return quota

    @staticmethod
    def process_answer(user, question_id, subject, is_correct, user_answer, time_spent):
        """答题后处理积分与免费额度逻辑"""
        cfg = current_app.config
        points_cost = 0
        points_earned = 0
        max_wrong = get_int("max_wrong_before_quota", cfg.get("MAX_WRONG_BEFORE_QUOTA", 5))
        points_after_quota = get_int("points_per_question_after_quota", cfg.get("POINTS_PER_QUESTION_AFTER_QUOTA", 5))

        if PointsService.is_vip(user):
            if is_correct:
                points_earned = 3
            else:
                points_earned = 1
        else:
            quota = PointsService.get_or_create_quota(user.id)
            quota.free_done += 1

            if quota.quota_used:
                points_cost = points_after_quota
                if user.points < points_cost:
                    return {
                        "ok": False,
                        "code": "INSUFFICIENT_POINTS",
                        "message": f"今日免费额度已用尽，积分不足（每题需 {points_cost} 积分）",
                    }
                PointsService.deduct_points(
                    user, points_cost, "answer_after_quota", "超额刷题消耗"
                )
            elif not is_correct:
                quota.wrong_count += 1
                if quota.wrong_count >= max_wrong:
                    quota.quota_used = True
            if is_correct:
                points_earned = 3
            else:
                points_earned = 1

        if points_earned:
            PointsService.add_points(
                user,
                points_earned,
                "correct_answer" if is_correct else "wrong_answer",
                "答题奖励",
            )

        if not is_correct:
            wq = WrongQuestion.query.filter_by(
                user_id=user.id, question_id=question_id
            ).first()
            if wq:
                wq.wrong_count += 1
                wq.last_wrong_at = datetime.utcnow()
                wq.is_mastered = False
            else:
                db.session.add(
                    WrongQuestion(
                        user_id=user.id,
                        question_id=question_id,
                        next_review_at=datetime.utcnow() + timedelta(days=1),
                    )
                )

        db.session.commit()
        return {
            "ok": True,
            "points_cost": points_cost,
            "points_earned": points_earned,
            "balance": user.points,
        }
