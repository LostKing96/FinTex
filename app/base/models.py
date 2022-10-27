# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
import sqlalchemy

from app import db

from app.base.util import hash_pass
from functools import wraps
import logging

from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from passlib.context import CryptContext
import smtplib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:

    def start_session(self, user):

        session['logged_in'] = True
        session['user'] = user['username']
        return session['user']

    def signup(self, username, email, password):
        print(request.form)

        # Create the user object
        user = {
            "username": username,
            "email": email,
            "password": password,
            "payment_status": "beginner"
        }

        # Encrypt the password
        user['hashed_password'] = pwd_context.hash((user['password']))

        if db.users.insert_one(user):
            return True
        return False

    def logout(self):
        session.clear()
        return redirect('/')

    def ResetPswd(self, emailUser):

        user = db.users.find_one({
            "email":emailUser
        })
        logging.error(user)
        # Добавляем необходимые подклассы - MIME-типы
        from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
        from email.mime.text import MIMEText  # Текст/HTML

        addr_from = "foo@yandex.ru"
        addr_to = emailUser
        password = "pass"  # пароль от почты addr_from

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = 'Reset password for Fintex.kz'  # Тема сообщения

        body = "Текст сообщения"
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
        # server.starttls()             # Начинаем шифрованный обмен по TLS
        server.login(addr_from, password)  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим



    def login(self, username, password):

        user = db.users.find_one({
            "username": username
        })
        logging.error(user)

        if user and pwd_context.verify(password, user['hashed_password']):
            self.start_session(user)
            return True
        return False


# make as user -- array
#  or make data -- array of the information
#  or 
# type -- index/lecture1/lecture2/lecture3// countructorBusiness/ConstructorFin
# it would be perfect if also could add the information about clicks and stuff??

class ClickInfo:
    def user_get(username, time, type):
        user_click_info = {
            "username": username,
            "access_time": time,
            "page": type
        }
        return True


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap
