from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(Integer, primary_key=True)
    notification_message = Column(String)
    notification_datetime = Column(DateTime)
    recipient_id = Column(Integer, ForeignKey('users.user_id'))
    notification_type = Column(String)

    recipient = relationship('User', backref='notifications')

    def __repr__(self):
        return f"<Notification(notification_id='{self.notification_id}', notification_message='{self.notification_message}', recipient_id='{self.recipient_id}', notification_type='{self.notification_type}')>"
    