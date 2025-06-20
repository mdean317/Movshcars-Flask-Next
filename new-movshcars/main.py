import os
from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.blueprints import blueprints 
from app.init_db_data import init_db_data
from flask_login import LoginManager
from app.models.user import User
from dotenv import load_dotenv



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'movshcars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

if not app.secret_key:
    raise ValueError("No FLASK_SECRET_KEY set! Please set the environment variable.")
    

for bp in blueprints:
    app.register_blueprint(bp)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

with app.app_context():
        print("Tables detected:", db.metadata.tables.keys())
        print("DB will be created at:", os.path.abspath("movshcars.db"))
        db.create_all() 
        init_db_data()   

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=4000, debug=True)