# File: googledrive_consts.py
#
# Copyright (c) 2018-2022 Splunk Inc.
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
LIST_RESP_FIELDS = "nextPageToken, files(id, name, kind, mimeType, webContentLink, webViewLink, parents, md5Checksum)"

# The API is supposed to return all the metadeta, but my experience has been it only returning id, name, kind and mimeType
ALL_FILE_FIELDS = "kind, id, name, mimeType, description, starred, trashed, explicitlyTrashed, "\
                  "parents, properties, appProperties, spaces, version, webContentLink, webViewLink, "\
                  "iconLink, thumbnailLink, viewedByMe, viewedByMeTime, createdTime, modifiedTime, "\
                  "modifiedByMeTime, sharedWithMeTime, sharingUser, owners, lastModifyingUser, "\
                  "shared, ownedByMe, viewersCanCopyContent, writersCanShare, permissions, "\
                  "folderColorRgb, originalFilename, fullFileExtension, fileExtension, size, "\
                  "md5Checksum, quotaBytesUsed, headRevisionId, contentHints, imageMediaMetadata, "\
                  "videoMediaMetadata, capabilities, isAppAuthorized, hasThumbnail, thumbnailVersion, "\
                  "modifiedByMe, trashingUser, trashedTime, teamDriveId, permissionIds"

m_doc = 'application/msword'
m_docx = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
m_xls = 'application/vnd.ms-excel',
m_xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
m_csv = 'text/csv'
m_ppt = 'application/vnd.ms-powerpoint',
m_pptx = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'

m_google_doc = 'application/vnd.google-apps.document'
m_google_sheet = 'application/vnd.google-apps.spreadsheet'
m_google_slide = 'application/vnd.google-apps.presentation'

# There is dynamic list of these which you can query through the API,
#  but it contains a lot of conversions which I'd imagine you don't want
#  for example, BMP -> google doc file
# This is a more simplified list of things, like docx -> google doc,
MIME_TYPE_MAPPINGS = {
    m_doc: m_google_doc,
    m_docx: m_google_doc,
    m_xls: m_google_sheet,
    m_xlsx: m_google_sheet,
    m_csv: m_google_sheet,
    m_ppt: m_google_slide,
    m_pptx: m_google_slide,
}

EXPORT_TYPE_MAPPINGS = {
    m_google_doc: m_docx,
    m_google_sheet: m_xlsx,
    m_google_slide: m_pptx,
}
DEFAULT_REQUEST_TIMEOUT = 30  # in seconds
