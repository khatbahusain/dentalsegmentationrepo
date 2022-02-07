import pytest
from __init__ import create_app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture(scope='module')
def new_user():
    user = User(email="newuser@gmail.com", name="newuser", password="123456")
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='patkennedy79@gmail.com', password='FlaskIsAwesome')
    user2 = User(email='kennedyfamilyrecipes@gmail.com', password='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='patkennedy79@gmail.com', password='FlaskIsAwesome'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
