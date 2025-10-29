from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

from web.routes import bp
app.register_blueprint(bp)