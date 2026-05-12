import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

creds = None

# Load token
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Login if needed
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Build Gmail service
service = build('gmail', 'v1', credentials=creds)

print("Connected to Gmail!")

# Labels we want
labels_to_create = [
    "Jobs",
    "School",
    "Priority",
    "Internships"
]

# Get existing labels
results = service.users().labels().list(userId='me').execute()
existing_labels = results.get('labels', [])

existing_label_names = [label['name'] for label in existing_labels]

# Create labels if they don't exist
for label_name in labels_to_create:

    if label_name not in existing_label_names:

        label_object = {
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }

        service.users().labels().create(
            userId='me',
            body=label_object
        ).execute()

        print(f"Created label: {label_name}")

    else:
        print(f"Label already exists: {label_name}")