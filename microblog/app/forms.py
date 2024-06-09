from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired , ValidationError , Email, EqualTo
from app.models import User 
import sqlalchemy as sa
from app import db

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    rememberMe = BooleanField("Remember Me", validators=[DataRequired()])
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(username).where(username))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter(User.email==email).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
