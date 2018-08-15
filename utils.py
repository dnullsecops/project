from copy import deepcopy
from dpath.util import get as get_item
from functools import partial

get_item = partial(get_item, separator='.')


def merge(source, main_vars, recursive=False):
    to_merge = get_item(source, main_vars)
    include = to_merge.get('$include')
    
    if include:
        for i in include:
            if recursive:
                merge(source, i, recursive)
            part = get_item(source, i)
            merge_dicts(to_merge, part)


def merge_dicts(source, merge_with):
    for k, v in merge_with.items():
        if k.startswith('$'):
            continue
        if not k in source:
            source[k] = v
        elif isinstance(v, dict):
            merge_dicts(source[k], v)
