from flask_table import Table, Col


class UrnResults(Table):
    id = Col('Id', show=False)
    urn = Col('URN')
    url = Col('URL')
    approved = Col('Approved')
    date_added = Col('Date Added')
