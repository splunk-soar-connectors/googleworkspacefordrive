[comment]: # "Auto-generated SOAR connector documentation"
# G Suite for Drive

Publisher: Splunk  
Connector Version: 2\.0\.20  
Product Vendor: Google  
Product Name: Google Drive  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This app allows various file manipulation actions to be performed on Google Drive

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2018-2022 Splunk Inc."
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

-   Go to your G Suite domain’s [Admin console.](http://admin.google.com/)
-   Select **Security** from the list of controls. If you don't see **Security** listed, select
    **More controls** from the gray bar at the bottom of the page, then select **Security** from the
    list of controls. If you can't see the controls, make sure you're signed in as an administrator
    for the domain.
-   Select **Show more** and then **Advanced settings** from the list of options.
-   Select **Manage API client access** in the **Authentication** section.
-   In the **Client Name** field enter the service account's **Client ID** . You can find your
    service account's client ID in the [Service accounts
    page](https://console.developers.google.com/permissions/serviceaccounts) or in the service
    account JSON file (key named **client_id** ).
-   In the **One or More API Scopes** field enter the list of scopes that you wish to grant access
    to the App. For example, to enable all the scopes required by this app enter:
    https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/drive
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


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Google Drive asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**login\_email** |  required  | string | Login \(Admin\) email
**key\_json** |  required  | password | Contents of Service Account JSON file

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list users](#action-list-users) - Get the list of users  
[delete file](#action-delete-file) - Delete a file  
[create folder](#action-create-folder) - Create a new folder  
[upload file](#action-upload-file) - Upload a file from the Vault to Drive  
[get file](#action-get-file) - Get information about a file or download it to the Vault  
[list files](#action-list-files) - Get the list of files  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list users'
Get the list of users

Type: **investigate**  
Read only: **True**

Action uses the Admin SDK API to get a list of users\. Requires authorization with the following scope\:<ul><li>https\://www\.googleapis\.com/auth/admin\.directory\.user</li></ul><br>The action will limit the number of users returned to <b>max\_items</b> or \(if not specified\) 500\. If the system has any more users, a next page token will be returned in <b>action\_result\.summary\.next\_page\_token</b>\. Use this value as input to <b>next\_page\_token</b> in subsequent calls to <b>list users</b>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**max\_items** |  optional  | Maximum number of users to return | numeric | 
**next\_page\_token** |  optional  | Next Page Token | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.max\_items | numeric | 
action\_result\.parameter\.next\_page\_token | string | 
action\_result\.data\.\*\.agreedToTerms | boolean | 
action\_result\.data\.\*\.archived | boolean | 
action\_result\.data\.\*\.changePasswordAtNextLogin | boolean | 
action\_result\.data\.\*\.creationTime | string | 
action\_result\.data\.\*\.customerId | string | 
action\_result\.data\.\*\.emails\.\*\.address | string |  `email` 
action\_result\.data\.\*\.emails\.\*\.primary | boolean | 
action\_result\.data\.\*\.emails\.\*\.type | string | 
action\_result\.data\.\*\.etag | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.includeInGlobalAddressList | boolean | 
action\_result\.data\.\*\.ipWhitelisted | boolean | 
action\_result\.data\.\*\.isAdmin | boolean | 
action\_result\.data\.\*\.isDelegatedAdmin | boolean | 
action\_result\.data\.\*\.isEnforcedIn2Sv | boolean | 
action\_result\.data\.\*\.isEnrolledIn2Sv | boolean | 
action\_result\.data\.\*\.isMailboxSetup | boolean | 
action\_result\.data\.\*\.kind | string | 
action\_result\.data\.\*\.lastLoginTime | string | 
action\_result\.data\.\*\.name\.familyName | string | 
action\_result\.data\.\*\.name\.fullName | string | 
action\_result\.data\.\*\.name\.givenName | string | 
action\_result\.data\.\*\.nonEditableAliases | string |  `email` 
action\_result\.data\.\*\.orgUnitPath | string | 
action\_result\.data\.\*\.phones\.\*\.type | string | 
action\_result\.data\.\*\.phones\.\*\.value | string | 
action\_result\.data\.\*\.primaryEmail | string |  `email` 
action\_result\.data\.\*\.recoveryEmail | string | 
action\_result\.data\.\*\.suspended | boolean | 
action\_result\.summary\.next\_page\_token | string | 
action\_result\.summary\.total\_users\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete file'
Delete a file

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email \(use this drive\) | string |  `email` 
**id** |  required  | File ID | string |  `drive file id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.id | string |  `drive file id` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create folder'
Create a new folder

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email \(use this drive\) | string |  `email` 
**name** |  required  | Name of the new folder | string | 
**folder\_id** |  optional  | ID of the parent folder | string |  `drive file id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.folder\_id | string |  `drive file id` 
action\_result\.parameter\.name | string | 
action\_result\.data | string | 
action\_result\.summary\.new\_folder\_id | string |  `drive file id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'upload file'
Upload a file from the Vault to Drive

Type: **generic**  
Read only: **False**

If the Drive API does not support the conversion from the files original MIME type to <b>dest\_mime\_type</b>, the uploaded file will become a native Google Drive type \(e\.g\. a Google document\)\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email \(use this drive\) | string |  `email` 
**vault\_id** |  required  | Vault ID | string |  `vault id`  `sha1` 
**source\_mime\_type** |  optional  | MIME type of file in vault | string |  `mime type` 
**dest\_mime\_type** |  optional  | MIME type of new Drive file \(will disable convert\) | string |  `mime type` 
**folder\_id** |  optional  | ID of the parent folder | string |  `drive file id` 
**file\_name** |  optional  | Set the file name in Drive | string | 
**convert** |  optional  | Attempt to convert file to native Drive type\. Will only have an effect if dest\_mime\_type is not set | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.convert | boolean | 
action\_result\.parameter\.dest\_mime\_type | string |  `mime type` 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.file\_name | string | 
action\_result\.parameter\.folder\_id | string |  `drive file id` 
action\_result\.parameter\.source\_mime\_type | string |  `mime type` 
action\_result\.parameter\.vault\_id | string |  `vault id`  `sha1` 
action\_result\.data | string | 
action\_result\.summary\.new\_file\_id | string |  `drive file id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get file'
Get information about a file or download it to the Vault

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email \(use this drive\) | string |  `email` 
**id** |  required  | File ID | string |  `drive file id` 
**download\_file** |  optional  | Download the file to the Vault | boolean | 
**mime\_type** |  optional  | MIME Type for exported file\. This will only have an effect if the original document is file type that needs to be exported \(i\.e\. Google Docs / Sheets / Slides files\) | string |  `mime type` 
**file\_name** |  optional  | Set a new name for the file before adding it to the vault | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.download\_file | boolean | 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.file\_name | string | 
action\_result\.parameter\.id | string |  `drive file id` 
action\_result\.parameter\.mime\_type | string |  `mime type` 
action\_result\.data\.\*\.capabilities\.canAddChildren | boolean | 
action\_result\.data\.\*\.capabilities\.canAddMyDriveParent | boolean | 
action\_result\.data\.\*\.capabilities\.canChangeCopyRequiresWriterPermission | boolean | 
action\_result\.data\.\*\.capabilities\.canChangeViewersCanCopyContent | boolean | 
action\_result\.data\.\*\.capabilities\.canComment | boolean | 
action\_result\.data\.\*\.capabilities\.canCopy | boolean | 
action\_result\.data\.\*\.capabilities\.canDelete | boolean | 
action\_result\.data\.\*\.capabilities\.canDownload | boolean | 
action\_result\.data\.\*\.capabilities\.canEdit | boolean | 
action\_result\.data\.\*\.capabilities\.canListChildren | boolean | 
action\_result\.data\.\*\.capabilities\.canModifyContent | boolean | 
action\_result\.data\.\*\.capabilities\.canMoveChildrenWithinDrive | boolean | 
action\_result\.data\.\*\.capabilities\.canMoveItemIntoTeamDrive | boolean | 
action\_result\.data\.\*\.capabilities\.canMoveItemOutOfDrive | boolean | 
action\_result\.data\.\*\.capabilities\.canMoveItemWithinDrive | boolean | 
action\_result\.data\.\*\.capabilities\.canReadRevisions | boolean | 
action\_result\.data\.\*\.capabilities\.canRemoveChildren | boolean | 
action\_result\.data\.\*\.capabilities\.canRemoveMyDriveParent | boolean | 
action\_result\.data\.\*\.capabilities\.canRename | boolean | 
action\_result\.data\.\*\.capabilities\.canShare | boolean | 
action\_result\.data\.\*\.capabilities\.canTrash | boolean | 
action\_result\.data\.\*\.capabilities\.canUntrash | boolean | 
action\_result\.data\.\*\.createdTime | string | 
action\_result\.data\.\*\.explicitlyTrashed | boolean | 
action\_result\.data\.\*\.fileExtension | string | 
action\_result\.data\.\*\.fullFileExtension | string | 
action\_result\.data\.\*\.hasThumbnail | boolean | 
action\_result\.data\.\*\.headRevisionId | string | 
action\_result\.data\.\*\.iconLink | string |  `url` 
action\_result\.data\.\*\.id | string |  `drive file id` 
action\_result\.data\.\*\.isAppAuthorized | boolean | 
action\_result\.data\.\*\.kind | string | 
action\_result\.data\.\*\.lastModifyingUser\.displayName | string | 
action\_result\.data\.\*\.lastModifyingUser\.emailAddress | string |  `email` 
action\_result\.data\.\*\.lastModifyingUser\.kind | string | 
action\_result\.data\.\*\.lastModifyingUser\.me | boolean | 
action\_result\.data\.\*\.lastModifyingUser\.permissionId | string | 
action\_result\.data\.\*\.md5Checksum | string |  `md5` 
action\_result\.data\.\*\.mimeType | string |  `mime type` 
action\_result\.data\.\*\.modifiedByMe | boolean | 
action\_result\.data\.\*\.modifiedByMeTime | string | 
action\_result\.data\.\*\.modifiedTime | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.originalFilename | string | 
action\_result\.data\.\*\.ownedByMe | boolean | 
action\_result\.data\.\*\.owners\.\*\.displayName | string | 
action\_result\.data\.\*\.owners\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.owners\.\*\.kind | string | 
action\_result\.data\.\*\.owners\.\*\.me | boolean | 
action\_result\.data\.\*\.owners\.\*\.permissionId | string | 
action\_result\.data\.\*\.parents | string | 
action\_result\.data\.\*\.permissionIds | string | 
action\_result\.data\.\*\.permissions\.\*\.deleted | boolean | 
action\_result\.data\.\*\.permissions\.\*\.displayName | string | 
action\_result\.data\.\*\.permissions\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.permissions\.\*\.id | string | 
action\_result\.data\.\*\.permissions\.\*\.kind | string | 
action\_result\.data\.\*\.permissions\.\*\.role | string | 
action\_result\.data\.\*\.permissions\.\*\.type | string | 
action\_result\.data\.\*\.quotaBytesUsed | string | 
action\_result\.data\.\*\.shared | boolean | 
action\_result\.data\.\*\.size | string | 
action\_result\.data\.\*\.spaces | string | 
action\_result\.data\.\*\.starred | boolean | 
action\_result\.data\.\*\.thumbnailLink | string |  `url` 
action\_result\.data\.\*\.thumbnailVersion | string | 
action\_result\.data\.\*\.trashed | boolean | 
action\_result\.data\.\*\.version | string | 
action\_result\.data\.\*\.viewedByMe | boolean | 
action\_result\.data\.\*\.viewedByMeTime | string | 
action\_result\.data\.\*\.viewersCanCopyContent | boolean | 
action\_result\.data\.\*\.webContentLink | string |  `url` 
action\_result\.data\.\*\.webViewLink | string |  `url` 
action\_result\.data\.\*\.writersCanShare | boolean | 
action\_result\.summary\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list files'
Get the list of files

Type: **investigate**  
Read only: **True**

You can use the <b>query</b> parameter to filter the results\. The full documentation on this parameter can be read <a href="https\://developers\.google\.com/drive/v3/web/search\-parameters">here</a>\. Here are some examples\:<ul><li><b>mimeType='application/vnd\.google\-apps\.folder'</b>\: show only folders</li><li><b>modifiedTime > '2018\-01\-05T12\:00\:00' and mimeType='application/vnd\.google\-apps\.document'</b>\: Show only documents which have been modified since the date</li></ul>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email \(use this drive\) | string |  `email` 
**max\_results** |  optional  | Max Results | numeric | 
**next\_page\_token** |  optional  | Next Page Token | string | 
**query** |  optional  | Query | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.parameter\.next\_page\_token | string | 
action\_result\.parameter\.query | string | 
action\_result\.data\.\*\.id | string |  `drive file id` 
action\_result\.data\.\*\.kind | string | 
action\_result\.data\.\*\.md5Checksum | string |  `md5` 
action\_result\.data\.\*\.mimeType | string |  `mime type` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.parents | string | 
action\_result\.data\.\*\.webContentLink | string |  `url` 
action\_result\.data\.\*\.webViewLink | string |  `url` 
action\_result\.summary\.next\_page\_token | string | 
action\_result\.summary\.total\_files\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 