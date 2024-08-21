from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive():
    # Authenticate and build the Google Drive service
    creds = service_account.Credentials.from_service_account_file('path-to-your-service-account.json')
    drive_service = build('drive', 'v3', credentials=creds)

    # Set file metadata and upload
    file_metadata = {
        'name': 'GTFS_Realtime.zip',
        'parents': ['your-google-drive-folder-id']
    }
    media = MediaFileUpload('GTFS_Realtime.zip', mimetype='application/zip')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"File ID: {file.get('id')}")

if __name__ == "__main__":
    upload_to_drive()
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive():
    # Authenticate and build the Google Drive service
    creds = service_account.Credentials.from_service_account_file('path-to-your-service-account.json')
    drive_service = build('drive', 'v3', credentials=creds)

    # Set file metadata and upload
    file_metadata = {
        'name': 'GTFS_Realtime.zip',
        'parents': ['your-google-drive-folder-id']
    }
    media = MediaFileUpload('GTFS_Realtime.zip', mimetype='application/zip')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"File ID: {file.get('id')}")

if __name__ == "__main__":
    upload_to_drive()
