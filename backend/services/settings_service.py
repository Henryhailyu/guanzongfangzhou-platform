from extensions import db
from models import SystemSetting

DEFAULTS = {
    "free_daily_questions": "20",
    "wrong_quota_penalty": "5",
    "max_wrong_before_quota": "5",
    "points_per_question_after_quota": "5",
    "ai_writing_points": "50",
    "ai_video_analysis_points": "10",
    "max_commission_rate": "0.20",
    "default_referral_commission_rate": "0.10",
    "withdraw_min_amount": "50",
}


def ensure_defaults():
    changed = False
    for key, value in DEFAULTS.items():
        if not SystemSetting.query.get(key):
            db.session.add(SystemSetting(key=key, value=value))
            changed = True
    if changed:
        db.session.commit()


def _get_raw():
    ensure_defaults()
    return {s.key: s.value for s in SystemSetting.query.all()}


def get_int(key, fallback=0):
    raw = _get_raw()
    try:
        return int(raw.get(key, fallback))
    except (TypeError, ValueError):
        return fallback


def get_float(key, fallback=0.0):
    raw = _get_raw()
    try:
        return float(raw.get(key, fallback))
    except (TypeError, ValueError):
        return fallback


def set_values(updates: dict):
    ensure_defaults()
    for key, value in updates.items():
        if key not in DEFAULTS:
            continue
        row = SystemSetting.query.get(key)
        if row:
            row.value = str(value)
        else:
            db.session.add(SystemSetting(key=key, value=str(value)))
    db.session.commit()


def as_response():
    raw = _get_raw()
    return {
        "quota": {
            "free_daily_questions": int(raw["free_daily_questions"]),
            "wrong_quota_penalty": int(raw["wrong_quota_penalty"]),
            "max_wrong_before_quota": int(raw["max_wrong_before_quota"]),
            "points_per_question_after_quota": int(raw["points_per_question_after_quota"]),
        },
        "ai": {
            "writing_points": int(raw["ai_writing_points"]),
            "video_analysis_points": int(raw["ai_video_analysis_points"]),
        },
        "referral": {
            "default_commission_rate": float(raw["default_referral_commission_rate"]),
            "max_commission_rate": float(raw["max_commission_rate"]),
            "withdraw_min_amount": float(raw["withdraw_min_amount"]),
        },
    }
