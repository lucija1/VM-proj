import os

from dotenv import load_dotenv
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from VM_proj_flask.extensions import db

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def get_token(self, expire_timer=600):
        serial = Serializer(SECRET_KEY, expires_in=expire_timer)
        return serial.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_token(token):
        serial = Serializer(SECRET_KEY)
        try:
            user_id = serial.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
