from urnie.models import db, Uri
from urnie.urn.tables import UrnResults
from urnie.urn.forms import AddUriForm
from flask import Blueprint, render_template, current_app, request, url_for, redirect, flash

urn_bp = Blueprint('urn_bp', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='assets')


@urn_bp.route('/')
def list():
    all_uris = Uri.query.filter_by(approved=True).all()
    results = [
        {
            "urn": uri.key,
            "url": uri.url,
            "approved": uri.approved,
            "date_added": uri.date_added
        } for uri in all_uris
    ]
    table = UrnResults(results)
    return render_template('urn/list.html', table=table)


@urn_bp.route('/<urn>', methods=['GET'])
def go(urn):
    url = get_url(urn)
    if url is None:
        return render_template('urn/notfound.html', urn=urn)
    return render_template('urn/redirect.html', url=str(url))


@urn_bp.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddUriForm()

    if request.method == 'POST':
        if add_form.validate():
            uri = request.form['urn']
            url = request.form['url']

            existing_uri = Uri.query.filter_by(key=uri).first()
            if existing_uri is None:
                u = Uri(key=uri, url=url, approved=False)
                db.session.add(u)
                db.session.commit()
                flash(f'URN request "{uri}" has been submitted for approval.', 'info')
            else:
                flash(f'URN "{uri}" is already taken.', 'error')

            return redirect(url_for('urn_bp.list'))

    return render_template('urn/add.html', form=add_form)


def get_url(urn):
    if urn == None:
        return None

    db_uri = Uri.query.filter_by(key=urn).first()
    if db_uri is not None:
        return db_uri.url

    return None
