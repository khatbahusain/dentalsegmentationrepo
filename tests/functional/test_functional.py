"""
This file (test_users.py) contains the functional tests for the `users` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `users` blueprint.
"""


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200


def test_signup_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/signup')
    assert response.status_code == 200


def test_predictions_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/predictions')
    assert response.status_code == 302


def test_about_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/about')
    assert response.status_code == 404


def test_profile_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.post('/profile', follow_redirects=True)
    assert response.status_code == 200



def test_login_already_logged_in(test_client, init_database, login_default_user):
    response = test_client.post('/login',
                                data=dict(email='patkennedy79@gmail.com', 
                                name = "user",
                                password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200



def test_valid_login_logout(test_client, init_database):

    response = test_client.post('/login',
                                data=dict(email='patkennedy79@gmail.com', 
                                name = "user",
                                password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200




def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/signup',
                                data=dict(email='patkennedy79@yahoo.com',
                                          name = "user",
                                          password='FlaskIsGreat',
                                          confirm='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200



