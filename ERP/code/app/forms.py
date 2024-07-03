from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from  app.models import Sponcer , Influencer
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    role = SelectField('Role', choices=[('admin', 'Admin'), ('sponcer', 'Sponcer'), ('influencer', 'Influencer')])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    image = StringField('Image')
    description =  StringField('Description')
    industry = StringField('Industry')


    submit = SubmitField('Register')
    def validate_username(self, username):
        user = Sponcer.query.filter_by(username=username.data).first()
        if user is not None:
            if user.username == current_user.username:
                pass
            else:
                raise ValidationError('Please use a different username.')

class SponcerRegistration(RegistrationForm):
    pass # intentially left blank
    

    

class InfluncerRegistration(RegistrationForm):
    youtube = IntegerField('youtube', default = 0, validators=[DataRequired()])
    insta = IntegerField('insta', default = 0, validators=[DataRequired()])
    facebook = IntegerField('facebook', default = 0, validators=[DataRequired()])
    min_budget = IntegerField('min_budget', default = 0, validators=[DataRequired()])
    niche = StringField('Niche')



class CampainForm(FlaskForm):
    
    
    name = StringField('Name', validators=[DataRequired()])
    image = StringField('Image')
    description =  StringField('Description')
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('Start Date', validators=[DataRequired()])
    visibility = SelectField('Role', choices=[('private', 'Private'), ('public', 'Public')], default='private')
    goals = StringField('Terms', validators=[DataRequired()])            # TODO make api for this shit better
    budget = IntegerField('Budget',validators=[DataRequired()])
    niche = StringField('Niche')
    submit = SubmitField('Add')

class addAdsForm(FlaskForm):
    
    
    name = StringField('Name', validators=[DataRequired()])
    description =  StringField('Description')
    term = StringField('Terms', validators=[DataRequired()])            # TODO make api for this shit better
    payment = IntegerField('Budget',validators=[DataRequired()])
    influencer_id = IntegerField('InfluencerId', validators=[DataRequired()])  #Todo make new page where a user can go asnd select the user form there 
    submit = SubmitField('Add')
    # camp_id = db.Column(db.BigInteger, db.ForeignKey('sponcer.id'), nullable=False) #Todo make it automatically pulled 

class addAdsFormFind(FlaskForm):
    
    
    name = StringField('Name', validators=[DataRequired()])
    description =  StringField('Description')
    term = StringField('Terms', validators=[DataRequired()])            # TODO make api for this shit better
    payment = IntegerField('Budget',validators=[DataRequired()])
    campainId = IntegerField('campain Id', validators=[DataRequired()])  #Todo make new page where a user can go asnd select the user form there 
    submit = SubmitField('Add')
    # camp_id = db.Column(db.BigInteger, db.ForeignKey('sponcer.id'), nullable=False) #Todo make it automatically pulled 

