from flask import Blueprint, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func, case

from extensions import db
from models import AnswerRecord, WrongQuestion
from utils.response import success

learning_bp = Blueprint("learning", __name__, url_prefix="/api/learning")

SUBJECT_LABELS = {
    "math": "数学基础",
    "logic": "逻辑推理",
    "writing": "写作",
    "english": "英语二",
}


def _subject_from_mongo(question_id):
    doc = current_app.mongo_db.questions.find_one(
        {"question_id": question_id}, {"subject": 1}
    )
    return doc.get("subject") if doc else "unknown"


@learning_bp.get("/progress")
@jwt_required()
def progress():
    user_id = int(get_jwt_identity())

    rows = (
        db.session.query(
            AnswerRecord.subject,
            func.count(AnswerRecord.id).label("total"),
            func.sum(case((AnswerRecord.is_correct, 1), else_=0)).label("correct"),
        )
        .filter(AnswerRecord.user_id == user_id)
        .group_by(AnswerRecord.subject)
        .all()
    )

    wrong_by_subject = {}
    for w in WrongQuestion.query.filter_by(user_id=user_id, is_mastered=False).all():
        subj = _subject_from_mongo(w.question_id)
        wrong_by_subject[subj] = wrong_by_subject.get(subj, 0) + 1

    subjects = []
    seen = set()
    for row in rows:
        subj = row.subject or "unknown"
        seen.add(subj)
        total = int(row.total or 0)
        correct = int(row.correct or 0)
        subjects.append(
            {
                "subject": subj,
                "label": SUBJECT_LABELS.get(subj, subj),
                "total_answered": total,
                "correct_count": correct,
                "accuracy": round(correct / total * 100, 1) if total else 0,
                "wrong_count": wrong_by_subject.get(subj, 0),
            }
        )

    for subj, count in wrong_by_subject.items():
        if subj not in seen:
            subjects.append(
                {
                    "subject": subj,
                    "label": SUBJECT_LABELS.get(subj, subj),
                    "total_answered": 0,
                    "correct_count": 0,
                    "accuracy": 0,
                    "wrong_count": count,
                }
            )

    total_answered = sum(s["total_answered"] for s in subjects)
    total_correct = sum(s["correct_count"] for s in subjects)
    total_wrong = WrongQuestion.query.filter_by(user_id=user_id, is_mastered=False).count()

    return success(
        {
            "subjects": subjects,
            "summary": {
                "total_answered": total_answered,
                "total_correct": total_correct,
                "accuracy": round(total_correct / total_answered * 100, 1) if total_answered else 0,
                "wrong_book_count": total_wrong,
            },
        }
    )
