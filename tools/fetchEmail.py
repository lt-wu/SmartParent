import autogen
from tools.pdf2img import pdf2img

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import base64
from fpdf import FPDF


from tools.email import authenticate_gmail, list_emails, get_email_details, save_to_pdf

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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


 