"""数据库与 MongoDB 种子数据"""
from werkzeug.security import generate_password_hash

from extensions import db
from models import Course, Lesson, TeacherMarketingConfig, TeacherProfile, User

SAMPLE_QUESTIONS = [
    {
        "question_id": "MATH_001_001",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 2,
        "tags": {"primary": "代数", "secondary": "方程", "tertiary": "一元一次方程"},
        "content": {
            "stem": "若 2x + 3 = 11，则 x = ?",
            "options": ["A. 2", "B. 3", "C. 4", "D. 5", "E. 6"],
            "correct_answer": "C",
            "answer_analysis": {"text": "2x = 8，x = 4。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_002",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 3,
        "tags": {"primary": "几何", "secondary": "平面几何"},
        "content": {
            "stem": "直角三角形两直角边分别为3和4，则斜边长为？",
            "options": ["A. 5", "B. 6", "C. 7", "D. 8", "E. 9"],
            "correct_answer": "A",
            "answer_analysis": {"text": "勾股定理：斜边 = √(9+16) = 5。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_003",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 2,
        "tags": {"primary": "代数", "secondary": "不等式"},
        "content": {
            "stem": "若 x - 5 > 0，则 x 的取值范围是？",
            "options": ["A. x > 5", "B. x < 5", "C. x ≥ 5", "D. x ≤ 5", "E. x = 5"],
            "correct_answer": "A",
            "answer_analysis": {"text": "移项得 x > 5。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_004",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 3,
        "tags": {"primary": "代数", "secondary": "二次方程"},
        "content": {
            "stem": "方程 x² - 5x + 6 = 0 的两根之和为？",
            "options": ["A. 5", "B. 6", "C. -5", "D. -6", "E. 1"],
            "correct_answer": "A",
            "answer_analysis": {"text": "韦达定理：两根之和 = 5。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_005",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 2,
        "tags": {"primary": "几何", "secondary": "圆"},
        "content": {
            "stem": "半径为 3 的圆，其面积为？（π 取 3.14 近似，选最接近值）",
            "options": ["A. 9.42", "B. 18.84", "C. 28.26", "D. 37.68", "E. 6.28"],
            "correct_answer": "C",
            "answer_analysis": {"text": "S = πr² = 3.14 × 9 ≈ 28.26。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_006",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 3,
        "tags": {"primary": "应用题", "secondary": "行程问题"},
        "content": {
            "stem": "甲、乙两地相距 120 km，汽车以 60 km/h 行驶，需几小时到达？",
            "options": ["A. 1", "B. 1.5", "C. 2", "D. 2.5", "E. 3"],
            "correct_answer": "C",
            "answer_analysis": {"text": "t = s/v = 120/60 = 2 小时。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_007",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 2,
        "tags": {"primary": "代数", "secondary": "比例"},
        "content": {
            "stem": "若 a:b = 2:3 且 a = 8，则 b = ?",
            "options": ["A. 6", "B. 10", "C. 12", "D. 14", "E. 16"],
            "correct_answer": "C",
            "answer_analysis": {"text": "8/b = 2/3，b = 12。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "MATH_001_008",
        "subject": "math",
        "question_type": "problem_solving",
        "difficulty": 4,
        "tags": {"primary": "几何", "secondary": "立体几何"},
        "content": {
            "stem": "棱长为 2 的正方体，体积为？",
            "options": ["A. 4", "B. 6", "C. 8", "D. 10", "E. 12"],
            "correct_answer": "C",
            "answer_analysis": {"text": "V = a³ = 8。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "LOGIC_001_001",
        "subject": "logic",
        "question_type": "single_choice",
        "difficulty": 2,
        "tags": {"primary": "形式逻辑", "secondary": "假言命题"},
        "content": {
            "stem": "所有A都是B。有些B是C。以下哪项一定为真？",
            "options": [
                "A. 所有A都是C",
                "B. 有些A是C",
                "C. 有些C是B",
                "D. 所有C都是A",
                "E. 以上都不一定为真",
            ],
            "correct_answer": "C",
            "answer_analysis": {"text": "由'有些B是C'可推出'有些C是B'。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "LOGIC_001_002",
        "subject": "logic",
        "question_type": "single_choice",
        "difficulty": 2,
        "tags": {"primary": "论证推理", "secondary": "加强削弱"},
        "content": {
            "stem": "某调查显示，经常运动的人更健康。以下哪项最能加强上述结论？",
            "options": [
                "A. 健康的人更喜欢运动",
                "B. 运动能提升免疫力",
                "C. 有些人不运动也很健康",
                "D. 运动需要花费时间",
                "E. 健康与饮食也有关",
            ],
            "correct_answer": "B",
            "answer_analysis": {"text": "B 提供了运动→健康的因果机制，属于加强。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "LOGIC_001_003",
        "subject": "logic",
        "question_type": "single_choice",
        "difficulty": 3,
        "tags": {"primary": "形式逻辑", "secondary": "联言选言"},
        "content": {
            "stem": "并非（p 且 q）等价于？",
            "options": [
                "A. 非 p 且 非 q",
                "B. 非 p 或 非 q",
                "C. p 或 q",
                "D. 非 p 或 q",
                "E. p 且 非 q",
            ],
            "correct_answer": "B",
            "answer_analysis": {"text": "德摩根律：¬(p∧q) ≡ ¬p∨¬q。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
    {
        "question_id": "LOGIC_001_004",
        "subject": "logic",
        "question_type": "single_choice",
        "difficulty": 3,
        "tags": {"primary": "综合推理", "secondary": "排序"},
        "content": {
            "stem": "甲、乙、丙三人排队，甲不在最前，乙在丙前面。以下哪项可能正确？",
            "options": [
                "A. 甲乙丙",
                "B. 丙甲乙",
                "C. 乙丙甲",
                "D. 丙乙甲",
                "E. 甲丙乙",
            ],
            "correct_answer": "C",
            "answer_analysis": {"text": "乙在丙前且甲不在最前，乙丙甲满足条件。"},
        },
        "ai_generated": False,
        "stats": {"total_attempts": 0, "correct_rate": 0, "avg_time_seconds": 0},
    },
]


def run_seed(app):
    with app.app_context():
        if not User.query.filter_by(email="admin@guanlian.com").first():
            admin = User(
                email="admin@guanlian.com",
                nickname="平台管理员",
                password_hash=generate_password_hash("admin123"),
                role="admin",
                points=9999,
            )
            db.session.add(admin)

        if not User.query.filter_by(email="teacher@guanlian.com").first():
            teacher = User(
                email="teacher@guanlian.com",
                nickname="张老师",
                password_hash=generate_password_hash("teacher123"),
                role="teacher",
                points=100,
            )
            db.session.add(teacher)
            db.session.flush()
            db.session.add(
                TeacherProfile(
                    user_id=teacher.id,
                    real_name="张老师",
                    bio="管理类联考数学名师，10年教学经验",
                    expertise="数学",
                    status="approved",
                )
            )
            db.session.add(
                TeacherMarketingConfig(teacher_id=teacher.id, slug="zhang-math")
            )
            course = Course(
                title="管理类联考数学基础精讲",
                subject="math",
                description="系统讲解管理类联考数学核心考点",
                teacher_id=teacher.id,
                price=199,
                original_price=399,
                status="published",
                total_lessons=2,
            )
            db.session.add(course)
            db.session.flush()
            db.session.add(
                Lesson(course_id=course.id, title="第1讲：代数基础", sort_order=1, is_free=True)
            )
            db.session.add(
                Lesson(course_id=course.id, title="第2讲：几何要点", sort_order=2)
            )

        if not User.query.filter_by(email="student@guanlian.com").first():
            db.session.add(
                User(
                    email="student@guanlian.com",
                    nickname="备考学员",
                    password_hash=generate_password_hash("student123"),
                    role="student",
                    points=100,
                )
            )

        db.session.commit()

        from services.settings_service import ensure_defaults
        ensure_defaults()

        col = app.mongo_db.questions
        inserted = 0
        for q in SAMPLE_QUESTIONS:
            if not col.find_one({"question_id": q["question_id"]}):
                col.insert_one(q)
                inserted += 1
        if inserted:
            print(f"MongoDB: seeded {inserted} questions")

        print("Seed completed")
