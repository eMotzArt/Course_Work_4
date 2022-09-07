from app.database import db


class UserToken(db.Model):
    __tablename__ = 'refreshtokens'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    refresh_token = db.Column(db.String, nullable=False)
    user_for_token = db.relationship("User", back_populates="token_for_user")
