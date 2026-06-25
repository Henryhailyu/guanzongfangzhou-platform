from datetime import datetime, date
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(64), unique=True, nullable=True)
    nickname = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum("student", "teacher", "admin"), default="student")
    points = db.Column(db.Integer, default=0)
    level = db.Column(
        db.Enum("入门生", "备考生", "冲刺生", "上岸生"), default="入门生"
    )
    vip_expires_at = db.Column(db.DateTime, nullable=True)
    target_school = db.Column(db.String(100))
    target_major = db.Column(
        db.Enum("MBA", "MPA", "MPAcc", "MEM", "MAud", "MTA", "MLIS"), nullable=True
    )
    exam_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "points": self.points,
            "level": self.level,
            "vip_expires_at": self.vip_expires_at.isoformat() if self.vip_expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TeacherProfile(db.Model):
    __tablename__ = "teacher_profiles"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), unique=True)
    real_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    expertise = db.Column(db.String(200))
    status = db.Column(
        db.Enum("pending", "approved", "rejected", "suspended"), default="pending"
    )
    commission_rate = db.Column(db.Numeric(4, 2), default=0.70)
    approved_by = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id], backref="teacher_profile")


class PointTransaction(db.Model):
    __tablename__ = "point_transactions"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    balance = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailyQuota(db.Model):
    __tablename__ = "daily_quota"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    date = db.Column(db.Date, nullable=False)
    free_done = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0)
    quota_used = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint("user_id", "date", name="uq_user_date"),)


class AnswerRecord(db.Model):
    __tablename__ = "answer_records"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    question_id = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(20))
    is_correct = db.Column(db.Boolean)
    user_answer = db.Column(db.String(10))
    time_spent = db.Column(db.Integer)
    points_cost = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WrongQuestion(db.Model):
    __tablename__ = "wrong_questions"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    question_id = db.Column(db.String(50), nullable=False)
    wrong_count = db.Column(db.Integer, default=1)
    last_wrong_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_at = db.Column(db.DateTime, nullable=True)
    is_mastered = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint("user_id", "question_id", name="uq_user_question"),)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.Enum("math", "logic", "writing", "english", "combo"))
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    price = db.Column(db.Numeric(10, 2), default=0)
    original_price = db.Column(db.Numeric(10, 2))
    is_free = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum("draft", "published", "archived"), default="draft")
    total_lessons = db.Column(db.Integer, default=0)
    student_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship("User", foreign_keys=[teacher_id])
    lessons = db.relationship("Lesson", backref="course", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "description": self.description,
            "cover_url": self.cover_url,
            "teacher_id": self.teacher_id,
            "teacher_name": self.teacher.nickname if self.teacher else None,
            "price": float(self.price or 0),
            "original_price": float(self.original_price) if self.original_price else None,
            "is_free": self.is_free,
            "status": self.status,
            "total_lessons": self.total_lessons,
            "student_count": self.student_count,
        }


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    course_id = db.Column(db.BigInteger, db.ForeignKey("courses.id"))
    title = db.Column(db.String(200))
    vod_file_id = db.Column(db.String(200))
    duration_sec = db.Column(db.Integer)
    sort_order = db.Column(db.Integer, default=0)
    is_free = db.Column(db.Boolean, default=False)
    preview_sec = db.Column(db.Integer, default=300)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "vod_file_id": self.vod_file_id,
            "duration_sec": self.duration_sec,
            "sort_order": self.sort_order,
            "is_free": self.is_free,
            "preview_sec": self.preview_sec,
        }


class CourseEnrollment(db.Model):
    __tablename__ = "course_enrollments"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    course_id = db.Column(db.BigInteger, db.ForeignKey("courses.id"))
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_pct = db.Column(db.Numeric(5, 2), default=0)
    last_active_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint("user_id", "course_id", name="uq_user_course"),)

    user = db.relationship("User", foreign_keys=[user_id])
    course = db.relationship("Course", foreign_keys=[course_id])


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    product_type = db.Column(
        db.Enum("course", "live_class", "points_pack", "vip", "question_analysis")
    )
    product_id = db.Column(db.BigInteger)
    amount = db.Column(db.Numeric(10, 2))
    points_granted = db.Column(db.Integer, default=0)
    referrer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    referral_link_id = db.Column(db.BigInteger, nullable=True)
    payment_method = db.Column(db.Enum("wechat", "alipay", "points"), nullable=True)
    status = db.Column(
        db.Enum("pending", "paid", "refunded", "cancelled"), default="pending"
    )
    paid_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TeacherMarketingConfig(db.Model):
    __tablename__ = "teacher_marketing_configs"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), unique=True)
    slug = db.Column(db.String(50), unique=True)
    student_referral_enabled = db.Column(db.Boolean, default=False)
    referral_reward_type = db.Column(
        db.Enum("cash", "points", "coupon", "mixed"), default="points"
    )
    referral_commission_rate = db.Column(db.Numeric(4, 2), default=0.10)
    referral_points = db.Column(db.Integer, default=200)
    max_commission_rate = db.Column(db.Numeric(4, 2), default=0.20)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ReferralLink(db.Model):
    __tablename__ = "referral_links"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    course_id = db.Column(db.BigInteger, db.ForeignKey("courses.id"), nullable=True)
    referrer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    referrer_type = db.Column(
        db.Enum("teacher", "student", "platform"), default="teacher"
    )
    code = db.Column(db.String(32), unique=True)
    channel = db.Column(db.String(50))
    click_count = db.Column(db.Integer, default=0)
    convert_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
