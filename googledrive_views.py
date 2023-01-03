# File: googledrive_views.py
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
def list_users(provides, all_results, context):

    context['results'] = results = []

    headers = ['Status', 'Full Name', 'Email']
    context['headers'] = headers

    for summary, action_results in all_results:
        for result in action_results:
            table = dict()
            table['data'] = rows = []
            data = result.get_data()

            result_status = 'failed'
            if result.get_status():
                result_status = 'success'

            for item in data:
                row = []
                row.append({'value': result_status})
                row.append({'value': item.get('name', {}).get('fullName')})
                row.append({'value': item.get('primaryEmail'), 'contains': ['email']})
                rows.append(row)
            results.append(table)

    return 'googledrive_list_users.html'
