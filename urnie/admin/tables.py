from flask_table import Table, Col, LinkCol, ButtonCol


class PendingApproval(Table):
    id = Col('Id', show=False)
    urn = Col('URN')
    url = Col('URL')
    approve = ButtonCol('Approve', 'admin_bp.approve', url_kwargs=dict(urn='urn'))
    delete = ButtonCol('Delete', 'admin_bp.delete', url_kwargs=dict(urn='urn'))

class Approved(Table):
    id = Col('Id', show=False)
    urn = Col('URN')
    url = Col('URL')
    update = ButtonCol('Update', 'admin_bp.update', url_kwargs=dict(urn='urn'))
    delete = ButtonCol('Delete', 'admin_bp.delete', url_kwargs=dict(urn='urn'))

