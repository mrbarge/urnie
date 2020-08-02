from flask_table import Table, Col, LinkCol


class UrnResults(Table):
    id = Col('Id', show=False)
    urn = LinkCol('URN', url_kwargs=dict(urn='urn'), attr=('urn'), endpoint='urn_bp.go')
    url = Col('URL')
    approved = Col('Approved')
    date_added = Col('Date Added')
