"""
A Python script for downloading all files under a folder in Google Drive.
Downloaded files will be saved at the current working directory.
This script uses the official Google Drive API (https://developers.google.com/drive).
As the examples in the official doc are not very clear to me,
so I thought sharing this script would be helpful for someone.
To use this script, you should first follow the instruction 
in Quickstart section in the official doc (https://developers.google.com/drive/api/v3/quickstart/python):
- Enable Google Drive API 
- Download `credential.json`
- Install dependencies
Notes:
- This script will only work on a local environment, 
  i.e. you can't run this on a remote machine
  because of the authentication process of Google.
- This script only downloads binary files not google docs or spreadsheets.
Author: Sangwoong Yoon (https://github.com/swyoon/)
"""
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


'''Configuration'''
# ID of the folder to be downloaded.
# ID can be obtained from the URL of the folder
FOLDER_ID = 'YOURFOLDERIDGOHERE'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials.json"


def main():
    """Download all files in the specified folder in Google Drive."""
    creds, _ = google.auth.default()
    service = build('drive', 'v3', credentials=creds)

    page_token = None
    while True:
        # Call the Drive v3 API
        results = service.files().list(
            q=f"'{FOLDER_ID}' in parents",
            pageSize=10, fields="nextPageToken, files(id, name)",
            pageToken=page_token).execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

                file_id = item['id']
                request = service.files().get_media(fileId=file_id)

                with open(item['name'], 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break


if __name__ == '__main__':
    main()
