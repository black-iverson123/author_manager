from flask import Blueprint, request, url_for, render_template_string
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.models.users import User, UserSchema
from src.api.utils.database import db
from flask_jwt_extended import create_access_token
from src.api.utils.token import generate_token, verify_token
from src.api.utils.email import send_email
from src.api.utils.tools.email_templates import confirmation_email_html, subject
from flasgger import swag_from
from datetime import datetime
import logging
import traceback


user_routes = Blueprint('user_routes', __name__)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@user_routes.post("/register")
@swag_from('../../docs/users/create_user.yml')
def create_user():
    try:
        data = request.get_json()
        if (User.find_by_email(data['email']) is not None or User.find_by_username(data['username']) is not None):
            return response_with(resp.DUPLICATE_ENTRY_409)
        user_schema = UserSchema()
        user = user_schema.load(data)
        user_password_hashed = user.generate_hash(user.password)
        user.password = user_password_hashed
        token = generate_token(data['email'])
        email_verification = url_for('user_routes.verify_email', token=token, _external=True)
        html = render_template_string(confirmation_email_html, name=user.username, confirm_url=email_verification, year=datetime.now().year)
        send_email(user.email, subject, html)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user": result})
    except Exception as error:
        logging.debug(f"Alert: {error}")
        logging.error(traceback.format_exc())
        return response_with(resp.INVALID_INPUT_422)



@user_routes.get('/confirm/<token>')
@swag_from('../../docs/users/verify_email.yml')
def verify_email(token):
    try:
        email = verify_token(token)
    except:
        return response_with(resp.SERVER_ERROR_401)
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.verified:
        return response_with(resp.INVALID_INPUT_422)
    
    else:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={"message":
                                                      "Email verified, you can proceed to login now."})


@user_routes.post("/login")
@swag_from('../../docs/users/login_user.yml')
def login_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username']) or User.find_by_email(data['email'])
        if not current_user:
            return response_with(resp.UNAUTHORIZED_403)
        
        if current_user and not current_user.verified:
            return response_with(resp.BAD_REQUEST_400)

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=current_user.email)
            return response_with(resp.SUCCESS_200, value={"message": "Logged in as {}".format(current_user.username), "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as error:
        logging.debug(f"Alert: {error}")
        return response_with(resp.INVALID_INPUT_422)
