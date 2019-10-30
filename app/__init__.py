from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pandas as pd
import os

current_dir_path = os.path.dirname(os.path.abspath(__file__))
# read rating matrix
df_rating = pd.read_json(os.path.join(current_dir_path, 'res/rating.json'), encoding='utf-8')
df_rating_ave = df_rating.groupby(['useridindex', 'businessidindex']).mean()
E_o = df_rating_ave.pivot(index='userorder', columns='itemorder', values='stars')
E_o = E_o.fillna(0)
E_o = E_o.values
E = E_o.astype(float)
indexdir = os.path.join(current_dir_path, 'res/indexdir')

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'LukeZSWsupersecretstring'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
