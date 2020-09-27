import datetime
import sqlalchemy
from fuzzywuzzy import process
from flask import app
from urnie.models import db, Uri


def get_all_urns(approved=True):
    '''
    Retrieve all URNs from the database.
    :param approved: Only approved URNs will be returned.
    :return: List of URNs
    '''
    try:
        all_uris = Uri.query.filter_by(approved=approved).all()
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception()

    results = [
        {
            "urn": uri.key,
            "url": uri.url,
            "approved": uri.approved,
            "date_added": uri.date_added
        } for uri in all_uris
    ]
    return results


def search_term(term):
    '''
    Search for an URN or URL matching the specified term
    :param term: Term to search for
    :return: Matching URN entries
    '''
    try:
        all_uris = Uri.query.filter(
            (Uri.approved == True) & ((Uri.key.like(f"%{term}%")) | (Uri.url.like(f"%{term}%")))).all()
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception()

    results = [
        {
            "urn": uri.key,
            "url": uri.url,
            "approved": uri.approved,
            "date_added": uri.date_added
        } for uri in all_uris
    ]

    return results


def get_urn(urn):
    '''
    Return the details of a specific URN
    :param urn: URN to retrieve
    :return:
    '''
    try:
        db_urn = Uri.query.filter_by(key=urn).first()
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception()

    if not db_urn:
        return None

    results = {
        "urn": db_urn.key,
        "url": db_urn.url,
        "approved": db_urn.approved,
        "date_added": db_urn.date_added
    }
    return results


def get_urns_like(urn):
    '''
    Return URNs that are similar to the supplied urn
    :param urn: URN used for matching
    :return:
    '''
    try:
        all_urns = get_all_urns()
    except Exception:
        return []

    if not all_urns:
        return []

    urn_choices = [u['urn'] for u in all_urns]
    matches = process.extractBests(urn, urn_choices)
    return [m[0] for m in matches]


def add_urn(urn, url):
    '''
    Add a new URN to the database
    :param urn: URN Key
    :param url: URN URL
    :return:
    '''
    u = Uri(key=urn, url=url, approved=False)
    try:
        db.session.add(u)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception()


def approve_urn(urn):
    '''
    Approve an URN in the database
    :param urn: URN to approve
    :return:
    '''
    try:
        u = Uri.query.filter_by(key=urn).first()
        if u:
            u.approved = True
            u.date_added = datetime.datetime.utcnow()
            db.session.commit()
        return u
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception('a database error occurred')


def change_urn_url(urn, url):
    '''
    Update an URN's URL
    :param urn: URN key
    :param url: URN URL
    :return:
    '''
    try:
        u = Uri.query.filter_by(key=urn).first()
        if u:
            u.url = url
            db.session.commit()
        return u
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception('a database error occurred')


def delete_urn(urn):
    '''
    Delete the specified URN from the database
    :param urn: URN key
    :return:
    '''
    try:
        u = Uri.query.filter_by(key=urn).first()
        if u is not None:
            db.session.delete(u)
            db.session.commit()
        return u
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception('a database error occurred')
