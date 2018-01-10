# --
# File: googledrive_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault  # noqa
import phantom.utils as ph_utils

from googledrive_consts import *

import magic
import tempfile
import requests

# Fix to add __init__.py to dependencies folder
import os
init_path = '{}/dependencies/google/__init__.py'.format(  # noqa
    os.path.dirname(os.path.abspath(__file__))  # noqa
)  # noqa
try:
    open(init_path, 'a+').close()  # noqa
except:  # noqa
    pass  # noqa


import json
import sys

from google.oauth2 import service_account


# the following argv 'work around' is to keep apiclient happy
# and _also_ debug the connector as a script via pudb
try:
    argv_temp = list(sys.argv)
except:
    pass
sys.argv = ['']

import apiclient  # noqa
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload  # noqa


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
            return self.set_status(phantom.APP_ERROR, "Unable to extract domain from login_email")

        return phantom.APP_SUCCESS

    def finalize(self):
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _create_service(self, action_result, scopes, api_name, api_version, delegated_user=None):

        # if delegated_user is None:
        #     delegated_user = self._login_email

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
                    "Please make sure the user '{0}' is valid and the service account has the proper scopes enabled.".format(delegated_user)),
                None))

        return RetVal2(phantom.APP_SUCCESS, service)

    def _handle_test_connectivity(self, param):
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(dict(param)))

        scopes = ['https://www.googleapis.com/auth/admin.directory.user']

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
            return action_result.set_status(phantom.APP_ERROR, "Failed to get users.", e)

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_users(self, param):
        config = self.get_config()

        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = ['https://www.googleapis.com/auth/admin.directory.user']

        login_email = config['login_email']

        ret_val, service = self._create_service(action_result, scopes, "admin", "directory_v1", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        max_users = param.get('max_items', 500)

        kwargs = {'domain': self._domain, 'maxResults': max_users, 'orderBy': 'email', 'sortOrder': 'ASCENDING'}

        page_token = param.get('page_token')
        if (page_token):
            kwargs.update({'pageToken': page_token})

        try:
            users_resp = service.users().list(**kwargs).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Failed to get users.", e)

        users = users_resp.get('users', [])
        num_users = len(users)
        next_page = users_resp.get('nextPageToken')
        summary = action_result.update_summary({'total_users_returned': num_users})

        for curr_user in users:
            action_result.add_data(curr_user)

        if (next_page):
            summary['next_page_token'] = next_page

        return action_result.set_status(
            phantom.APP_SUCCESS, 'Successfully retrieved {} user{}'.format(
                num_users, 's' if num_users > 1 else ''
            )
        )

    def _handle_list_files(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = ['https://www.googleapis.com/auth/drive']

        login_email = param.get('email', self._login_email)
        max_results = int(param.get('max_results', 500))

        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        kwargs = {'orderBy': 'name', 'pageSize': max_results, 'fields': LIST_RESP_FIELDS}

        page_token = param.get('page_token')
        if (page_token):
            kwargs.update({'pageToken': page_token})

        try:
            resp = service.files().list(**kwargs).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Failed to list files", e)

        for file_obj in resp['files']:
            action_result.add_data(file_obj)

        num_files = len(resp['files'])
        summary = action_result.update_summary({'total_files_returned': num_files})

        next_page = resp.get('nextPageToken')
        if (next_page):
            summary['next_page_token'] = next_page

        return action_result.set_status(
            phantom.APP_SUCCESS, 'Successfully retrieved {} file{}'.format(
                num_files, 's' if num_files > 1 else ''
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

    def _handle_get_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = ['https://www.googleapis.com/auth/drive']

        login_email = param.get('email', self._login_email)

        file_id = param['id']

        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        try:
            file_metadata = service.files().get(fileId=file_id, fields=ALL_FILE_FIELDS).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Failed to get file", e)

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

        tmp = tempfile.NamedTemporaryFile(dir="/opt/phantom/vault/tmp/", delete=False)
        downloader = MediaIoBaseDownload(tmp, file_req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        file_name = param.get('file_name') or file_metadata['name']

        resp = Vault.add_attachment(tmp.name, self.get_container_id(), file_name=file_name)
        if not resp['succeeded']:
            return action_result.set_status(
                phantom.APP_ERROR, "Error adding file to vault: {}".format(resp['message'])
            )

        action_result.update_summary({
            'vault_id': resp['vault_id']
        })
        action_result.add_data(file_metadata)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved file and added to vault")

    def _convert_mime_types(self, file_metadata, mime_type):
        updated_mime_type = MIME_TYPE_MAPPINGS.get(mime_type)
        if updated_mime_type:
            file_metadata['mimeType'] = updated_mime_type

    def _handle_create_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = ['https://www.googleapis.com/auth/drive']

        login_email = param.get('email', self._login_email)

        vault_id = param['vault_id']

        ret_val, service = self._create_service(action_result, scopes, "drive", "v3", login_email)
        if phantom.is_fail(ret_val):
            return ret_val

        mime = magic.Magic(mime=True)

        vault_file_metadata = Vault.get_file_info(vault_id=vault_id)[0]

        mime_type = mime.from_file(vault_file_metadata['path'])

        file_metadata = {
            'name': vault_file_metadata['name']
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
            return action_result.set_status(phantom.APP_ERROR, "Error adding file to drive", e)

        action_result.update_summary({'new_file_id': resp['id']})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully added new file to Drive")

    def _handle_delete_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = ['https://www.googleapis.com/auth/drive']
        login_email = param.get('email', self._login_email)

        file_id = param['id']

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

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully delete file from Drive")

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

        elif action_id == 'delete_file':
            ret_val = self._handle_delete_file(param)

        return ret_val


if __name__ == '__main__':

    import sys
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            print ("Accessing the Login page")
            r = requests.get("https://127.0.0.1/login", verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = 'https://127.0.0.1/login'

            print ("Logging into Platform to get the session id")
            r2 = requests.post("https://127.0.0.1/login", verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GoogleDriveConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
