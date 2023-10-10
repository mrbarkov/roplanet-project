import random
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, jsonify
from flask_restful import Resource
from database import db, User


class UserGetInfo(Resource):
    @jwt_required()
    def get(self):
        get_user = User.query.filter_by(email=get_jwt_identity()).first()
        return jsonify(get_user.as_dict())

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
        user_create.sms_code = str(random.randint(100000, 999999))
        db.session.commit()
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
        if user_get is not True:
            return "User not found", 401
        user_get.sms_code = str(random.randint(100000, 999999))
        db.session.commit()
        if user_get:
            send_confirmation_email(data["email"], code=str(user_get.sms_code))
            return "Good xuiny", 200
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
    email_address = "iambitkov@yandex.ru"
    email_password = "kdkewoxsfhxmvlsr"
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
