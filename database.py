import json

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()

class Categories(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.String, primary_key=True, nullable=False)
    category_name = db.Column(db.String)
    image = db.Column(db.Text)

    def json(self):
        return {
            'id': self.id,
            'name': self.category_name,
            'image': self.image
        }

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String, nullable=False)
    product_sizes = db.Column(db.String)
    product_colors = db.Column(db.String)
    product_articul = db.Column(db.String)
    product_type = db.Column(db.String)
    product_name = db.Column(db.String)
    product_about = db.Column(db.String)
    product_descriptions = db.Column(db.String)
    product_price = db.Column(db.Float)
    product_size_description = db.Column(db.String)
    product_images = db.Column(db.String)  #
    sale_price = db.Column(db.Float)

    def as_dict(self):
        return {
            'categoryId': self.category_id,
            'productId': self.product_id,
            'productSizes': json.loads(self.product_sizes) if self.product_sizes else [],
            'productColors': json.loads(self.product_colors) if self.product_colors else [],
            'productArticul': self.product_articul,
            'productType': self.product_type,
            'productName': self.product_name,
            'productAbout': self.product_about,
            'productDescriptions': self.product_descriptions,
            'productPrice': self.product_price,
            'productSizeDescription': self.product_size_description,
            'productImages': json.loads(self.product_images) if self.product_images else [],
            'salePrice': self.sale_price if self.sale_price is not None else None
        }

    def json(self):
        return {
            'categoryId': self.category_id,
            'productId': self.product_id,
            'productSizes': json.loads(self.product_sizes) if self.product_sizes else [],
            'productColors': json.loads(self.product_colors) if self.product_colors else [],
            'productArticul': self.product_articul,
            'productType': self.product_type,
            'productName': self.product_name,
            'productAbout': self.product_about,
            'productDescriptions': self.product_descriptions,
            'productPrice': self.product_price,
            'productSizeDescription': self.product_size_description,
            'productImages': json.loads(self.product_images) if self.product_images else [],
            'salePrice': self.sale_price if self.sale_price is not None else None
        }

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_description = db.Column(db.String)
    review_image = db.Column(db.String)

    def as_dict(self):
        return {
            'id': self.id,
            'reviewDescription': self.review_description,
            'reviewImage': self.review_image
        }


from sqlalchemy import Column, Integer, String, Boolean

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255))
    parentName = Column(String(255))
    role = Column(Boolean)
    phone = Column(String(20))
    email = Column(String(255))
    sms_code = Column(String(100))

    def as_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'parentname': self.parentName,
            'role': self.role,
            'phone': self.phone,
            'email': self.email,
        }

class Order(db.Model):
    orderID = db.Column(db.String(50), primary_key=True)
    orderNumber = db.Column(db.String(50), nullable=True)
    orderDate = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    house = db.Column(db.String(10), nullable=True)
    apartments = db.Column(db.String(10))
    entrance = db.Column(db.String(10))
    floor = db.Column(db.String(10))
    commentary = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=True)
    deliveryService = db.Column(db.String(50), nullable=True)
    deliveryTrack = db.Column(db.String(50))
    deliveryAmount = db.Column(db.Float)
    totalAmount = db.Column(db.Float, nullable=True)

class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.String(50), db.ForeignKey('order.orderID'), nullable=True)
    productId = db.Column(db.String(50), nullable=True)
    productSizes = db.Column(db.String(50), nullable=True)
    productColor = db.Column(db.String(50), nullable=True)
    count = db.Column(db.Integer, nullable=True)

# # Выполните создание таблицы с помощью db.create_all() в вашем приложении Flask.
# class ProductSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Product
#
# class OrderSchema(ma.SQLAlchemyAutoSchema):
#     products = ma.Nested(ProductSchema, many=True)
#
#
#


