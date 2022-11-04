# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm, Form, validators
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired,regexp

## login and registration

class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login'   , validators=[DataRequired(),])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    Email = StringField('E-mail', id='username_email'   , validators=[DataRequired(),Email()])
    Code = StringField('Code', id='CodeReset', validators=[DataRequired()])
    password = PasswordField('New Password', id='newPassword', validators=[DataRequired()])


class CreateAccountForm1(FlaskForm):
    username = StringField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = StringField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
