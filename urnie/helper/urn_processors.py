import shlex
from typing import List

VALUE_PROCESS_FLAG = ('%v', 'Insert parameter as-is', lambda x, y: x.replace('%v', y))
JQL_PROCESS_FLAG = ('%j', 'Translate to JQL text search', lambda x, y: jira_textsearch(x, shlex.split(y)))


def substitute(url: str, val: str):
    return url.replace('%v', val)


def jira_textsearch(url: str, val: List[str]):
    search_term = ''
    for term in val:
        if search_term != '':
            search_term += ' AND '
        search_term += f'(text ~ "{term}" OR comment ~ "{term}")'
    return url.replace('%j', search_term)


def process_urn_url(url, urn_param):
    if not url:
        return url
    for processor in get_processors():
        url = processor[2](url, urn_param)
    return url


def get_processors():
    return [
        VALUE_PROCESS_FLAG,
        JQL_PROCESS_FLAG
    ]
