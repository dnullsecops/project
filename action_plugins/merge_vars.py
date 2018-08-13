# (c) 2016, Allen Sanabria <asanabria@linuxdynasty.org>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import yaml
import json
import dpath.util
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.utils.vars import combine_vars
from ansible.module_utils._text import to_text
import glob
from os import path, walk, getcwd, listdir

VALID_FILE_EXTENSIONS = ['yaml', 'yml']
class ActionModule(ActionBase):

    def _set_args(self):
        self.lookup_vars_dir = self._task.args.get('lookup_vars_dir')
        self.main_vars = self._task.args.get('main_vars')
        self.merge_with = self._task.args.get('merge_with')
        self.valid_extensions = self._task.args.get('valid_extensions', VALID_FILE_EXTENSIONS)
        self.show_content = self._task.args.get('shown_content', True)
        self.recursive = self._task.args.get('recursive', False)
        # self.changed = self._task.args.get('changed', False)
        self.data_store = {}

    def get_root_dir(self, vars_dir):
        if vars_dir.split('/') == 'vars':
            path_to_use = path.join(vars_dir)
            if path.exists(path_to_use):
                vars_dir = path_to_use
        else:
            current_dir = getcwd()
            path_to_use = path.join(current_dir, vars_dir)
            vars_dir = path_to_use
        return vars_dir

    def valid_file(self, file, root_dir):
        # NOT WORKING
        if not file.startswith(u'.') and not file.endswith(u'~'):
            full_filepath = path.join(root_dir, file)
            if path.isfile(full_filepath):
                ext = path.splitext(file)[-1]
                if not ext or to_text(ext) in self.valid_extensions:
                    return True
            else:
                return False

    def find_files(self, root_dir, recursive=False):
        found_files = []
        # if recursive:
        for root, dirs, files in walk(root_dir):
            for ffile in files:
                # if self.valid_file(ffile, root):
                found_files.append(path.join(root, ffile))
        # else:
            # for ffile in listdir(root_dir):
            #     if self.valid_file(ffile, root_dir):
            #         found_files.append(ffile)
        return found_files

    def load_found_files(self, found_files):
        results = {}
        for found in found_files:
            new_data = self._loader.load_from_file(found, cache=True, unsafe=True)
            if new_data:  # ignore empty files
                results = combine_vars(results, new_data)
        return results


    def merge(self, main_vars, merge_with, data_store):
        # merge_with = list of str
        source_vars = dpath.util.get(data_store, main_vars) # dict

        for merge_vars in merge_with:
            self.merge_recursive(source_vars, merge_vars, data_store)
        return main_vars

    def merge_recursive(self, main_vars, merge_vars, data_store):
        if merge_vars:
            parent_include = dpath.util.get(data_store, "{0}.include".format(merge_vars), separator='.')
            parent_content = dpath.util.get(data_store, merge_vars, separator='.')
            self.merge_content(main_vars, parent_content)
            if parent_content:
                self.merge_recursive(parent_include, data_store, source_content)
        return source_content

    def merge_content(self, source_content, parent_content):
        dpath.util.merge(parent_content, source_content, flags=2)
        source_content.update(parent_content)
        return source_content



    def run(self, tmp=None, task_vars=None):
        failed = False
        merged_dict = dict()

        self._set_args()
        root_dir = self.get_root_dir(self.lookup_vars_dir)
        found_files = self.find_files(root_dir)
        # found_files = ['/home/shellshock/run/default_vars/couchdb.yml', '/home/shellshock/run/default_vars/couchdb_auction.yml']
        self.data_store.update(self.load_found_files(found_files))
        if self.data_store:
            merged_dict.update(self.merge(self.main_vars, self.data_store))
        # if failed:
        #     result['failed'] = failed
        #     result['message'] = err_msg

        result = super(ActionModule, self).run(task_vars=task_vars)
        result['ansible_included_var_files'] = found_files
        result['ansible_facts'] = self.data_store
        result['_ansible_no_log'] = not self.show_content
        # result['changed'] = self.changed

        return result


    # def _set_root_dir(self):
    #     if self._task._role:
    #         if self.lookup_vars_dir.split('/')[0] == 'vars':
    #             path_to_use = (
    #                 path.join(self._task._role._role_path, self.lookup_vars_dir)
    #             )
    #             if path.exists(path_to_use):
    #                 self.lookup_vars_dir = path_to_use
    #         else:
    #             path_to_use = (
    #                 path.join(
    #                     self._task._role._role_path, 'vars', self.lookup_vars_dir
    #                 )
    #             )
    #             self.lookup_vars_dir = path_to_use
    #     else:
    #         current_dir = (
    #             "/".join(self._task._ds._data_source.split('/')[:-1])
    #         )
    #         self.lookup_vars_dir = path.join(current_dir, self.lookup_vars_dir)


# if __name__ == "__main__":
#     source_name = 'couchdb_auction'
#
#     def merge_recursive(include, data_store, source_content):
#         if include:
#             parent_include = dpath.util.get(data_store, include+'.include', separator='.')
#             parent_content = dpath.util.get(data_store, include+'.content', separator='.')
#             merge_content(source_content, parent_content)
#             if parent_content:
#                 merge_recursive(parent_include, data_store, source_content)
#
#
#     def merge_content(source_content, parent_content):
#             print(type(parent_content))
#             # parent_content = dpath.util.get(parent, '/content')
#             print("PARENT", json.dumps(parent_content, indent=4))
#             print("SOURCE", json.dumps(source_content, indent=4))
#             dpath.util.merge(parent_content, source_content, flags=2)
#             source_content.update(parent_content)
#             print("RESOURCE", json.dumps(source_content, indent=4))
#
#     def merge(source, data_store):
#         source_content  = dpath.util.get(source, '/template/{0}/content'.format(source_name))
#         source_includes = dpath.util.get(source, '/template/{0}/include'.format(source_name))
#
#         for include in source_includes:
#             merge_recursive(include, data_store, source_content)
#
#     with open("/home/shellshock/run/default_vars/{0}.yml".format(source_name), 'r') as couchdb_auction_stream:
#         source = yaml.load(couchdb_auction_stream)
#
#     with open("/home/shellshock/run/default_vars/couchdb.yml", 'r') as couchdb_stream:
#         data_store = yaml.load(couchdb_stream)
#
#     merge(source, data_store)
