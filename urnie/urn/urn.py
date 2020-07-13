from flask import Blueprint, render_template, current_app

urn_bp = Blueprint('urn_bp', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='assets')


@urn_bp.route('/', methods=['GET'])
def list():
    return render_template('urn/list.html')


@urn_bp.route('/<urn>', methods=['GET'])
def redirect(urn):
    url = get_url(urn)
    if url is None:
        return render_template('urn/notfound.html', urn=urn)
    url = url.decode('UTF-8')
    return render_template('urn/redirect.html', url=str(url))


def get_url(urn):
    redis_client = current_app.extensions['redis']
    return redis_client.get(urn)


def get_all():
    redis_client = current_app.extensions['redis']
    return redis_client.keys('*')
