[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2018-2023 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
### Service Account

This app requires a pre-configured service account to operate. Please follow the procedure outlined
at [this link](https://support.google.com/a/answer/7378726?hl=en) to create a service account.  
The following APIs will need to be enabled:

-   AdminSDK
-   Drive API

At the end of the creation process, the admin console should ask you to save the config as a JSON
file. Copy the contents of the JSON file in the clipboard and paste it as the value of the "Contents
of Service Account JSON file" asset configuration parameter.

### Scopes

Once the service account has been created and APIs enabled, the next step is to configure scopes on
these APIs to allow the App to access them. Every action requires different scopes to operate, these
are listed in the action documentation.  
To enable scopes please complete the following steps:

-   Go to your G Suite domain's [Admin console.](http://admin.google.com/)
-   Select **Security** from the list of controls. If you don't see **Security** listed, select
    **Show More** , then select **Security** from the list of controls. If you can't see the
    controls, make sure you're signed in as an administrator for the domain.
-   Select **API controls** in the **Access and data control** section.
-   Select **MANAGE DOMAIN WIDE DELEGATIONS** in the **Domain wide delegation** section.
-   Select **Add new** in the API clients section
-   In the **Client Name** field enter the service account's **Client ID** . You can find your
    service account's client ID in the [Service accounts credentials
    page](https://console.developers.google.com/apis/credentials) or the service account JSON file
    (key named **client_id** ).
-   In the **One or More API Scopes** field enter the list of scopes that you wish to grant access
    to the App. For example, to enable all the scopes required by this app enter:
    https://www.googleapis.com/auth/admin.directory.user.readonly,
    https://www.googleapis.com/auth/drive.readonly, https://www.googleapis.com/auth/drive
-   Click **Authorize** .

### MIME Types

Both **upload file** and **get file** support specifying MIME types in their parameters. While these
are optional, they can be used to convert files when importing/exporting to Drive. For example, if
you are adding an Excel file to Drive, you can specify the **source_mime_type** to be
**application/vnd.ms-excel** and **dest_mime_type** to be
**application/vnd.google-apps.spreadsheet** (this is the type of Google's Sheet files). This will
convert the Excel file, and make it editable in Drive. In the case where the **source_mime_type** is
not supplied, the app will attempt to deduce the correct MIME type of the added file, though
**source_mime_type** can be used to fix any errors. For example, a JSON file would automatically be
assigned the MIME type of **text/plain** , as opposed to **application/json** .

When downloading a file from Drive, the same thing applies. When attempting to download a file which
is native to Drive (Sheet, Doc, Slide), the app will export their Microsoft Office equivalents
(Excel, Word, PowerPoint). By specifying the **mime_type** you can change this behavior. For
example, setting it to **text/csv** will cause a Sheet file to export to a CSV file, as opposed to
Excel.

A full list of Google Drive's own MIME types can be found at this link:
<https://developers.google.com/drive/v3/web/mime-types>

The list files action would return only 460 files at a time. The next token can be used to fetch more files.