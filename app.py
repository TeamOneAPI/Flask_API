from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes import api_bp
from auth import auth_bp
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(api_bp, url_prefix="/api")

# Swagger – US-06
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "BlueWave API",
        "requestInterceptor": """
            function(request) {
                // Automatically prepend 'Bearer ' if Authorization header exists
                if (request.headers['Authorization'] && !request.headers['Authorization'].startsWith('Bearer ')) {
                    request.headers['Authorization'] = 'Bearer ' + request.headers['Authorization'];
                }
                return request;
            }
        """
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
