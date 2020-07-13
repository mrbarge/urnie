from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='assets')


@admin_bp.route('/', methods=['GET'])
def show():
    return render_template('admin/show.html')

@admin_bp.route('/<urn>', methods=['DELETE'])
def delete(urn):
    return render_template('urn/delete.html', urn=urn)
