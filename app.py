import os
from datetime import datetime
import flask
from flask import request, session, send_file, jsonify
from flask import request
from flask_restful import Resource
from user.User import UserRegistration, UserSmsConfirm, UserLogin, RefreshToken
from __init__ import allowed_file
from categories.categories import CategoriesResource, CategoryResource
from Products.product import ProductGet, GetProductById, ProductCreate, ProductChange
from reviews.reviews import ReviewIdMod, Review, CreateReview, ReviewGetList
from database import db
from __init__ import app, api


@app.before_request
def create_table():
    """Create table"""
    db.create_all()


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class ImageGet(Resource):
    """Class get image on server"""

    def get(self, filename):
        """Request from get image"""
        path = f'uploads/{filename}'
        return send_file(path, as_attachment=True)


class ImageUpload(Resource):
    def post(self):
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = f"{str(datetime.now()).replace(' ', '_')}.png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename




api.add_resource(UserRegistration, "/api/user/registration")
api.add_resource(UserLogin, "/api/user/login")
api.add_resource(RefreshToken, "/token/refresh")
api.add_resource(UserSmsConfirm, "/api/user/code")
api.add_resource(ImageUpload, "/api/image/load")
api.add_resource(ImageGet, "/api/image/<string:filename>")

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
