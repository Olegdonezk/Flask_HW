from flask import Blueprint, request

categories_bp = Blueprint('categories', __name__)

# временная "память"
categories = []


@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    category = {
        "id": len(categories) + 1,
        "name": data["name"]
    }
    categories.append(category)
    return category, 201


@categories_bp.route('/', methods=['GET'])
def get_categories():
    return categories


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    for c in categories:
        if c["id"] == id:
            c["name"] = data["name"]
            return c
    return {"error": "not found"}, 404


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    global categories
    categories = [c for c in categories if c["id"] != id]
    return {"message": "deleted"}