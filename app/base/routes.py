# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import logging
import random
import smtplib
import ssl
import traceback

import email_validator
from flask import jsonify, render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from datetime import datetime
from app import db
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm1, ResetPasswordForm
from app.base.models import User

from app.base.util import verify_pass


@blueprint.route('/')
def route_default():
    if 'logged_in' in session:
        return redirect(url_for('authorized_blueprint.route_index'))
    elif "logged in" not in session:

        return redirect(url_for('base_blueprint.login'))


@blueprint.route('/grant_info')
def grant_info():
    return render_template("info_page.html")


## Login & Registration

@blueprint.route('/chgPass', methods=['GET', 'POST'])
def chgPass():
    Code = request.form.get('code')
    newPassword = request.form.get('password')
    Email = request.form.get('email')
    User = db.get_last(db.resetPswd, "email", Email)
    if User:
        ConfCode = str(User['code'])
        if Code == ConfCode:
            db.updatePassword(newPassword, Email)
            return "Пароль изменен."
        else:
            return "Код не совпал."
    else:
        return "Запроса на восстановление учетной записи не поступало."
@blueprint.route('/reset_password', methods=['GET', 'POST'])
def resetPassword():
    resetPasswordForm = ResetPasswordForm(request.form)
    if request.method == "GET":
        return render_template('accounts/reset_password.html', msg='Введите свой E-mail', form=resetPasswordForm)
    if request.method == "POST":
        pass



@blueprint.route('/sendCode', methods=['GET', 'POST'])
def sendCode():
        Email = request.form.get('email')
        User = db.get_one(db.users, "email", Email)
        if User:
            Code = random.randrange(1000, 9999)
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText  # Текст/HTML

            addr_from = "aimbetovaaizhan@yandex.kz"
            addr_to = Email
            password = "100mlnUSD"  # пароль от почты addr_from

            CodeReset = {
                "email": Email,
                "code": Code,
                "date": datetime.now()
            }
            db.insert(db.resetPswd, CodeReset)
            msg = MIMEMultipart()  # Создаем сообщение
            msg['From'] = addr_from  # Адресат
            msg['To'] = addr_to  # Получатель
            msg['Subject'] = f'Reset password for Fintex.kz for account {Email}'

            body = f"""\
            <html>
              <head></head>
              <body>
                <p>Здравствуйте.<br>
                   Ваш код для восстановления пароля учетной записи:<b>{Code}</b><br>
                   Код действителен для аккаунта {Email}<br>
                   Если вы не хотите сбрасывать пароль, просто проигнорируйте это письмо.
                </p>
              </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))
            server = smtplib.SMTP_SSL('smtp.yandex.kz', 465)
            server.login(addr_from, password)
            try:
                    server.send_message(msg)

            except Exception as e:
                    return f"Ошибка отправки письма.{traceback.format_exc()}"
            server.quit()
        else:
            return f"Пользователя с почтой {Email} не существует."
        return f"Код отправлен на почту {Email}"
        #return


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    logging.error("test")
    login_form = LoginForm(request.form)
    if request.method == "GET":
        return render_template('accounts/login.html', msg='Введите свои данные', form=login_form)
    if request.method == "POST":
        if 'login' in request.form:
            # read form data
            username = request.form['username']
            password = request.form['password']

        if User().login(username, password):
            # successfull login
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            username = session['user']
            click_info = {
                "username": username,
                "access_time": dt_string,
                "page": "login",
                "date_obj": now
            }
            db.insert(db.statistics, click_info)
            # return redirect(url_for('base_blueprint.route_default'))
            return redirect(url_for("authorized_blueprint.route_index"))
        elif User().login(username, password) is False:
            return render_template('accounts/login.html', msg='Неправильный логин или пароль', form=login_form)
        print(session)

    #     # Locate user
    #     user = User.query.filter_by(username=username).first()

    #     # Check the password
    #     if user and verify_pass( password, user.password):

    #         login_user(user)
    #         return redirect(url_for('base_blueprint.route_default'))

    #     # Something (user or pass) is not ok
    #     return render_template( 'accounts/login.html', msg='Неправильный логин или пароль', form=login_form)

    # if not current_user.is_authenticated:
    #     return render_template( 'accounts/login.html',
    #                             form=login_form)
    # return redirect(url_for('authorized_blueprint.index'))
    # return render_template('index.html')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm1(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check usename exists
        user = db.get_one(db.users, "username", username)
        if user:
            return render_template('accounts/register.html',
                                   msg='Это имя пользователя уже занято',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = db.get_one(db.users, "email", email)
        if user:
            return render_template('accounts/register.html',
                                   msg='Такой Email уже зарегистрирован',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        # user = User(**request.form)
        # db.session.add(user)
        # db.session.commit()
        if User().signup(username, email, password):
            return render_template('accounts/register.html',
                                   msg='Ваш аккаунт создан. Вы можете <a href="/login">Войти</a>',
                                   success=True,
                                   form=create_account_form)
        else:
            return render_template('accounts/register.html',
                                   msg='Технические проблемы, попробуйте еще раз',
                                   success=False,
                                   form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    User().logout()
    return redirect(url_for('base_blueprint.login'))


## Errors

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
