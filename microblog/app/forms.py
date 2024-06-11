""" Forms for input form users"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    """
    Login form

    Args:
        username: str
        password: str
        remember_me: bool
        submit: SubmitField
    
    Returns:
        LoginForm instance
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Registration form

    Args:
        username: str
        email: str
        password: str
        password2: str
        submit: Submit
    
    Returns:
        RegistrationForm instance
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Check if username is valid

        Args:
            username: str

        Returns:
            None

        """
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Check if email is valid

        Args:
            email: str
        """
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    """
    Edit profile form

    Args:
        username: str
    """

    username = StringField('Username', validators=[DataRequired()])
    about_me = StringField('About me', validators=[Length(min= 0 , max= 255)])
    submit = SubmitField('Submit')

    def __init__(self,original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        Check if username is valid

        Args:
            username: str
        """

        if username.data!= self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')

class EmptyForm(FlaskForm):
    """ Empty form"""
    submit = SubmitField('Submit')
