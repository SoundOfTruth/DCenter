from main import app, db


def drop_tables():
    with app.app_context():
        db.drop_all()


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    drop_tables()
    create_tables()