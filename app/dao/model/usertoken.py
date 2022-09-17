from app.database import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .user import User


class UserToken(db.Model):
    __tablename__ = 'refreshtokens'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    refresh_token = Column(String, nullable=False)
    user_for_token = relationship("User")
