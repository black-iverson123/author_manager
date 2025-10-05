from flask import Blueprint, request, url_for, current_app
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.authors import Author, AuthorSchema
from api.utils.database import db
from api.utils.tools.extensions import allowed_extensions, allowed_file
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from flasgger import swag_from
import logging
import os

author_routes = Blueprint("author_routes", __name__)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


@author_routes.post('/')
@jwt_required()
@swag_from('../../docs/authors/create_author.yml')
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        logging.debug(f"Alert: {e}")
        return response_with(resp.INVALID_INPUT_422)

@author_routes.get('/')
@swag_from('../../docs/authors/get_authors.yml')
def get_author_list():
    data = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['id','first_name','last_name'])
    authors = author_schema.dump(data)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.get('/<int:author_id>')
@swag_from('../../docs/authors/get_author_by_id.yml')
def get_author_detail(author_id):
    data = Author.query.filter_by(id=author_id).first_or_404()
    author_schema = AuthorSchema()
    author = author_schema.dump(data)
    return response_with(resp.SUCCESS_200, value={"author": author})

@author_routes.put('/<int:author_id>')
@jwt_required()
@swag_from('../../docs/authors/update_author.yml')
def update_author_details(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    try:
        get_author.first_name = data['first_name']
        get_author.last_name = data['last_name']
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return response_with(resp.SUCCESS_200, value={"author": author})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.INVALID_INPUT_422)

@author_routes.patch('/<int:author_id>')
@jwt_required()
@swag_from('../../docs/authors/modify_author.yml')
def modify_author_details(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    try:
        if 'first_name' in data:
            get_author.first_name = data['first_name']
        if 'last_name' in data:
            get_author.last_name = data['last_name']
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return response_with(resp.SUCCESS_200, value={"author": author})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.INVALID_INPUT_422)

@author_routes.delete('/<int:author_id>')
@jwt_required()
@swag_from('../../docs/authors/delete_author.yml')
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    if get_author:
        try:
            db.session.delete(get_author)
            db.session.commit()
            return response_with(resp.SUCCESS_204)
        except Exception as error:
            logging.debug(f"Alert: {error}")
            db.session.rollback()
            return response_with(resp.INVALID_FIELD_NAME_SENT_422)
        
@author_routes.post('/avatar/<int:author_id>')
@jwt_required()
@swag_from('../../docs/authors/avatar_upload.yml')
def upload_avatar(author_id):
    try:
        file = request.files['avatar']
        get_author = Author.query.get_or_404(author_id)

        if not file or not allowed_file(file.content_type):
            return response_with(resp.INVALID_INPUT_422)

        
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            get_author.avatar = url_for('uploaded_file', filename=filename, _external=True)
            db.session.add(get_author)
            db.session.commit()
            author_schema = AuthorSchema()
            author = author_schema.dump(get_author)
            return response_with(resp.SUCCESS_200, value={"author": author})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.INVALID_INPUT_422)
    return response_with(resp.INVALID_INPUT_422)
