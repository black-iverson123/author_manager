from api.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Date)
    edition = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, title, year, edition, author_id):
        self.title = title
        self.year = year
        self.edition = edition
        self.author_id = author_id
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class BookSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Book
        load_instance = True
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    year = fields.Date(required=True)
    edition = fields.String(required=True)
    author_id = fields.Integer()