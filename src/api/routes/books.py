from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import BookSchema, Book
from flask_jwt_extended import jwt_required
from api.utils.database import db
from flasgger import swag_from
import logging

book_routes = Blueprint("book_routes", __name__)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@book_routes.post('/')
@jwt_required()
@swag_from('../../docs/books/create_book.yml')
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data)
        result =    book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.INVALID_INPUT_422)

@book_routes.get('/')
@swag_from('../../docs/books/list_books.yml')
def list_books():
    retrieved = Book.query.all()
    try:
        book_schema = BookSchema(many=True, only=['author_id', 'year', 'title','edition'])
        books = book_schema.dump(retrieved)
        return response_with(resp.SUCCESS_200, value={"books": books})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.BAD_REQUEST_400)

@book_routes.get('/<int:book_id>')
@swag_from('../../docs/books/get_book_detail.yml')
def get_book_detail(book_id):
    data = Book.query.get_or_404(book_id)
    try:
        book_schema = BookSchema()
        book = book_schema.dump(data)
        return response_with(resp.SUCCESS_200, value={'book': book})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.BAD_REQUEST_400)

@book_routes.put('/<int:book_id>')
@jwt_required()
@swag_from('../../docs/books/update_book.yml')
def update_book_detail(book_id):
    data = request.get_json()


    if not data:
        return response_with(resp.BAD_REQUEST_400)

    get_book = Book.query.get_or_404(book_id)
    try: 
            get_book.title = data['title']
            get_book.year = data['year']
            get_book.edition = data['edition']
            db.session.add(get_book)
            db.session.commit()
            book_schema = BookSchema()
            book = book_schema.dump(get_book)
            return response_with(resp.SUCCESS_200, value={"book": book})
    except Exception as error:
            logging.debug(f'Alert: {error}')
            db.session.rollback()
            return response_with(resp.BAD_REQUEST_400)

@book_routes.patch('/<int:book_id>')
@jwt_required()
@swag_from('../../docs/books/modify_book.yml')
def modify_book_detail(book_id):
    data = request.get_json()
    if data:
        get_book = Book.query.get_or_404(book_id)
        try:
            if 'title' in data:
                get_book.title = data['title']
            if 'year' in data:
                get_book.year = data['year']
            if 'edition' in data:
                get_book.edition = data['edition']
            
            db.session.add(get_book)
            db.session.commit()
            book_schema = BookSchema()
            book = book_schema.dump(get_book)
            return response_with(resp.SUCCESS_200, value={"book": book})
        except Exception as error:
            logging.debug(f"Alert: {error}")
            db.session.rollback()
            return response_with(resp.BAD_REQUEST_400)

@book_routes.delete('/<int:book_id>')
@jwt_required()
@swag_from('../../docs/books/delete_book.yml')
def delete_book(book_id):
    get_book = Book.query.get_or_404(book_id)
    if get_book:
        try:
            db.session.delete(get_book)
            db.session.commit()
            return response_with(resp.SUCCESS_204)
        except Exception as error:
            logging.debug(f"Alert: {error}")
            return response_with(resp.BAD_REQUEST_400)

