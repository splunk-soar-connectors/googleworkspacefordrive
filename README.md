[comment]: # "Auto-generated SOAR connector documentation"
# G Suite for Drive

Publisher: Splunk  
Connector Version: 2.2.1  
Product Vendor: Google  
Product Name: Google Drive  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.1.0  

This app allows various file manipulation actions to be performed on Google Drive

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

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Google Drive asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**login_email** |  required  | string | Login (Admin) email
**key_json** |  required  | password | Contents of Service Account JSON file

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

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/admin.directory.user.readonly</li></ul>.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list users'
Get the list of users

Type: **investigate**  
Read only: **True**

Action uses the Admin SDK API to get a list of users. Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/admin.directory.user.readonly</li></ul><br>The action will limit the number of users returned to <b>max_items</b> or (if not specified) 500. If the system has any more users, a next page token will be returned in <b>action_result.summary.next_page_token</b>. Use this value as input to <b>next_page_token</b> in subsequent calls to <b>list users</b>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**max_items** |  optional  | Maximum number of users to return | numeric | 
**next_page_token** |  optional  | Next Page Token | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.max_items | numeric |  |   2 
action_result.parameter.next_page_token | string |  |   Invalid 
action_result.data.\*.agreedToTerms | boolean |  |   True  False 
action_result.data.\*.archived | boolean |  |   True  False 
action_result.data.\*.changePasswordAtNextLogin | boolean |  |   True  False 
action_result.data.\*.creationTime | string |  |   2017-05-11T21:35:38.000Z 
action_result.data.\*.customerId | string |  |   C02eisxhx 
action_result.data.\*.emails.\*.address | string |  `email`  |   test@test.us 
action_result.data.\*.emails.\*.primary | boolean |  |   True  False 
action_result.data.\*.emails.\*.type | string |  |   work 
action_result.data.\*.etag | string |  |   "Slw4z1WwXVNuSGyQ8doTq9uidvys/F2uDjNoukDRgPx6dvH-7j-A7NgQ" 
action_result.data.\*.id | string |  |   113211632970586452310 
action_result.data.\*.includeInGlobalAddressList | boolean |  |   True  False 
action_result.data.\*.ipWhitelisted | boolean |  |   True  False 
action_result.data.\*.isAdmin | boolean |  |   True  False 
action_result.data.\*.isDelegatedAdmin | boolean |  |   True  False 
action_result.data.\*.isEnforcedIn2Sv | boolean |  |   True  False 
action_result.data.\*.isEnrolledIn2Sv | boolean |  |   True  False 
action_result.data.\*.isMailboxSetup | boolean |  |   True  False 
action_result.data.\*.kind | string |  |   admin#directory#user 
action_result.data.\*.languages.\*.languageCode | string |  |   en 
action_result.data.\*.languages.\*.preference | string |  |   preferred 
action_result.data.\*.lastLoginTime | string |  |   2018-01-06T01:11:49.000Z 
action_result.data.\*.name.familyName | string |  |   Edwards 
action_result.data.\*.name.fullName | string |  |   test Edwards 
action_result.data.\*.name.givenName | string |  |   test 
action_result.data.\*.nonEditableAliases | string |  `email`  |   test@test.us 
action_result.data.\*.orgUnitPath | string |  |   / 
action_result.data.\*.phones.\*.type | string |  |   work 
action_result.data.\*.phones.\*.value | string |  |  
action_result.data.\*.primaryEmail | string |  `email`  |   test@test.us 
action_result.data.\*.recoveryEmail | string |  |   test@test.us 
action_result.data.\*.suspended | boolean |  |   True  False 
action_result.data.\*.suspensionReason | string |  |   ADMIN 
action_result.summary.next_page_token | string |  |   ~!!~AI9FV7RCbmvPCnWK0UIxnjniVz68Lt8ZOsGim7uc5YxlceqS4ovMelh229zAeFmpmw1aoBTI4ZmcjNxMdAPHEE5nW8BKEx7TI4LzYmLlvpBGoKnyf3lPFenef25jRS7FSMDBb1prqjMEFzRlvZtfX4X9kZuYVDk_dwUcjiKDkEXC2DUPCPcKctAg2HN-VH9FGcSAcSBftVBfbrLwZu9AgnfHvz-8wkDK1PpwE4l1H_mkfvRm_Ckvq9dnLCFSu5W-YzF6nXuZSgmJx5WWMO-IHSLILAf8OXPwbxJbTqM_YCdLeYD71IeqEu_idn54UhYNUCBi3mxeQJzzfp4vHJa3q1wN4uUuCNshqkXvLDwuVIk4cYHHVcJ2-A4GJhPGkQ2SfuMrIigi0nGKEk8pTmJaeD5C825ALevDLf574abZ385Hu7d0NTpJxfDdJti0JdcyL66qYis2l_zxMZZ-ZcSFpl_TSUxk87jhhjI55tCvjkw= 
action_result.summary.total_users_returned | numeric |  |   6 
action_result.message | string |  |   Successfully retrieved 6 users 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete file'
Delete a file

