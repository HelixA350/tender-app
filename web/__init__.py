from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

db = SQLAlchemy()
admin = Admin()

# --- Инициализация сервисов ---
from web.services import FileService, DataService, AgentService
file_service = FileService(r'web\tmp')
data_service = DataService(db)
agent_service = AgentService()
from web.services.request_handler_service import HandlerService
handler = HandlerService()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    from web.routes import bp
    app.register_blueprint(bp)

    from web.admin import init_admin
    init_admin(app, db)
   

    return app