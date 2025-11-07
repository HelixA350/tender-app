from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

db = SQLAlchemy()
admin = Admin()

# --- Инициализация сервисов ---
from web.services import FileService, DataService, AgentService
file_service = FileService(r'web\tmp')
data_service = DataService(db)
agent_service = AgentService()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    from web.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from web.routes import bp
    from web.errors import error_bp
    app.register_blueprint(bp)
    app.register_blueprint(error_bp)

    from web.admin import init_admin
    init_admin(app, db)
   

    return app