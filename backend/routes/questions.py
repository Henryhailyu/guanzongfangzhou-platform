from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import User
from services.points_service import PointsService
from utils.response import error, success

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


def get_mongo():
    return current_app.mongo_db


def _serialize(item, hide_answer=False):
    item["_id"] = str(item["_id"])
    if hide_answer and "content" in item:
        content = dict(item["content"])
        content.pop("correct_answer", None)
        content.pop("answer_analysis", None)
        item = dict(item)
        item["content"] = content
    return item


@questions_bp.get("/tags")
def list_tags():
    subject = request.args.get("subject")
    query = {"subject": subject} if subject else {}
    tags = get_mongo().questions.distinct("tags.primary", query)
    return success(sorted(t for t in tags if t))


@questions_bp.get("/practice")
def practice_set():
    subject = request.args.get("subject", "math")
    mode = request.args.get("mode", "random")
    tag = request.args.get("tag")
    count = min(int(request.args.get("count", 10)), 30)

    query = {"subject": subject}
    if mode == "specialized" and tag:
        query["tags.primary"] = tag

    col = get_mongo().questions
    total = col.count_documents(query)
    if total == 0:
        return success([])

    pipeline = [{"$match": query}, {"$sample": {"size": min(count, total)}}]
    items = [_serialize(doc, hide_answer=True) for doc in col.aggregate(pipeline)]
    return success(
        {
            "items": items,
            "mode": mode,
            "subject": subject,
            "tag": tag,
            "total": total,
        }
    )


@questions_bp.get("")
def list_questions():
    subject = request.args.get("subject")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    query = {}
    if subject:
        query["subject"] = subject

    col = get_mongo().questions
    total = col.count_documents(query)
    items = [
        _serialize(doc, hide_answer=True)
        for doc in col.find(query).skip((page - 1) * page_size).limit(page_size)
    ]

    return success(
        items,
        pagination={"page": page, "page_size": page_size, "total": total},
    )


@questions_bp.get("/<question_id>/similar")
def similar_questions(question_id):
    doc = get_mongo().questions.find_one({"question_id": question_id})
    if not doc:
        return error("NOT_FOUND", "题目不存在", 404)

    primary = doc.get("tags", {}).get("primary")
    limit = min(int(request.args.get("limit", 3)), 10)
    query = {
        "subject": doc.get("subject"),
        "question_id": {"$ne": question_id},
    }
    if primary:
        query["tags.primary"] = primary

    items = [
        _serialize(d, hide_answer=True)
        for d in get_mongo().questions.find(query).limit(limit)
    ]
    if len(items) < limit:
        extra = [
            _serialize(d, hide_answer=True)
            for d in get_mongo().questions.find(
                {"subject": doc.get("subject"), "question_id": {"$ne": question_id}}
            ).limit(limit - len(items))
        ]
        seen = {i["question_id"] for i in items}
        items.extend(x for x in extra if x["question_id"] not in seen)

    return success(items[:limit])


@questions_bp.get("/<question_id>")
def get_question(question_id):
    doc = get_mongo().questions.find_one({"question_id": question_id})
    if not doc:
        return error("NOT_FOUND", "题目不存在", 404)
    return success(_serialize(doc))


@questions_bp.post("/<question_id>/submit")
@jwt_required()
def submit_answer(question_id):
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json() or {}
    user_answer = data.get("answer", "").strip().upper()
    time_spent = data.get("time_spent", 0)

    doc = get_mongo().questions.find_one({"question_id": question_id})
    if not doc:
        return error("NOT_FOUND", "题目不存在", 404)

    correct = doc["content"]["correct_answer"].upper()
    is_correct = user_answer == correct

    result = PointsService.process_answer(
        user, question_id, doc.get("subject"), is_correct, user_answer, time_spent
    )
    if not result["ok"]:
        return error(result["code"], result["message"], 402)

    from models import AnswerRecord

    db.session.add(
        AnswerRecord(
            user_id=user.id,
            question_id=question_id,
            subject=doc.get("subject"),
            is_correct=is_correct,
            user_answer=user_answer,
            time_spent=time_spent,
            points_cost=result["points_cost"],
        )
    )
    db.session.commit()

    stats = doc.get("stats") or {}
    attempts = stats.get("total_attempts", 0) + 1
    prev_correct = stats.get("correct_rate", 0) * stats.get("total_attempts", 0)
    new_rate = (prev_correct + (1 if is_correct else 0)) / attempts
    get_mongo().questions.update_one(
        {"question_id": question_id},
        {
            "$set": {
                "stats.total_attempts": attempts,
                "stats.correct_rate": round(new_rate, 4),
            }
        },
    )

    similar = list(
        get_mongo().questions.find(
            {
                "subject": doc.get("subject"),
                "question_id": {"$ne": question_id},
                "tags.primary": doc.get("tags", {}).get("primary"),
            },
            {"content.options": 0},
        ).limit(2)
    )
    for s in similar:
        s["_id"] = str(s["_id"])

    return success(
        {
            "is_correct": is_correct,
            "correct_answer": correct,
            "analysis": doc["content"].get("answer_analysis", {}).get("text"),
            "points_earned": result["points_earned"],
            "points_cost": result["points_cost"],
            "balance": result["balance"],
            "similar_questions": similar,
        }
    )
