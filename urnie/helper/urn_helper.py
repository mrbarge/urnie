import datetime
import sqlalchemy
from fuzzywuzzy import process

from urnie.models import db, Uri


def get_all_urns(approved=True):
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


def search_urn(term):
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
    u = Uri(key=urn, url=url, approved=False)
    try:
        db.session.add(u)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception()


def approve_urn(urn):
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
    try:
        u = Uri.query.filter_by(key=urn).first()
        if u:
            u.url = url
            db.session.commit()
        return u
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception('a database error occurred')


def delete_urn(urn):
    try:
        u = Uri.query.filter_by(key=urn).first()
        if u is not None:
            db.session.delete(u)
            db.session.commit()
        return u
    except sqlalchemy.exc.SQLAlchemyError:
        raise Exception('a database error occurred')

