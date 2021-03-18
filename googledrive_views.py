# File: googledrive_views.py
# Copyright (c) 2018-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.


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
