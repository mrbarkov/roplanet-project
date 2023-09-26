import flask
from flask import request, session, send_file, jsonify
from flask_restful import Api, Resource

from categories.categories import CategoriesResource, CategoryResource
from Products.product import ProductGet, GetProductById, ProductCreate, ProductChange
from reviews.reviews import ReviewIdMod, Review, CreateReview, ReviewGetList
from database import Categories, db
from __init__ import app, api


@app.before_request
def create_table():
    """Create table"""
    db.create_all()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api.add_resource(CategoriesResource, "/api/categories")
api.add_resource(CategoryResource, "/api/categories/<string:id>")

api.add_resource(ProductGet, "/api/product/list")
api.add_resource(GetProductById, "/api/product/<int:id>")
api.add_resource(ProductCreate, "/api/product")
api.add_resource(ProductChange, "/api/product/<int:id>")

api.add_resource(ReviewGetList, "/api/review/list")
api.add_resource(CreateReview, "/api/review")
api.add_resource(ReviewIdMod, "/api/review/<int:id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)