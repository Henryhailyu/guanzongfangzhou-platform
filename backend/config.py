import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/guanlian_questions")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASS = os.getenv("REDIS_PASS") or None

    # 平台默认参数
    FREE_DAILY_QUESTIONS = 20
    WRONG_QUOTA_PENALTY = 5
    MAX_WRONG_BEFORE_QUOTA = 5
    POINTS_PER_QUESTION_AFTER_QUOTA = 5
    REFERRAL_COMMISSION_DEFAULT = 0.10
    REFERRAL_COMMISSION_MAX = 0.20
