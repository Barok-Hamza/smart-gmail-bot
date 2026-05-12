import os
import json
import time
import schedule

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

print("Smart Gmail Bot Running...")

# Labels
labels_to_create = [
    "Jobs",
    "Internships",
    "Priority",
    "School",
    "Shopping",
    "Social",
    "Housing",
    "Tech Programs"
]

# Create labels
results = service.users().labels().list(userId='me').execute()
existing_labels = results.get('labels', [])

existing_label_names = [label['name'] for label in existing_labels]

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

# Refresh labels
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

label_dict = {}

for label in labels:
    label_dict[label['name']] = label['id']

# File to store processed emails
PROCESSED_FILE = "processed_emails.json"

# Load processed emails
if os.path.exists(PROCESSED_FILE):

    with open(PROCESSED_FILE, "r") as file:
        processed_emails = json.load(file)

else:
    processed_emails = []

# Main categorization function
def check_emails():

    global processed_emails

    print("\nChecking for new emails...\n")

    results = service.users().messages().list(
        userId='me',
        maxResults=10
    ).execute()

    messages = results.get('messages', [])

    for message in messages:

        message_id = message['id']

        # Skip already processed emails
        if message_id in processed_emails:
            continue

        msg = service.users().messages().get(
            userId='me',
            id=message_id
        ).execute()

        headers = msg['payload']['headers']

        subject = ""
        sender = ""

        for header in headers:

            if header['name'] == 'Subject':
                subject = header['value']

            if header['name'] == 'From':
                sender = header['value']

        subject_lower = subject.lower()
        sender_lower = sender.lower()

        selected_label = None

        # Categorization rules
        if "tiktok" in sender_lower:
            selected_label = "Social"

        elif "h&m" in sender_lower:
            selected_label = "Shopping"

        elif "codepath" in sender_lower:
            selected_label = "Tech Programs"

        elif "apartment" in sender_lower or "rent" in subject_lower:
            selected_label = "Housing"

        # Apply label
        if selected_label:

            label_id = label_dict[selected_label]

            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={
                    'addLabelIds': [label_id]
                }
            ).execute()

            print(f"Applied label '{selected_label}' to:")
            print(subject)
            print("-" * 50)

        # Mark email as processed
        processed_emails.append(message_id)

    # Save processed emails
    with open(PROCESSED_FILE, "w") as file:
        json.dump(processed_emails, file)

# Run every 30 seconds
schedule.every(30).seconds.do(check_emails)

# Run immediately once
check_emails()

# Keep running forever
while True:

    schedule.run_pending()
    time.sleep(1)