import os
import sys
import logging
from flask import Flask, jsonify, send_from_directory
from src.api.utils.database import db
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.routes.authors import author_routes
from src.api.routes.books import book_routes
from src.api.routes.users import user_routes
from src.api.config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask_jwt_extended import JWTManager
from src.api.utils.email import mail
from flask_migrate import Migrate
from flasgger import Swagger
from src.api.utils.tools.extensions import swagger_template


def create_app(config):
    app = Flask(__name__)

    app.register_blueprint(author_routes, url_prefix='/api/authors')
    app.register_blueprint(book_routes, url_prefix='/api/books')
    app.register_blueprint(user_routes, url_prefix='/api/users')

    @app.route('/avatar/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if os.environ.get('FLASK_ENV') == 'production':
        app_config = ProductionConfig()
    elif os.environ.get('FLASK_ENV') == 'testing':
        app_config = TestingConfig()
    else:
        app_config = DevelopmentConfig()

    app.config.from_object(app_config)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


    @app.after_request
    def add_header(response):
        return response
        
    @app.errorhandler(400)
    def bad_request(error):
        logging.error(f"400 Bad Request: {error}")
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(404)
    def not_found(error):
        logging.error(f"404 Not Found: {error}")
        return response_with(resp.SERVER_ERROR_404)

    @app.errorhandler(500)
    def server_error(error):
        logging.error(f"500 Server Error: {error}")
        return response_with(resp.SERVER_ERROR_500)
    

    jwt = JWTManager(app)
    db.init_app(app) 
    mail.init_app(app)
    migrate = Migrate(app, db)

    swagger = Swagger(app, template=swagger_template)
    
    with app.app_context():
        db.create_all()
    
    return app

#created the app at module level so run.py can import ir
app = create_app(None) 

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', use_reloader=True)






