from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import base64
from fpdf import FPDF
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
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
                    image_filename = f"{message_id}_{part['filename']}"
                    save_image(image_data, image_filename)
                    images.append(image_filename)
            elif part['mimeType'].startswith('application/pdf'):
                attachment_id = part['body'].get('attachmentId')
                print("attachment_id-----",attachment_id)
                if attachment_id:
                    image_data = get_attachment(service, message_id, attachment_id)
                    image_filename = f"{message_id}_{part['filename']}"
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


def main():
    # Authenticate and connect to Gmail API
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


if __name__ == '__main__':
    main()
