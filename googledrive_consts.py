# --
# File: googledrive_consts.py
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

LIST_RESP_FIELDS = "nextPageToken, files(id, name, kind, mimeType, webContentLink, webViewLink)"

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
