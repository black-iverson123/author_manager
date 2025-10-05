# utils/file_validation.py
allowed_extensions = set(['image/jpg', 'jpeg', 'image/png'])

def allowed_file(filename):
    return filetype in allowed_extensions



swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Author and Books API",
        "description": "Documentation for APIs",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    }
}