import os

import pytest
from urllib.parse import urlparse

from urnie.urn.forms import AddUriForm
from urnie import create_app

TEST_URN_KEY = 'test'
TEST_URN_URL = 'http://test.example.com'
TEST_URN_SUBSTITUTE_URL = 'http://test.example.com/%v'


@pytest.fixture
def app():
    os.environ['FLASK_ENV'] = 'test'
    app = create_app()
    return app


@pytest.fixture
def mock_urn(mocker):
    # hashed password of 'test'
    return mocker.patch('urnie.helper.urn_helper.get_urn', return_value={
        'urn': TEST_URN_KEY,
        'url': TEST_URN_URL,
        'approved': True,
        'date_added': 'testdate'
    })


@pytest.fixture
def mock_urn_substitute(mocker):
    return mocker.patch('urnie.helper.urn_helper.get_urn', return_value={
        'urn': TEST_URN_KEY,
        'url': TEST_URN_SUBSTITUTE_URL,
        'approved': True,
        'date_added': 'testdate'
    })


@pytest.fixture
def mock_get_all_urns_empty(mocker):
    return mocker.patch('urnie.helper.urn_helper.get_all_urns', return_value=[])


def test_go(app, mock_urn):
    with app.test_client() as c:
        response = c.get(f'/go/{TEST_URN_KEY}', follow_redirects=True)
        response_data = response.get_data(as_text=True)
        assert f'<meta http-equiv="refresh" content="0; URL={TEST_URN_URL}"/>' in response_data
        assert response.status_code == 200


def test_go_urn_exists(app, mock_urn):
    with app.test_client() as c:
        response = c.get(f'/go/{TEST_URN_KEY}', follow_redirects=True)
        response_data = response.get_data(as_text=True)
        assert f'<meta http-equiv="refresh" content="0; URL={TEST_URN_URL}"/>' in response_data
        assert response.status_code == 200


def test_add_urn_exists(app, mock_urn):
    with app.test_request_context():
        with app.test_client() as c:
            addform = AddUriForm(urn=TEST_URN_KEY, url=TEST_URN_URL)
            response = c.post('/go/add', data=addform.data)
            assert response.status_code == 302


def test_add_urn_whitespace(app, mock_urn):
    with app.test_request_context():
        with app.test_client() as c:
            addform = AddUriForm(urn='test urn', url=TEST_URN_URL)
            response = c.post('/go/add', data=addform.data)
            assert response.status_code == 302


# def test_go_substitute(app, mock_urn_substitute):
#     with app.test_client() as c:
#         response = c.get(f'/go/{TEST_URN_KEY}', follow_redirects=True)
#         response_data = response.get_data(as_text=True)
#         assert f'<meta http-equiv="refresh" content="0; URL={TEST_URN_URL}"/>' in response_data
#         assert response.status_code == 200
