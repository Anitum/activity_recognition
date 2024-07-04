from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import db, login



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from sqlalchemy import Column, Integer, String, Date, Float, JSON, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import os

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///your_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Redis
app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize extensions
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    date_of_joining = Column(Date, nullable=False)
    password = Column(String(255), nullable=False)
    performance_score = Column(Float(53), nullable=False)
    identity_verification_document = Column(JSON, nullable=False)
    facility_id = Column(Integer, ForeignKey('facilities.id', ondelete='CASCADE'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    facility = relationship('Facility', back_populates='users')
    address = relationship('Address', back_populates='users')

class Employee(User):
    __tablename__ = 'employees'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    salary = Column(DECIMAL(10, 2), nullable=False)
    bonus = Column(DECIMAL(10, 2), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False)
    additional_responsibility_id = Column(Integer, ForeignKey('additional_responsibilities.id', ondelete='SET NULL'))
    salary_account = Column(JSON, nullable=False)
    qualification_document = Column(JSON, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
    }

    department = relationship('Department', back_populates='employees')
    additional_responsibility = relationship('AdditionalResponsibility', back_populates='employees')

class Teacher(Employee):
    __tablename__ = 'teachers'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    section = relationship('Section', back_populates='teachers')

class Manager(Employee):
    __tablename__ = 'managers'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    team_size = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }

class PublicRelation(Employee):
    __tablename__ = 'public_relations'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    conversion_rate = Column(Float(53), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'public_relation',
    }

class HelpingStaff(Employee):
    __tablename__ = 'helping_staff'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    role = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'helping_staff',
    }

class Driver(Employee):
    __tablename__ = 'drivers'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    license_number = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'driver',
    }

class Guard(Employee):
    __tablename__ = 'guards'

    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    shift = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'guard',
    }

class Student(User):
    __tablename__ = 'students'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    fees = Column(DECIMAL(10, 2), nullable=False)
    pending_fees = Column(DECIMAL(10, 2), nullable=False)
    date_of_billing = Column(Date, nullable=False)
    picture = Column(JSON, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    section = relationship('Section', back_populates='students')

class Parent(User):
    __tablename__ = 'parents'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    education_level = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'parent',
    }

class Owner(User):
    __tablename__ = 'owners'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    ownership_percentage = Column(Float(53), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }

class Admin(User):
    __tablename__ = 'admins'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    access_level = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

# Other models (not inheriting from User)

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    emp_issue_id = Column(Integer, ForeignKey('employees.id', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    emp_issue = relationship('Employee', back_populates='materials')

class AdditionalResponsibility(Base):
    __tablename__ = 'additional_responsibilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    employees = relationship('Employee', back_populates='additional_responsibility')

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_students = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    students = relationship('Student', back_populates='section')
    teachers = relationship('Teacher', back_populates='section')

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_line = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    users = relationship('User', back_populates='address')
    facilities = relationship('Facility', back_populates='address')

class Facility(Base):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    revenue_generated_per_month = Column(DECIMAL(10, 2), nullable=False)
    expense = Column(DECIMAL(10, 2), nullable=False)
    rent = Column(DECIMAL(10, 2), nullable=False)
    area = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    address = relationship('Address', back_populates='facilities')
    users = relationship('User', back_populates='facility')

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    employees = relationship('Employee', back_populates='department')

# Example route using both SQLAlchemy and Redis
@app.route('/user/<int:user_id>')
def get_user(user_id):
    # Try to get user from Redis cache first
    cached_user = redis_client.get(f'user:{user_id}')
    if cached_user:
        return cached_user.decode('utf-8')
    
    # If not in cache, get from database
    user = User.query.get(user_id)
    if user:
        user_data = f"{user.first_name} {user.last_name}"
        # Cache the result in Redis for 1 hour (3600 seconds)
        redis_client.setex(f'user:{user_id}', 3600, user_data)
        return user_data
    return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
    
    





