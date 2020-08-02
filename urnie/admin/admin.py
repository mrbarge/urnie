import datetime

from urnie.helper import urn_helper
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
    pending_urns = urn_helper.get_all_urns(approved=False)
    approved_urns = urn_helper.get_all_urns(approved=True)

    pending_table = PendingApproval(pending_urns)
    pending_table.classes = ['table']
    approved_table = Approved(approved_urns)
    approved_table.classes = ['table']
    return render_template('admin/approve.html', pending_table=pending_table, approved_table=approved_table)


@admin_bp.route('/approve/<urn>', methods=['GET', 'POST'])
@login_required
def approve(urn):
    try:
        if urn_helper.approve_urn(urn):
            flash(f'URN {urn} approved.', 'info')
        else:
            flash(f'URN {urn} could not be found.', 'error')
    except Exception as err:
        flash(f'An error occurred approving URN {urn}: {err}', 'error')

    return redirect(url_for('admin_bp.list'))


@admin_bp.route('/update/<urn>', methods=['GET', 'POST'])
@login_required
def update(urn):
    u = urn_helper.get_urn(urn)
    if not u:
        flash(f'URN "{urn}" could not be found.', 'error')
        return redirect(url_for('admin_bp.list'))

    update_form = AddUriForm()
    if request.method == 'POST' and update_form.validate():
        if urn_helper.change_urn_url(u['urn'], update_form.url.data):
            flash(f'URN "{urn}" updated successfully.', 'info')
        else:
            flash(f'URN "{urn}" could not be updated.', 'error')
        return redirect(url_for('admin_bp.list'))

    update_form.urn.data = u['urn']
    update_form.url.data = u['url']
    return render_template('admin/update.html', form=update_form)


@admin_bp.route('/delete/<urn>', methods=['POST', 'DELETE'])
@login_required
def delete(urn):
    if urn_helper.delete_urn(urn):
        flash(f'URN {urn} rejected and deleted.', 'info')
    else:
        flash(f'Could not find urn {urn}.', 'error')

    return redirect(url_for('admin_bp.list'))
