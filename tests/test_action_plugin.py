import os
from mock import MagicMock
from yaml import load

from action_plugins.merge_vars import ActionModule


with open(os.path.join(os.path.dirname(__file__), 'data.yaml'), 'r') as file_obj:
    data = load(file_obj)


def test_run():
    mocked_module = MagicMock()
    mocked_module.main_vars = 'couchdb_auction.content'
    mocked_module.recursive = False
    mocked_module.load_found_files = MagicMock(return_value=data)
    mocked_module.data_store = MagicMock()
    mocked_module.data_store.update = MagicMock(side_effect=Exception())
    try:
        ActionModule.run(mocked_module)
    except:
        assert data['couchdb_auction']['content'] == {
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
