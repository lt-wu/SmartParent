import autogen
from tools.pdf2img import pdf2img

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import base64
from fpdf import FPDF

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def email_reader_agent():
    return autogen.AssistantAgent(
    name="EmailReader", system_message="Reads the latest school newsletter", llm_config=False)


def authenticate_gmail():
    """Authenticate and connect to Gmail API."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_emails(service):
    """List all emails in the Gmail inbox."""
    all_messages = []
    next_page_token = None
    query = 'has:attachment'  # Search for forwarded emails
    while True:
        # Fetch messages (default 100 per request)
        response = service.users().messages().list(userId='me',  q= query, pageToken=next_page_token).execute()
        messages = response.get('messages', [])
        print(messages)
        all_messages.extend(messages)
        
        # Check if there are more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return all_messages
def get_email_details(service, message_id):
    """Retrieve email details (subject and body) and download images."""
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    payload = message['payload']
    print("message ", payload  )
    headers = payload['headers']
    # Extract subject
    subject = "No Subject"
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
            break
    # Extract email body (text/plain or HTML)
    body = ""
    images = []
    if 'parts' in payload:
        for part in payload['parts']:
            # Handle plain text
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode("utf-8")
            # Handle inline images
            elif part['mimeType'].startswith('image/'):
                attachment_id = part['body'].get('attachmentId')
                print("attachment_id-----",attachment_id)
                if attachment_id:
                    image_data = get_attachment(service, message_id, attachment_id)
                    image_filename = f"{part['filename']}"
                    save_image(image_data, image_filename)
                    images.append(image_filename)
            elif part['mimeType'].startswith('application/pdf'):
                attachment_id = part['body'].get('attachmentId')
                print("attachment_id-----",attachment_id)
                if attachment_id:
                    image_data = get_attachment(service, message_id, attachment_id)
                    image_filename = f"{part['filename']}"
                    save_image(image_data, image_filename)
    elif payload['mimeType'] == 'text/plain':
        body = base64.urlsafe_b64decode(payload['body']['data']).decode("utf-8")
    return subject, body, images


def get_attachment(service, message_id, attachment_id):
    """Retrieve attachment data."""
    attachment = service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()
    data = attachment['data']
    return base64.urlsafe_b64decode(data)

def save_image(image_data, filename):
    """Save image to a file."""
    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Image saved as {filename}")

def save_to_pdf(subject, body, images, output_filename):
    """Save email content and images to a PDF file."""

    body = body.encode("latin-1", "replace").decode("latin-1")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add subject and body
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Subject: {subject}", ln=True, align='L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, body)

    # Add images to the PDF
    for image in images:
        pdf.add_page()  # Add a new page for each image
        pdf.image(image, x=10, y=30, w=180)  # Adjust the image size and position
    
    pdf.output(output_filename)
    #print(f"PDF saved as {output_filename}")


def fetchEmail():
    try:
        # Authenticate and connect to Gmail API
        print("Authenticate and connect to Gmail API")
        service = authenticate_gmail()
        # List recent emails
        emails = list_emails(service)
        if not emails:
            print("No emails found.")
            return
        # Process each email
        for email in emails:
            message_id = email['id']
            subject, body, images = get_email_details(service, message_id)
            
            print(f"Email Subject: {subject}")
            print(f"Email Body:\n{body}\n")
            print(f"Images: {images}")
            
            # Save email to PDF
            output_filename = f"email_{message_id}.pdf"
            save_to_pdf(subject, body, images, output_filename)
            pdf2img()
        return "Newsletter fetched successfully"
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


def authenticate_gmail3():

    # Specify the required Google Calendar API scope
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    """
    Authenticate and connect to the Google Calendar API.
    Returns:
        service (Resource): Google Calendar API service object.
    """
    creds = None

    # Check if token.pickle exists (stores user's credentials)
    if os.path.exists('token3.pickle'):
        with open('token3.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are found, authenticate the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials3.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token3.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Google Calendar API
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(event_data):
    """
    Create an event on the user's Google Calendar.

    Args:
        event_data (dict): Dictionary containing event details in the following format:
            {
                "summary": "Event Title",
                "location": "Event Location",
                "description": "Event Description",
                "start": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",
                    "timeZone": "Time Zone"
                },
                "end": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",
                    "timeZone": "Time Zone"
                },
                "attendees": [
                    {"email": "attendee_email@example.com"},
                    ...
                ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 24 * 60},  # 1 day before
                        {"method": "popup", "minutes": 10}         # 10 minutes before
                    ]
                }
            }

    Returns:
        str: The result of the event creation process.
    """

    """
    Create an event on the user's Google Calendar.

    Args:
        event_data (dict): Dictionary containing event details in the following format:
            {
                "summary": "Event Title",
                "location": "Event Location",
                "description": "Event Description",
                "start": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",
                    "timeZone": "Time Zone"
                },
                "end": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",
                    "timeZone": "Time Zone"
                },
                "attendees": [
                    {"email": "attendee_email@example.com"},
                    ...
                ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 3 * 24 * 60},  # 3 day before
                        {"method": "popup", "minutes": 10}         # 10 minutes before
                    ]
                }
            }

    Returns:
        str: The result of the event creation process.
    """
    try:
        print("Authenticating and connecting to Google Calendar API...")
        service = authenticate_gmail3()  # Ensure this function is defined and working.

        # Debugging: Print the service object type
        print(f"Service Object Type: {type(service)}")

        # Debugging: Print the event data
        print(f"Event Data: {event_data}")

        # Insert the event into the user's primary calendar
        print("Creating event on Google Calendar...")
        event = service.events().insert(calendarId='primary', body=event_data).execute()

        # Log and return the event creation result
        event_link = event.get('htmlLink', 'No link available')
        print(f"Event successfully created: {event_link}")
        return f"Event successfully created: {event_link}"


    except Exception as e:
        # Handle and log errors gracefully
        error_message = f"Error creating event: {e}"
        print(error_message)
        return error_message


#service = authenticate_gmail()
#fetch_latest_newsletter()