Type: **contain**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/drive</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email (use this drive) | string |  `email` 
**id** |  required  | File ID | string |  `drive file id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.email | string |  `email`  |   abc@gmail.com 
action_result.parameter.id | string |  `drive file id`  |   12wNhYsdgesIzNyXfXZqI7l9GCs4yjoeZt-vgy46DA 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   File doesn't exist or has already been deleted 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create folder'
Create a new folder

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/drive</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email (use this drive) | string |  `email` 
**name** |  required  | Name of the new folder | string | 
**folder_id** |  optional  | ID of the parent folder | string |  `drive file id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.email | string |  `email`  |   abc@gmail.com 
action_result.parameter.folder_id | string |  `drive file id`  |   1OPjWKnOCGlretd23P0lnW5mlLE2x8D 
action_result.parameter.name | string |  |   NewFolder1 
action_result.data | string |  |  
action_result.summary.new_folder_id | string |  `drive file id`  |   1OPjWKnOCGlretd23P0lnW5mlLE2x8D 
action_result.message | string |  |   Successfully added new folder to Drive 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'upload file'
Upload a file from the Vault to Drive

Type: **generic**  
Read only: **False**

If the Drive API does not support the conversion from the files original MIME type to <b>dest_mime_type</b>, the uploaded file will become a native Google Drive type (e.g. a Google document).<br>Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/drive</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email (use this drive) | string |  `email` 
**vault_id** |  required  | Vault ID | string |  `vault id`  `sha1` 
**source_mime_type** |  optional  | MIME type of file in vault | string |  `mime type` 
**dest_mime_type** |  optional  | MIME type of new Drive file (will disable convert) | string |  `mime type` 
**folder_id** |  optional  | ID of the parent folder | string |  `drive file id` 
**file_name** |  optional  | Set the file name in Drive | string | 
**convert** |  optional  | Attempt to convert file to native Drive type. Will only have an effect if dest_mime_type is not set | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.convert | boolean |  |   True  False 
action_result.parameter.dest_mime_type | string |  `mime type`  |   application/vnd.test-apps.spreadsheet 
action_result.parameter.email | string |  `email`  |   abc@gmail.com 
action_result.parameter.file_name | string |  |   file1 
action_result.parameter.folder_id | string |  `drive file id`  |   1OPjWKnOCGlrePZ3cnLD0lnW5mlLE2x8D 
action_result.parameter.source_mime_type | string |  `mime type`  |   application/vnd.test-apps.spreadsheet 
action_result.parameter.vault_id | string |  `vault id`  `sha1`  |   82cbbb588ce83b5527e2f9f1d3bcba24f60c92cc 
action_result.data | string |  |  
action_result.summary.new_file_id | string |  `drive file id`  |   12wNhYsdgesIzNyXfXZqI7l9GCs4yjoeZt-vSJaLo1fA 
action_result.message | string |  |   Successfully added new file to Drive 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get file'
Get information about a file or download it to the Vault

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/drive.readonly</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email (use this drive) | string |  `email` 
**id** |  required  | File ID | string |  `drive file id` 
**download_file** |  optional  | Download the file to the Vault | boolean | 
**mime_type** |  optional  | MIME Type for exported file. This will only have an effect if the original document is file type that needs to be exported (i.e. Google Docs / Sheets / Slides files) | string |  `mime type` 
**file_name** |  optional  | Set a new name for the file before adding it to the vault | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.download_file | boolean |  |   True  False 
action_result.parameter.email | string |  `email`  |   abc@gmail.com 
action_result.parameter.file_name | string |  |   file.pdf 
action_result.parameter.id | string |  `drive file id`  |   12wNhYsdgesIzNyXfXZqI7l9GCs4yjoeZt-vSJaLo1fA 
action_result.parameter.mime_type | string |  `mime type`  |   application/pdf 
action_result.data.\*.capabilities.canAcceptOwnership | boolean |  |   True  False 
action_result.data.\*.capabilities.canAddChildren | boolean |  |   True  False 
action_result.data.\*.capabilities.canAddMyDriveParent | boolean |  |   True  False 
action_result.data.\*.capabilities.canChangeCopyRequiresWriterPermission | boolean |  |   True  False 
action_result.data.\*.capabilities.canChangeSecurityUpdateEnabled | boolean |  |   True  False 
action_result.data.\*.capabilities.canChangeViewersCanCopyContent | boolean |  |   True  False 
action_result.data.\*.capabilities.canComment | boolean |  |   True  False 
action_result.data.\*.capabilities.canCopy | boolean |  |   True  False 
action_result.data.\*.capabilities.canDelete | boolean |  |   True  False 
action_result.data.\*.capabilities.canDownload | boolean |  |   True  False 
action_result.data.\*.capabilities.canEdit | boolean |  |   True  False 
action_result.data.\*.capabilities.canListChildren | boolean |  |   True  False 
action_result.data.\*.capabilities.canModifyContent | boolean |  |   True  False 
action_result.data.\*.capabilities.canModifyContentRestriction | boolean |  |  
action_result.data.\*.capabilities.canModifyLabels | boolean |  |   True  False 
action_result.data.\*.capabilities.canMoveChildrenWithinDrive | boolean |  |   True  False 
action_result.data.\*.capabilities.canMoveItemIntoTeamDrive | boolean |  |   True  False 
action_result.data.\*.capabilities.canMoveItemOutOfDrive | boolean |  |   True  False 
action_result.data.\*.capabilities.canMoveItemWithinDrive | boolean |  |   True  False 
action_result.data.\*.capabilities.canReadLabels | boolean |  |   True  False 
action_result.data.\*.capabilities.canReadRevisions | boolean |  |   True  False 
action_result.data.\*.capabilities.canRemoveChildren | boolean |  |   True  False 
action_result.data.\*.capabilities.canRemoveMyDriveParent | boolean |  |   True  False 
action_result.data.\*.capabilities.canRename | boolean |  |   True  False 
action_result.data.\*.capabilities.canShare | boolean |  |   True  False 
action_result.data.\*.capabilities.canTrash | boolean |  |   True  False 
action_result.data.\*.capabilities.canUntrash | boolean |  |   True  False 
action_result.data.\*.createdTime | string |  |   2018-01-10T01:17:40.409Z 
action_result.data.\*.explicitlyTrashed | boolean |  |   True  False 
action_result.data.\*.fileExtension | string |  |  
action_result.data.\*.fullFileExtension | string |  |  
action_result.data.\*.hasThumbnail | boolean |  |   True  False 
action_result.data.\*.headRevisionId | string |  |   0B3SKAcU2R7vU7lNyRm40eHNlS245VWZiTnp3QXh4OFFZRSt3PQ 
action_result.data.\*.iconLink | string |  `url`  |   https://drive-thirdparty.testusercontent.com/16/type/application/vnd.test-apps.spreadsheet 
action_result.data.\*.id | string |  `drive file id`  |   12wNhYsdgesIzNyXfXZqI7l9GCs4yjoeZt-vSJaLo1fA 
action_result.data.\*.isAppAuthorized | boolean |  |   True  False 
action_result.data.\*.kind | string |  |   drive#file 
action_result.data.\*.lastModifyingUser.displayName | string |  |   test Edwards 
action_result.data.\*.lastModifyingUser.emailAddress | string |  `email`  |   test@test.us 
action_result.data.\*.lastModifyingUser.kind | string |  |   drive#user 
action_result.data.\*.lastModifyingUser.me | boolean |  |   True  False 
action_result.data.\*.lastModifyingUser.permissionId | string |  |   03385014771683765349 
action_result.data.\*.lastModifyingUser.photoLink | string |  |   https://lh3.testusercontent.com/a/default-user=s64 
action_result.data.\*.md5Checksum | string |  `md5`  |   ts6c887e20b103b9215082dcd07a86fc 
action_result.data.\*.mimeType | string |  `mime type`  |   application/vnd.test-apps.spreadsheet 
action_result.data.\*.modifiedByMe | boolean |  |   True  False 
action_result.data.\*.modifiedByMeTime | string |  |   2018-01-10T01:17:41.700Z 
action_result.data.\*.modifiedTime | string |  |   2018-01-10T01:17:41.700Z 
action_result.data.\*.name | string |  |   Untitled.xlsx 
action_result.data.\*.originalFilename | string |  |   New Plain Text 
action_result.data.\*.ownedByMe | boolean |  |   True  False 
action_result.data.\*.owners.\*.displayName | string |  |   test Edwards 
action_result.data.\*.owners.\*.emailAddress | string |  `email`  |   test@test.us 
action_result.data.\*.owners.\*.kind | string |  |   drive#user 
action_result.data.\*.owners.\*.me | boolean |  |   True  False 
action_result.data.\*.owners.\*.permissionId | string |  |   03385014771683713179 
action_result.data.\*.owners.\*.photoLink | string |  |   https://lh3.testusercontent.com/a/default-user=s64 
action_result.data.\*.parents | string |  |   0AHSKAcU2T6x2Uk9PVA 
action_result.data.\*.permissionIds | string |  |   03385014771683713179 
action_result.data.\*.permissions.\*.deleted | boolean |  |   True  False 
action_result.data.\*.permissions.\*.displayName | string |  |   test Edwards 
action_result.data.\*.permissions.\*.emailAddress | string |  `email`  |   test@test.us 
action_result.data.\*.permissions.\*.id | string |  |   03385014771683713179 
action_result.data.\*.permissions.\*.kind | string |  |   drive#permission 
action_result.data.\*.permissions.\*.pendingOwner | boolean |  |   True  False 
action_result.data.\*.permissions.\*.photoLink | string |  |   https://lh3.testusercontent.com/a/default-user=s64 
action_result.data.\*.permissions.\*.role | string |  |   owner 
action_result.data.\*.permissions.\*.type | string |  |   user 
action_result.data.\*.quotaBytesUsed | string |  |   0 
action_result.data.\*.shared | boolean |  |   True  False 
action_result.data.\*.size | string |  |   48 
action_result.data.\*.spaces | string |  |   drive 
action_result.data.\*.starred | boolean |  |   True  False 
action_result.data.\*.thumbnailLink | string |  `url`  |   https://drive.test.com/a/acme.com/&v=1&s=AMedNnoAAAAAWlWZqdcfxjkYUHbKl-ko4BLBo5QZYPyz8c&sz=s220?ddrp=1# 
action_result.data.\*.thumbnailVersion | string |  |   1 
action_result.data.\*.trashed | boolean |  |   True  False 
action_result.data.\*.version | string |  |   6 
action_result.data.\*.viewedByMe | boolean |  |   True  False 
action_result.data.\*.viewedByMeTime | string |  |   2018-01-10T01:17:48.669Z 
action_result.data.\*.viewersCanCopyContent | boolean |  |   True  False 
action_result.data.\*.webContentLink | string |  `url`  |   https://drive.test.com/a/acme.com/uc?id=12wNhYsdgesIzNyXfXZqI7l9GCs4yjoeZt-vSJaLo1fA&export=download 
action_result.data.\*.webViewLink | string |  `url`  |   https://docs.test.com/a/acme.com/spreadsheets/d/12wNhYsdgesIzNyXfXZqI7l6dfGjoeZt-vSJaLo1fA/edit?usp=drivesdk 
action_result.data.\*.writersCanShare | boolean |  |   True  False 
action_result.summary.vault_id | string |  `sha1`  `vault id`  |   7f56GVe7bdeffe563d13770c2519f99a19bbeef3 
action_result.message | string |  |   Successfully retrieved file and added to vault 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   0   

