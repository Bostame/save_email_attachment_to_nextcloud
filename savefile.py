import imaplib
import email
import os
import requests
import time
import logging
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IMAP settings
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('IMAP_PASSWORD')
IMAP_FOLDER = os.getenv('IMAP_FOLDER')

# Nextcloud configuration
NEXTCLOUD_BASE_URL = os.getenv('NEXTCLOUD_BASE_URL')
NEXTCLOUD_USERNAME = os.getenv('NEXTCLOUD_USERNAME')
NEXTCLOUD_PASSWORD = os.getenv('NEXTCLOUD_PASSWORD')
NEXTCLOUD_DIRECTORY = os.getenv('NEXTCLOUD_BASE_URL', 'NEXTCLOUD_DIRECTORY')

def save_attachment_to_nextcloud(attachment_path, nextcloud_directory):
    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as f:
        file_content = f.read()
    response = requests.put(
        f'{NEXTCLOUD_BASE_URL}{nextcloud_directory}/{filename}',
        auth=(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD),
        data=file_content
    )
    if response.status_code == 201:
        logger.info(f'Successfully uploaded {filename} to Nextcloud under {nextcloud_directory}')
    else:
        logger.error(f'Failed to upload {filename} to Nextcloud under {nextcloud_directory}')
        logger.error(f'Response: {response.text}')

def fetch_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract subject
        subject = msg['subject']
        logger.info(f"Processing email with subject: {subject}")

        # Determine NEXTCLOUD_DIRECTORY based on subject
        if 'S1' in subject or 's1' in subject:
            nextcloud_directory = 'euref-lecturer/Campus-Euref/S1'
        elif 'S2' in subject or 's2' in subject:
            nextcloud_directory = 'euref-lecturer/Campus-Euref/S2'
        elif 'S3' in subject or 's3' in subject:
            nextcloud_directory = 'euref-lecturer/Campus-Euref/S3'
        elif 'S4' in subject or 's4' in subject:
            nextcloud_directory = 'euref-lecturer/Campus-Euref/S4'
        elif 'S5' in subject or 's5' in subject:
            nextcloud_directory = 'euref-lecturer/Campus-Euref/S5'
        else:
            logger.warning(f"No specific directory found for subject: {subject}. Using fallback directory.")
            nextcloud_directory = 'euref-lecturer/Campus-Euref/others'

        if msg.get_content_maintype() == 'multipart':
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                if part.get_filename():
                    attachment_path = os.path.join('./attachments', part.get_filename())
                    if not os.path.isfile(attachment_path):
                        with open(attachment_path, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        logger.info(f'Saved attachment: {attachment_path}')
                        save_attachment_to_nextcloud(attachment_path, nextcloud_directory)
                    else:
                        logger.info(f'Attachment {part.get_filename()} already exists in the local directory.')
    mail.close()
    mail.logout()


if __name__ == "__main__":
    if not os.path.exists('./attachments'):
        os.makedirs('./attachments')
    
    while True:
        logger.info("Fetching emails...")
        fetch_emails()
        logger.info("Waiting for 30 seconds...")
        time.sleep(30)
