from flask_script import Manager
from website import create_app
from website import db
from datetime import datetime
from website.models import User

app = create_app()
manager = Manager(app)


@manager.command
def create_admin():
    db.session.add(User(
        email="ad@min.com",
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.utcnow)
    )
    db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)