## action: 'list files'
Get the list of files

Type: **investigate**  
Read only: **True**

You can use the <b>query</b> parameter to filter the results. The full documentation on this parameter can be read <a href="https://developers.google.com/drive/v3/web/search-parameters">here</a>. Here are some examples:<ul><li><b>mimeType='application/vnd.google-apps.folder'</b>: show only folders</li><li><b>modifiedTime > '2018-01-05T12:00:00' and mimeType='application/vnd.google-apps.document'</b>: Show only documents which have been modified since the date</li></ul>.<br>Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/drive.readonly</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  optional  | Email (use this drive) | string |  `email` 
**max_results** |  optional  | Max Results | numeric | 
**next_page_token** |  optional  | Next Page Token | string | 
**query** |  optional  | Query | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.email | string |  `email`  |   abc@gmail.com 
action_result.parameter.max_results | numeric |  |   2 
action_result.parameter.next_page_token | string |  |   ~!!~Tg45VCbmvPCnWK0UIxnjniVz68Lt8ZOsGim7uc5YxlceqS4ovMelh229zAeFmpmw1aoBTI4ZmcjNxMdAPHEE5nW8BKEx7TI4LzYmLlvpBGoKnyf3lPFenef25jRS7FSMDBb1prqjMEFzRlvZtfX4X9kZuYVDk_dwUcjiKDkEXC2DUPCPcKctAg2HN-VH9FGcSAcSBftVBfbrLwZu9AgnfHvz-8wkDK1PpwE4l1H_mkfvRm_Ckvq9dnLCFSu5W-YzF6nXuZSgmJx5WWMO-IHSLILAf8OXPwbxJbTqM_YCdLeYD71IeqEu_idn54UhYNUCBi3mxeQJzzfp4vHJa3q1wN4uUuCNshqkXvLDwuVIk4cYHHVcJ2-A4GJhPGkQ2SfuMrIigi0nGKEk8pTmJaeD5C825ALevDLf574abZ385Hu7d0NTpJxfDdJti0JdcyL66qYis2l_zxMZZ-ZcSFpl_FKuhip3AP97VIk0QUiYlh9nH55tCvjkw= 
action_result.parameter.query | string |  |   modifiedTime > '2012-06-04T12:00:00' 
action_result.data.\*.id | string |  `drive file id`  |   1PJZ_cZKMbIZWOJdQQe3r41vdGj8 
action_result.data.\*.kind | string |  |   drive#file 
action_result.data.\*.md5Checksum | string |  `md5`  |   b99abc7a0e9da88f8636f0c48f924f63 
action_result.data.\*.mimeType | string |  `mime type`  |   application/vnd.test-apps.folder 
action_result.data.\*.name | string |  |   / 
action_result.data.\*.parents | string |  |   0AHSKAcU2T6x2Uk9PVA 
action_result.data.\*.webContentLink | string |  `url`  |   https://drive.test.com/a/acme.com/uc?id=1pF6FMUwRkTl2Bs15-CzWQVHa5LyuFIpSFlPFOxzD-Nw&export=download 
action_result.data.\*.webViewLink | string |  `url`  |   https://drive.test.com/drive/folders/1tfCbCKJ3d122RFSHxuVyDCx0a29dzJ-B 
action_result.summary.next_page_token | string |  |   ~!!~Td57GCbmvPCnWK0UIxnjniVz68Lt8ZOsGim7uc5YxlceqS4ovMelh229zAeFmpmw1aoBTI4ZmcjNxMdAPHEE5nW8BKEx7TI4LzYmLlvpBGoKnyf3lPFenef25jRS7FSMDBb1prqjMEFzRlvZtfX4X9kZuYVDk_dwUcjiKDkEXC2DUPCPcKctAg2HN-VH9FGcSAcSBftVBfbrLwZu9AgnfHvz-8wkDK1PpwE4l1H_mkfvRm_Ckvq9dnLCFSu5W-YzF6nXuZSgmJx5WWMO-IHSLILAf8OXPwbxJbTqM_YCdLeYD71IeqEu_idn54UhYNUCBi3mxeQJzzfp4vHJa3q1wN4uUuCNshqkXvLDwuVIk4cYHHVcJ2-A4GJhPGkQ2SfuMrIigi0nGKEk8pTmJaeD5C825ALevDLf574abZ385Hu7d0NTpJxfDdJti0JdcyL66qYis2l_zxMZZ-ZcSFpl_FKuhip3AP97VIk0QUiYlh9nH55tCvjkw= 
action_result.summary.total_files_returned | numeric |  |   47 
action_result.message | string |  |   Successfully retrieved 47 files 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 