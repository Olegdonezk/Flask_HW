from flask import Blueprint, request
from app.models import Question
from app.extensions import db

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()

    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "text": q.text,
            "category": {
                "id": q.category.id,
                "name": q.category.name
            } if q.category else None
        })

    return {"questions": result}


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.json

    question = Question(
        text=data["text"],
        category_id=data["category_id"]
    )

    db.session.add(question)
    db.session.commit()

    return {
        "id": question.id,
        "text": question.text,
        "category_id": question.category_id
    }, 201