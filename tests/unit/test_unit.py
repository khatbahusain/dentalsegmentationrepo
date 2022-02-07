"""
GIVEN a Flask application configured for testing
WHEN the 'route' page is requested (GET)
THEN check the response is valid
"""



from models import User
from __init__ import db

from werkzeug.security import generate_password_hash, check_password_hash


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """

    user = User(email="newuser@gmail.com", name="newuser", password=generate_password_hash("123456", method='sha256')) #

    assert user.email == 'newuser@gmail.com'
    assert user.name == 'newuser'
    assert user.password != '123456'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    user = User(email="newuser@gmail.com", name="newuser", password="123456")

    assert new_user.email == 'newuser@gmail.com'
    assert new_user.name == "newuser"
    assert new_user.password == "123456"
    
    
def test_make_prediction(test_client, init_database):
    response = test_client.post('/profile', follow_redirects=True)

    import cv2
    import base64
    import json
    import requests

    # read the file test.png and encode it into base64
    img = cv2.imread('test.png')
    _, img_encoded = cv2.imencode('.png', img)
    x_image = base64.b64encode(img_encoded).decode("utf-8")

    payload = json.dumps({"base64str": x_image,})

    response = requests.put("http://127.0.0.1:8000/predict", data = payload)

    assert response.status_code == 200
