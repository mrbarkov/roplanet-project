import json
import string
from random import random
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, jsonify
from flask_restful import Resource
from database import db, Product, User


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user_create = User(
            first_name=data["firstname"],
            last_name=data["lastname"],
            email=data["email"],
        )
        db.session.add(user_create)
        db.session.commit()
        user_create.sms_code = "748465"
        db.session.commit()
        # access_token = create_access_token(identity=data['email'])
        # refresh_token = create_refresh_token(identity=data['email'])
        # print(access_token, refresh_token)
        # print(user_create.sms_code)
        send_confirmation_email(data["email"], user_create.sms_code)
        return


class UserSmsConfirm(Resource):
    def post(self):
        data = request.get_json()
        user_get = User.query.filter_by(email=data["email"]).first()

        if user_get.sms_code == data["code"]:
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return "Mone", 401


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user_get = User.query.filter_by(email=data["email"]).first()
        user_get.sms_code = ''.join(random.choices(string.digits, k=6))
        db.session.commit()
        if user_get:
            send_confirmation_email(data["email"], user_get.sms_code)
        return "j", 401


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify(access_token=access_token)


def send_confirmation_email(email, code):
    smtp_server = "smtp.yandex.ru"
    smtp_port = 587

    # Ваш адрес электронной почты и пароль
    email_address = "Fleptn@yandex.ru"
    email_password = ""
    to_email = email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = "Код подтверждения Roplanet"
    body = f"Ваш код поддтверждения {code}."
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, to_email, msg.as_string())
    server.quit()

    print("Письмо отправлено успешно.")
