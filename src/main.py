import sys
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.database.core import session_factory # noqa
from src.models import User # noqa
from src.services import UserService # noqa
from src.views.auth import router as auth_app # noqa
from src.views.appointment import router as appointments_app # noqa
from src.views.index import router as index_app # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
app.debug = True

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"  # type: ignore


@login_manager.user_loader
def load_user(id: int) -> User | None:
    with session_factory() as session:
        user = UserService(session).get(id)
    return user


app.register_blueprint(auth_app)
app.register_blueprint(index_app)
app.register_blueprint(appointments_app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404


if __name__ == "__main__":
    app.run(port=5000)
