import datetime
import json
from yattag import Doc


def generate_export_json(urns):
    '''
    Generates a JSON export of the supplied URNs.
    :param urns:
    :return:
    '''
    urn_json = {
        "title": "urns",
        "generated": str(datetime.datetime.now().timestamp()),
    }
    children = [{
        "urn": urn["urn"],
        "url": urn["url"],
        "dateAdded": str(urn["date_added"].timestamp())
    } for urn in urns]
    urn_json["children"] = children
    return json.dumps(urn_json, sort_keys=True, indent=4)


def generate_export_html(urns):
    '''
    Generates a HTML export of the supplied URNs.
    :param urns:
    :return:
    '''

    doc, tag, text = Doc(
        defaults={
            'title': 'Urns',
        }
    ).tagtext()
    doc.line('h1', 'Urns')
    with tag('dl'):
        with tag('p'):
            for urn in urns:
                with tag('dt'):
                    with tag('a', href=urn["url"], date_added=str(urn["date_added"].timestamp())):
                        text(urn["urn"])
    return doc.getvalue()
