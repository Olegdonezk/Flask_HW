from flask import Blueprint

responses_bp = Blueprint('responses', __name__)

@responses_bp.route('/', methods=['GET'])
def get_responses():
    return {"message": "ok"}