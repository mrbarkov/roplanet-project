from flask import request, jsonify
from flask_restful import Resource
from database import Categories, db


class CategoriesResource(Resource):
    def get(self):
        categories = Categories.query.all()
        category_list = [category.json() for category in categories]
        return jsonify(category_list)

    def post(self):
        data = request.get_json()
        new_category = Categories(
            id=data.get("id"),
            category_name=data.get("name"),
            image=data.get("image")
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created successfully"})


class CategoryResource(Resource):
    def put(self, id):
        data = request.get_json()
        category = Categories.query.get(id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        category.category_name = data.get("name")
        category.image = data.get("image")
        db.session.commit()
        return jsonify({"message": "Category updated successfully"})

    def delete(self, id):
        category = Categories.query.get(id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"})
