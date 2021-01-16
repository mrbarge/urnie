import pytest
from urnie.helper import urn_processors


def test_substitute():
    test_val = ['TEST']
    test_url = 'abc%v123'
    test_url_none = 'abc123'
    assert urn_processors.substitute(test_url, test_val) == 'abcTEST123'
    assert urn_processors.substitute(test_url_none, test_val) == 'abc123'
    assert urn_processors.substitute(test_url, '') == 'abc123'


def test_jira_textsearch():
    test_val = ['TEST']
    test_vals = ['TEST', 'TEST2']
    test_url = 'abc %j'
    test_url_none = 'abc123'
    assert urn_processors.jira_textsearch(test_url, test_val) == 'abc (text ~ "TEST" OR comment ~ "TEST")'
    assert urn_processors.jira_textsearch(test_url,
                                          test_vals) == 'abc (text ~ "TEST" OR comment ~ "TEST") AND (text ~ "TEST2" OR comment ~ "TEST2")'
    assert urn_processors.jira_textsearch(test_url_none, test_val) == 'abc123'
    assert urn_processors.jira_textsearch(test_url, '') == 'abc '


def test_process_urn_url():
    test_val = ['TEST']
    test_url = 'https://test.example.com/%v'
    assert urn_processors.process_urn_url(test_url, test_val) == 'https://test.example.com/TEST'
    assert urn_processors.process_urn_url(test_url, '') == 'https://test.example.com/'
