import json

from flask import request, jsonify
from flask_restful import Resource
from database import db, Review


class CreateReview(Resource):
    def post(self):
        data = request.get_json()

        review_obj = Review(
            review_description=data["reviewDescription"],
            review_image=data["reviewImage"]
        )
        db.session.add(review_obj)
        db.session.commit()
        jsonify(review_obj.as_dict())

class ReviewGetList(Resource):
    def get(self):
        data = request.get_json()
        query = Review.query.all()
        products_data = [product.as_dict() for product in query]
        return jsonify(products_data)

class ReviewIdMod(Resource):
    def put(self, id):
        data = request.get_json()
        review_get = Review.query.get(id)
        if not review_get:
            return jsonify({"message": "Review not found"}), 404
        review_get.review_description = data["reviewDescription"]
        review_get.review_image = data["reviewImage"]
        db.session.commit()
        return jsonify(review_get.as_dict())
        # return jsonify({"message": "Category updated successfully"})

    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return jsonify({"message": "Review not found"}), 404
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "review deleted successfully"})
