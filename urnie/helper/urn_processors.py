VALUE_PROCESS_FLAG = ('%v', 'Insert parameter as-is', lambda x, y: x.replace('%v', y))


def substitute(url: str, val: str):
    return url.replace('%v', val)


def process_urn_url(url, urn_param):
    if not url:
        return url
    for processor in get_processors():
        url = processor[2](url, urn_param)
    return url


def get_processors():
    return [
        VALUE_PROCESS_FLAG
    ]
