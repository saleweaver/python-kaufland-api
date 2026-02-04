import functools
import re
from urllib.parse import quote


def kaufland_endpoint(path, method="GET"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs["path"] = path
            kwargs["_method"] = str(method).upper()
            return func(*args, **kwargs)

        wrapper.path = path
        wrapper.method = str(method).upper()
        return wrapper

    return decorator


def fill_query_params(path, *args, **kwargs):
    if kwargs:
        for name, value in kwargs.items():
            placeholder = "{" + name + "}"
            if placeholder in path:
                path = path.replace(placeholder, quote(str(value), safe=""))

    for value in args:
        if "{}" in path:
            path = path.replace("{}", quote(str(value), safe=""), 1)
            continue
        match = re.search(r"{[^}]+}", path)
        if not match:
            break
        path = path.replace(match.group(0), quote(str(value), safe=""), 1)

    return path
