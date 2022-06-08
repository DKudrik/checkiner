from app import application, db
from app.models import User, Post


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    application.run()
