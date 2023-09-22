import json

from flask import request, jsonify
from flask_restful import Resource
from database import db, Product


class ProductGet(Resource):
    def get(self):
        data = request.get_json()
        category_id = data.get('categoryId')
        query = Product.query.filter_by(category_id=category_id)
        products_data = [product.as_dict() for product in query]
        return jsonify(products_data)


class GetProductById(Resource):
    def get(self, id):
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        response = product.json()

        if product.sale_price is not None:
            response["salePrice"] = product.sale_price

        return jsonify(response)


class ProductCreate(Resource):
    def post(self):
        data = request.get_json()

        new_product = Product(
            category_id=data.get("categoryId"),
            product_sizes=json.dumps(data.get("productSizes")),  # Сериализуем список в JSON
            product_colors=json.dumps(data.get("productColors")),  # Сериализуем список в JSON
            product_articul=data.get("productArticul"),
            product_type=data.get("productType"),
            product_name=data.get("productName"),
            product_about=data.get("productAbout"),
            product_descriptions=data.get("productDescriptions"),
            product_price=data.get("productPrice"),
            product_size_description=data.get("productSizeDescription"),
            product_images=json.dumps(data.get("productImages")),  # Сериализуем список в JSON
            sale_price=data.get("salePrice")
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify(new_product.as_dict())


class ProductChange(Resource):
    def put(self, id):
        data = request.get_json()
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "product not found"}), 404
        product.category_id = data.get('categoryId')
        product.product_sizes = json.dumps(data.get('productSizes')) if data.get('productSizes') else None
        product.product_colors = json.dumps(data.get('productColors')) if data.get('productColors') else None
        product.product_articul = data.get('productArticul')
        product.product_type = data.get('productType')
        product.product_name = data.get('productName')
        product.product_about = data.get('productAbout')
        product.product_descriptions = data.get('productDescriptions')
        product.product_price = data.get('productPrice')
        product.product_size_description = data.get('productSizeDescription')
        product.product_images = json.dumps(data.get('productImages')) if data.get('productImages') else None
        product.sale_price = data.get('salePrice')
        db.session.commit()
        return jsonify(product.json())
        return jsonify({"message": "Category updated successfully"})

    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
