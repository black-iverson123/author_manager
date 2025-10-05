from src.api.utils.database import db
from passlib.hash import pbkdf2_sha256 as hasher
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @staticmethod
    def generate_hash(password):
        return hasher.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return hasher.verify(password, hash)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = User
        load_instance = True
        sqla_session = db.session
    
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
