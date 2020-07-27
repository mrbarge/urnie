from urnie.admin.tables import PendingApproval, Approved
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_manager
from urnie.models import db, Uri
from urnie.urn.forms import AddUriForm

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='templates',
                     static_folder='static', static_url_path='assets')


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def list():
    pending_urns = Uri.query.filter_by(approved=False).all()
    pending_results = [
        {
            "urn": uri.key,
            "url": uri.url
        } for uri in pending_urns
    ]
    approved_urns = Uri.query.filter_by(approved=True).all()
    approved_results = [
        {
            "urn": uri.key,
            "url": uri.url
        } for uri in approved_urns
    ]

    pending_table = PendingApproval(pending_results)
    approved_table = Approved(approved_results)
    return render_template('admin/approve.html', pending_table=pending_table, approved_table=approved_table)


@admin_bp.route('/approve/<urn>', methods=['GET', 'POST'])
@login_required
def approve(urn):
    db_uri = Uri.query.filter_by(key=urn).first()
    if db_uri is not None:
        db_uri.approved = True
        db.session.commit()
        flash(f'URN {urn} approved.', 'info')
    else:
        flash(f'Could not find urn {urn}.', 'error')

    return redirect(url_for('admin_bp.list'))


@admin_bp.route('/update/<urn>', methods=['GET', 'POST'])
@login_required
def update(urn):
    db_uri = Uri.query.filter_by(key=urn).first()
    update_form = AddUriForm()
    if db_uri:
        if request.method == 'POST' and update_form.validate():
            db_uri.url = update_form.url.data
            db.session.commit()
            flash(f'URN "{urn}" updated successfully.', 'info')
            return redirect(url_for('admin_bp.list'))

        update_form.urn.data = db_uri.key
        update_form.url.data = db_uri.url
    else:
        flash(f'URN "{urn}" could not be found.', 'error')
    return render_template('admin/update.html', form=update_form)


@admin_bp.route('/delete/<urn>', methods=['POST', 'DELETE'])
@login_required
def delete(urn):
    db_uri = Uri.query.filter_by(key=urn).first()
    if db_uri is not None:
        db.session.delete(db_uri)
        db.session.commit()
        flash(f'URN {urn} rejected and deleted.', 'info')
    else:
        flash(f'Could not find urn {urn}.', 'error')

    return redirect(url_for('admin_bp.list'))
