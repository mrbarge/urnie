from urnie.helper import urn_helper
from urnie.models import db, Uri
from urnie.urn.tables import UrnResults
from urnie.urn.forms import AddUriForm, ListUrnsForm
from flask import Blueprint, render_template, current_app, request, url_for, redirect, flash

urn_bp = Blueprint('urn_bp', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='assets')


@urn_bp.route('/')
def list():
    all_urns = urn_helper.get_all_urns(approved=True)
    table = UrnResults(all_urns)
    table.classes = ['table']
    search_form = ListUrnsForm()

    return render_template('urn/list.html', form=search_form, table=table)


@urn_bp.route('/search', methods=['POST'])
def search():
    search_form = ListUrnsForm()

    try:
        if search_form.validate_on_submit():
            term = search_form.search.data
            if term:
                matching_urns = urn_helper.search_urn(term)
                table = UrnResults(matching_urns)
                table.classes = ['table']
                return render_template('urn/list.html', form=search_form, table=table)
    except Exception as err:
        flash(f'An error occurred whilst searching: {err}', 'error')

    return redirect(url_for('urn_bp.list'))


@urn_bp.route('/<urn>', methods=['GET'])
def go(urn):
    try:
        u = urn_helper.get_urn(urn)
    except Exception as e:
        return render_template('urn/notfound.html', urn=urn, close_matches=[])

    if u is None:
        # get similar matches
        matches = urn_helper.get_urns_like(urn)
        return render_template('urn/notfound.html', urn=urn, close_matches=matches)

    return render_template('urn/redirect.html', url=u['url'])


@urn_bp.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddUriForm()

    if request.method == 'POST':
        if add_form.validate():
            urn = request.form['urn']
            url = request.form['url']

            try:
                existing_urn = urn_helper.get_urn(urn)
                if existing_urn is None:
                    urn_helper.add_urn(urn, url)
                    flash(f'URN request "{urn}" has been submitted for approval.', 'info')
                else:
                    flash(f'URN "{urn}" is already taken.', 'error')
            except Exception as e:
                flash(f'An error occurred adding the URN: {e}', 'error')

            return redirect(url_for('urn_bp.list'))

    return render_template('urn/add.html', form=add_form)
