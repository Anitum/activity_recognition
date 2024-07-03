from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import db, login



# Define your models
db.ForeignKeyConstraint(['camp_id'], ['campaign.id'])
db.ForeignKeyConstraint(['spons_index'], ['sponcer.id'])
db.ForeignKeyConstraint(['ads'], ['advertisement.id'])

@login.user_loader
def load_user(id):
    return Sponcer.query.get(int(id))

class Sponcer(UserMixin, db.Model):
    __tablename__ = 'sponcer'
    id = db.Column(db.Integer, primary_key=True)
    flagged = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    industry =  db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True, server_default="0") 


    password_hash = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Sponcer %r>' % self.name
    

    def profilePicture(self, size):
        # not perfect, but it works
                                                                                        #Todo make it work 
        return 'https://www.gravatar.com/avatar/' + md5((self.username +'@gmail.com' ).lower().encode('utf-8')).hexdigest() + '?d=identicon&s=' + str(size)

    

class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True )
    flagged = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    term = db.Column(db.JSON, nullable=False)
    payment = db.Column(db.Integer, nullable=False)
    influencer_id = db.Column(db.Integer, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True, server_default="0") 
    statusAccepted = db.Column(db.String(4), nullable=True)
    done = db.Column(db.Boolean, default=False)
    


    def __repr__(self):
        return '<Advertisement %r>' % self.name
            
    def profilePicture(self, size):
        # not perfect, but it works
                                                                                        #Todo make it work 
        return 'https://www.gravatar.com/avatar/' + md5((self.name +'@gmail.com' ).lower().encode('utf-8')).hexdigest() + '?d=identicon&s=' + str(size)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    flagged = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    visibility = db.Column(db.String(255), nullable=False)
    goals = db.Column(db.JSON, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    spons_index = db.Column(db.Integer, db.ForeignKey('sponcer.id'), nullable=False)
    niche = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True, server_default="0") 


    def __repr__(self) -> str:
        return '<Campaign %r>' % self.name
        
    def profilePicture(self, size):
        # not perfect, but it works
                                                                                        #Todo make it work 
        return 'https://www.gravatar.com/avatar/' + md5((self.name +'@gmail.com' ).lower().encode('utf-8')).hexdigest() + '?d=identicon&s=' + str(size)


class Influencer(UserMixin, db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    flagged = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.Integer, nullable=False)
    insta = db.Column(db.Integer, nullable=False)
    facebook = db.Column(db.Integer, nullable=False)
    min_budget = db.Column(db.Integer, nullable=False)
    ads = db.Column(db.Integer, db.ForeignKey('advertisement.id'), nullable=True)
    industry =  db.Column(db.String(255), nullable=True)
    niche = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True, server_default="0") 


    password_hash = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self) -> str:
        return '<Influencer %r>' % self.name
            
    def profilePicture(self, size):
        # not perfect, but it works
                                                                                        #Todo make it work 
        return 'https://www.gravatar.com/avatar/' + md5((self.name +'@gmail.com' ).lower().encode('utf-8')).hexdigest() + '?d=identicon&s=' + str(size)
    
class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True, server_default="0") 



    password_hash = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
            
    def profilePicture(self, size):
        # not perfect, but it works
                                                                                        #Todo make it work 
        return 'https://www.gravatar.com/avatar/' + md5((self.name +'@gmail.com' ).lower().encode('utf-8')).hexdigest() + '?d=identicon&s=' + str(size)

    def __repr__(self):
        return '<admin %r>' % self.name
    

    
    





