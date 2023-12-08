from src.web.controllers.users import users_bp
from src.web.controllers.institutions import institution_bp
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.home import home_bp
from src.web.controllers.services import service_bp

def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(institution_bp)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_bp)
    app.register_blueprint(service_bp)