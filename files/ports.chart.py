# -*- coding: utf-8 -*-
from collections import namedtuple
import re
from bases.FrameworkServices.ExecutableService import ExecutableService

# default module values (can be overridden per job in `config`)
# update_every = 2
priority = 60000
retries = 60
# set command: "/bin/false" in config to disable

# list of chart ids
ORDER = ['ports']

CHARTS = {
    # id -> {options: [], lines: [[]]}
    'ports': {
        # [name, title, units, family, context, charttype],
        'options': [None, "Current open tcp4 ports", "ports", "ports", "ports.open", "line"],
        'lines': [
                ['22', '22', 'absolute'],
        ]
    }
}

class Service(ExecutableService):
    def __init__(self, configuration=None, name=None):
        ExecutableService.__init__(self, configuration=configuration, name=name)
        self.command = ['netstat', '-tnpl4']
        self.order = ORDER
        self.definitions = CHARTS
        # conf access: self.configuration.get('host', '127.0.0.1')
    def check(self):
        return True

    def _get_data(self):
        """
        returns dict {unique_dimention_name -> value} or None
        """
        raw_data = self._get_raw_data()
        if not raw_data:
            return None
        result = {}
        for line in raw_data:
            if 'tcp' in line:
                parts = line.split()
                proto = parts[0]
                local_addr = parts[3]
                state = parts[5]
                ip, port = local_addr.rsplit(':', 1)
                port = str(port)
                result[port] = 1
                if state == 'LISTEN':
                    if port not in self.charts['ports']:
                        self.charts['ports'].add_dimension([port, port, 'absolute'])
        return result
