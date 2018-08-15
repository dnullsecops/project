import os
from yaml import load
from copy import deepcopy
from utils import get_item, merge_dicts, merge


with open(os.path.join(os.path.dirname(__file__), 'data.yaml'), 'r') as file_obj:
    data = load(file_obj)


def test_get_item():
    source = {
        'data': {
            'value': {
                'amount': 42
            }
        }
    }
    path = 'data.value.amount'

    assert get_item(source, path) == 42


def test_merge_dicts():
    source = {
        'a': 0,
        'b': 1,
        'c': {
            'd': 2,
            'e': 3,
        },
        'f': {
            'g': 4,
            'h': 5
        }
    }

    merge_with = {
        'a': 1,
        'j': 6,
        'c': {
            'd': 7,
            'k': 8
        },
        '$test': 'shouldn\'t'
    }

    expected = {
        'a': 0,
        'b': 1,
        'c': {
            'd': 2,
            'e': 3,
            'k': 8
        },
        'f': {
            'g': 4,
            'h': 5
        },
        'j': 6
    }

    merge_dicts(source, merge_with)
    assert source == expected
    assert '$test' not in source


def test_merge():
    test_data = deepcopy(data)
    merge(test_data, 'couchdb_auction.content')
    assert test_data['couchdb_auction']['content'] == {
        '$include': ['couchdb.content', 'logger.content'],
        'httpd': {
            'port': 5990,
            'host': 'localhost',
            'user': 'auction_admin',
            'pass': 'auction_admin_pass'
        },
        'auth': False,
        'logger_crit': {
            'handler': 'journald'
        }
    }

    test_data = deepcopy(data)
    merge(test_data, 'couchdb_auction.content', recursive=True)
    assert test_data['couchdb_auction']['content'] == {
        '$include': ['couchdb.content', 'logger.content'],
        'httpd': {
            'port': 5990,
            'host': 'localhost',
            'user': 'auction_admin',
            'pass': 'auction_admin_pass'
        },
        'auth': False,
        'logger_crit': {
            'handler': 'journald'
        },
        'user': 'default_admin',
        'pass': 'default_admin_pass'
    }
