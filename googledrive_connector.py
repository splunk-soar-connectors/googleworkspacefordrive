# File: googledrive_connector.py
#
# Copyright (c) 2018-2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Phantom App imports
import json
# Fix to add __init__.py to dependencies folder
import os
import sys
import tempfile

import magic
import phantom.app as phantom
import phantom.rules as ph_rules
import phantom.utils as ph_utils
import requests
from google.oauth2 import service_account
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault  # noqa

from googledrive_consts import *

init_path = '{}/dependencies/google/__init__.py'.format(  # noqa
    os.path.dirname(os.path.abspath(__file__))  # noqa
)  # noqa
try:
    open(init_path, 'a+').close()  # noqa
except:  # noqa
    pass  # noqa


# the following argv 'work around' is to keep apiclient happy
# and _also_ debug the connector as a script via pudb
try:
    argv_temp = list(sys.argv)
except:
    pass
sys.argv = ['']

import apiclient  # noqa
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload  # noqa


class RetVal2(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal2, (val1, val2))


class GoogleDriveConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(GoogleDriveConnector, self).__init__()
        self._login_email = None
        self._key_dict = None
        self._domain = None
        self._state = None

    def initialize(self):
        config = self.get_config()
        self._state = self.load_state()
        key_json = config['key_json']
        try:
            key_dict = json.loads(key_json)
        except Exception as e:
            return self.set_status(phantom.APP_ERROR, "Unable to load the key json", e)

        self._key_dict = key_dict

        login_email = config['login_email']

        if (not ph_utils.is_email(login_email)):
            return self.set_status(phantom.APP_ERROR, "Asset config 'login_email' failed validation")

        self._login_email = login_email

        try:
            username, _, self._domain = login_email.partition('@')
        except Exception as e:
            return self.set_status(phantom.APP_ERROR, "Unable to extract domain from login_email", e)

        return phantom.APP_SUCCESS

    def finalize(self):
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _create_service(self, action_result, scopes, api_name, api_version, delegated_user=None):

        # first the credentials
        try:
            credentials = service_account.Credentials.from_service_account_info(self._key_dict, scopes=scopes)
        except Exception as e:
            return RetVal2(action_result.set_status(phantom.APP_ERROR, "Unable to create load the key json", e))

        if (delegated_user):
            try:
                credentials = credentials.with_subject(delegated_user)
            except Exception as e:
                return RetVal2(action_result.set_status(phantom.APP_ERROR, "Failed to create delegated credentials", e), None)

        try:
            service = apiclient.discovery.build(api_name, api_version, credentials=credentials)
        except Exception as e:
            return RetVal2(action_result.set_status(phantom.APP_ERROR,
                "Failed to create service object for API: {0}-{1}. {2} {3}".format(api_name, api_version, str(e),
                    "Please make sure the user '{0}' is valid and the service account has the proper scopes enabled".format(delegated_user)),
                None))

        return RetVal2(phantom.APP_SUCCESS, service)

    def _handle_test_connectivity(self, param):
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(dict(param)))

        scopes = [GOOGLE_SCOPE_USER_READONLY]

        self.save_progress("Creating AdminSDK service object")
        ret_val, service = self._create_service(action_result, scopes, "admin", "directory_v1", config['login_email'])
        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return ret_val

        self.save_progress("Getting list of users for domain: {0}".format(self._domain))
        try:
            service.users().list(domain=self._domain, maxResults=1, orderBy='email', sortOrder="ASCENDING").execute()
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR, "Failed to get users", e)

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_users(self, param):
        config = self.get_config()

        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_USER_READONLY]

        login_email = config['login_email']

        self.save_progress("Querying handle list users")
        ret_val, service = self._create_service(action_result, scopes, "admin", "directory_v1", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        max_users = param.get('max_items', 500)

        kwargs = {'domain': self._domain, 'maxResults': max_users, 'orderBy': 'email', 'sortOrder': 'ASCENDING'}

        page_token = param.get('next_page_token')
        if (page_token):
            kwargs.update({'pageToken': page_token})

        try:
            users_resp = service.users().list(**kwargs).execute()
        except Exception as e:
            error_message = str(e)
            self.debug_print("Exception message: {}".format(error_message))
            return action_result.set_status(phantom.APP_ERROR, "Failed to get users")

        users = users_resp.get('users', [])
        num_users = len(users)
        next_page = users_resp.get('nextPageToken')
        summary = action_result.update_summary({'total_users_returned': num_users})

        for curr_user in users:
            action_result.add_data(curr_user)

        if (next_page):
            summary['next_page_token'] = next_page

        self.save_progress("Handle list users succeeded")
        return action_result.set_status(
            phantom.APP_SUCCESS, 'Successfully retrieved {} user{}'.format(
                num_users, '' if num_users == 1 else 's'
            )
        )

    def _handle_list_files(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_DRIVE_READONLY]

        login_email = param.get('email', self._login_email)
        max_results = int(param.get('max_results', 500))

        self.save_progress("Querying handle list files")
        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        kwargs = {'orderBy': 'name', 'pageSize': max_results, 'fields': LIST_RESP_FIELDS}

        query = param.get('query')
        if (query):
            kwargs.update({'q': query})

        page_token = param.get('next_page_token')
        if (page_token):
            kwargs.update({'pageToken': page_token})

        try:
            resp = service.files().list(**kwargs).execute()
        except Exception as e:
            error_message = str(e)
            self.debug_print("Exception message: {}".format(error_message))
            return action_result.set_status(phantom.APP_ERROR, "Failed to list files")

        for file_obj in resp['files']:
            action_result.add_data(file_obj)

        num_files = len(resp['files'])
        summary = action_result.update_summary({'total_files_returned': num_files})

        next_page = resp.get('nextPageToken')
        if (next_page):
            summary['next_page_token'] = next_page

        self.save_progress("Handle list files succeeded")
        return action_result.set_status(
            phantom.APP_SUCCESS, 'Successfully retrieved {} file{}'.format(
                num_files, '' if num_files == 1 else 's'
            )
        )

    def _get_export_mime_type(self, action_result, service, mime_type, param):
        export_mime_type = param.get('mime_type')
        if export_mime_type:
            return RetVal2(phantom.APP_SUCCESS, export_mime_type)

        export_mime_type = EXPORT_TYPE_MAPPINGS.get(mime_type)
        if export_mime_type:
            return RetVal2(phantom.APP_SUCCESS, export_mime_type)

        try:
            resp = service.about().get(fields='exportFormats').execute()
        except Exception as e:
            return RetVal2(action_result.set_status(phantom.APP_ERROR, "Error getting export MIME types", e))

        return RetVal2(phantom.APP_SUCCESS, resp['exportFormats'][mime_type][0])

    def _save_file_to_vault(self, action_result, service, param, file_metadata):
        file_id = param['id']

        if file_metadata['mimeType'].startswith('application/vnd.google-'):
            # We will need to export this type of file
            ret_val, mime_type = self._get_export_mime_type(action_result, service, file_metadata['mimeType'], param)
            if phantom.is_fail(ret_val):
                return ret_val
            try:
                file_req = service.files().export_media(fileId=file_id, mimeType=mime_type)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Failed to get file", e)
        else:
            # Binary file, just download it
            try:
                file_req = service.files().get_media(fileId=file_id)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Failed to get file", e)

        if hasattr(Vault, 'get_vault_tmp_dir'):
            tmp = tempfile.NamedTemporaryFile(dir=Vault.get_vault_tmp_dir(), delete=False)
        else:
            tmp = tempfile.NamedTemporaryFile(dir="/opt/phantom/vault/tmp/", delete=False)
        downloader = MediaIoBaseDownload(tmp, file_req)
        done = False
        try:
            while done is False:
                status, done = downloader.next_chunk()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error downloading file", e)

        file_name = param.get('file_name') or file_metadata['name']

        success, message, vault_id = ph_rules.vault_add(file_location=tmp.name, container=self.get_container_id(), file_name=file_name)
        if not success:
            return action_result.set_status(
                phantom.APP_ERROR, "Error adding file to vault: {}".format(message)
            )

        action_result.update_summary({
            'vault_id': vault_id
        })

        return phantom.APP_SUCCESS

    def _handle_get_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_DRIVE_READONLY]

        login_email = param.get('email', self._login_email)

        file_id = param['id']

        self.save_progress("Querying handle get file")
        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        try:
            file_metadata = service.files().get(fileId=file_id, fields=ALL_FILE_FIELDS).execute()
        except Exception as e:
            error_message = str(e)
            self.debug_print("Exception message: {}".format(error_message))
            return action_result.set_status(phantom.APP_ERROR, "Failed to get file metadata")

        if param.get('download_file'):
            ret_val = self._save_file_to_vault(
                action_result,
                service,
                param,
                file_metadata
            )
            if phantom.is_fail(ret_val):
                return ret_val

        action_result.add_data(file_metadata)

        self.save_progress("Handle get file succeeded")
        return action_result.set_status(
            phantom.APP_SUCCESS,
            "Successfully retrieved file information{}".format(
                " and added to vault" if param.get('download_file') else ""
            )
        )

    def _convert_mime_types(self, file_metadata, mime_type):
        updated_mime_type = MIME_TYPE_MAPPINGS.get(mime_type)
        if updated_mime_type:
            file_metadata['mimeType'] = updated_mime_type

    def _handle_create_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_DRIVE]

        login_email = param.get('email', self._login_email)

        vault_id = param['vault_id']

        self.save_progress("Querying handle create file")
        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        mime = magic.Magic(mime=True)

        success, message, vault_file_metadata = ph_rules.vault_info(vault_id=vault_id)
        if not success:
            return action_result.set_status(
                phantom.APP_ERROR, "Error fetching the file from vault. Error details: {}".format(message)
            )
        vault_file_metadata = list(vault_file_metadata)[0]

        mime_type = mime.from_file(vault_file_metadata['path'])

        name = param.get('file_name') or vault_file_metadata['name']

        file_metadata = {
            'name': name
        }

        source_mime_type = param.get('source_mime_type')
        if source_mime_type:
            mime_type = source_mime_type

        dest_mime_type = param.get('dest_mime_type')
        if dest_mime_type:
            file_metadata['mimeType'] = dest_mime_type
        elif param.get('convert', True):
            updated_mime_type = MIME_TYPE_MAPPINGS.get(mime_type)
            if updated_mime_type:
                file_metadata['mimeType'] = updated_mime_type

        folder_id = param.get('folder_id')
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(
            vault_file_metadata['path'],
            mimetype=mime_type
        )

        try:
            resp = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id').execute()
        except Exception as e:
            error_message = str(e)
            self.debug_print("Exception message: {}".format(error_message))
            return action_result.set_status(phantom.APP_ERROR, "Error adding file to drive")

        action_result.update_summary({'new_file_id': resp['id']})

        self.save_progress("Handle create file succeeded")
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully added new file to Drive")

    def _handle_create_folder(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_DRIVE]
        login_email = param.get('email', self._login_email)

        self.save_progress("Querying handle create folder")
        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        file_metadata = {
            'name': param['name'],
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder_id = param.get('folder_id')
        if folder_id:
            file_metadata['parents'] = [folder_id]

        try:
            resp = service.files().create(body=file_metadata, fields='id').execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error adding folder to drive", e)

        action_result.update_summary({'new_folder_id': resp['id']})

        self.save_progress("Handle create folder succeeded")
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully added new folder to Drive")

    def _handle_delete_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE_DRIVE]
        login_email = param.get('email', self._login_email)

        file_id = param['id']

        self.save_progress("Querying handle delete file")
        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        try:
            service.files().get(fileId=file_id, fields="id").execute()  # noqa
        except Exception:
            return action_result.set_status(phantom.APP_SUCCESS, "File doesn't exist or has already been deleted")

        try:
            resp = service.files().delete(fileId=file_id).execute()  # noqa
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error deleting file", e)

        self.save_progress("Handle delete file succeeded")
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted file from Drive")

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_users':
            ret_val = self._handle_list_users(param)

        elif action_id == 'list_files':
            ret_val = self._handle_list_files(param)

        elif action_id == 'get_file':
            ret_val = self._handle_get_file(param)

        elif action_id == 'create_file':
            ret_val = self._handle_create_file(param)

        elif action_id == 'create_folder':
            ret_val = self._handle_create_folder(param)

        elif action_id == 'delete_file':
            ret_val = self._handle_delete_file(param)

        return ret_val


if __name__ == '__main__':

    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)
    argparser.add_argument('-v', '--verify', action='store_true', help='verify', required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        login_url = BaseConnector._get_phantom_base_url() + "login"
        try:
            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=DEFAULT_REQUEST_TIMEOUT)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platfrom. Error: {}".format(str(e)))
            sys.exit(1)

    if (len(sys.argv) < 2):
        print("No test json specified as input")
        sys.exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GoogleDriveConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
