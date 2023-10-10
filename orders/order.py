import random
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, Order, OrderProduct, Product


class OrderChange(Resource):
    def put(self, order_id):
        order_data = request.get_json()

        # Ищем заказ по order_id
        order = Order.query.filter_by(orderID=order_id).first()
        if not order:
            return jsonify({'message': 'Заказ не найден'}), 404

        # Обновляем данные заказа
        order.city = order_data.get('city', order.city)
        order.phoneNumber = order_data.get('phoneNumber', order.phoneNumber)
        order.email = order_data.get('email', order.email)
        order.street = order_data.get('street', order.street)
        order.house = order_data.get('house', order.house)
        order.apartments = order_data.get('apartments', order.apartments)
        order.entrance = order_data.get('entrance', order.entrance)
        order.floor = order_data.get('floor', order.floor)
        order.commentary = order_data.get('commentary', order.commentary)
        order.status = order_data.get('status', order.status)
        order.deliveryService = order_data.get('deliveryService', order.deliveryService)
        order.deliveryTrack = order_data.get('deliveryTrack', order.deliveryTrack)
        order.deliveryAmount = order_data.get('deliveryAmount', order.deliveryAmount)
        order.totalAmount = order_data.get('totalAmount', order.totalAmount)

        # Обновляем данные продуктов в заказе
        if 'products' in order_data:
            products_data = order_data['products']
            for product_data in products_data:
                product = Product.query.get(product_data['id'])
                if product:
                    product.productSizes = product_data.get('productSizes', product.productSizes)
                    product.productColor = product_data.get('productColor', product.productColor)
                    product.count = product_data.get('count', product.count)

        db.session.commit()

        return jsonify({'message': 'Заказ успешно обновлен'}), 200


class OrderCreate(Resource):
    def post(self):
        order_data = request.get_json()
        print("GGG")
        # Создаем новый заказ
        new_order = Order(
            orderID=str(random.randint(100000, 999999)),
            orderNumber=str(random.randint(100000, 999999)),
            orderDate=datetime.now(),
            city=order_data['city'],
            phoneNumber=order_data['phoneNumber'],
            email=order_data['email'],
            street=order_data['street'],
            house=order_data['house'],
            apartments=order_data.get('apartments'),
            entrance=order_data.get('entrance'),
            floor=order_data.get('floor'),
            commentary=order_data.get('commentary'),
            totalAmount=order_data['totalAmount']
        )

        db.session.add(new_order)
        db.session.commit()

        # Создаем продукты в заказе
        if 'products' in order_data:
            products_data = order_data['products']
            for product_data in products_data:
                new_product = OrderProduct(
                    orderID=new_order.orderID,
                    productId=product_data['productId'],
                    productSizes=product_data['productSizes'],
                    productColor=product_data['productColor'],
                    count=product_data['count']
                )
                db.session.add(new_product)

        db.session.commit()

        return {'message': 'Заказ успешно создан', 'order_id': new_order.orderID}, 201


class OrderGetInfo(Resource):
    def get(self, order_id):
        order = Order.query.filter_by(orderID=order_id).first()
        if not order:
            return jsonify({'message': 'Заказ не найден'}), 404

        order_info = {
            'orderID': order.orderID,
            'orderNumber': order.orderNumber,
            'orderDate': order.orderDate,
            'city': order.city,
            'phoneNumber': order.phoneNumber,
            'email': order.email,
            'street': order.street,
            'house': order.house,
            'apartments': order.apartments,
            'entrance': order.entrance,
            'floor': order.floor,
            'commentary': order.commentary,
            'status': order.status,
            'deliveryService': order.deliveryService,
            'deliveryTrack': order.deliveryTrack,
            'deliveryAmount': order.deliveryAmount,
            'totalAmount': order.totalAmount,
        }

        products = []
        for product in OrderProduct.query.filter_by(orderID=order_id):
            product_info = {
                'productId': product.productId,
                'productSizes': product.productSizes,
                'productColor': product.productColor,
                'count': product.count,
            }
            products.append(product_info)

        order_info['products'] = products

        return jsonify(order_info)


class OrderCancel(Resource):
    def post(self, order_id):
        order = Order.query.filter_by(orderID=order_id).first()
        if order is not True:
            return "Not found order", 400
        order.status = "Отменен"
        db.session.commit()
        return "Заказ отменен", 200


class OrderGetList(Resource):
    @jwt_required()
    def get(self):
        orders = Order.query.filter_by(email=get_jwt_identity()).all()

        result = []
        for order in orders:
            order_info = {
                'orderID': order.orderID,
                'orderNumber': order.orderNumber,
                'orderDate': order.orderDate,
                'city': order.city,
                'phoneNumber': order.phoneNumber,
                'email': order.email,
                'street': order.street,
                'house': order.house,
                'apartments': order.apartments,
                'entrance': order.entrance,
                'floor': order.floor,
                'commentary': order.commentary,
                'status': order.status,
                'deliveryService': order.deliveryService,
                'deliveryTrack': order.deliveryTrack,
                'deliveryAmount': order.deliveryAmount,
                'totalAmount': order.totalAmount,
            }

            products = OrderProduct.query.filter_by(orderID=order.orderID).all()
            product_list = []
            for product in products:
                product_info = {
                    'productId': product.productId,
                    'productSizes': product.productSizes,
                    'productColor': product.productColor,
                    'count': product.count,
                }
                product_list.append(product_info)
            order_info['products'] = product_list

            result.append(order_info)

        return jsonify(result)
