import imaplib
import email
import os
import requests
import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
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

# Directory for saving attachments
ATTACHMENTS_DIR = './attachments'

# Track senders notified about invalid extensions
notified_senders = set()

# Function to load allowed extensions from file
def load_allowed_extensions(file_path='extensions.txt'):
    with open(file_path, 'r') as file:
        extensions = file.read().splitlines()
    return set(ext.strip() for ext in extensions)

# Load allowed extensions
ALLOWED_EXTENSIONS = load_allowed_extensions()

def is_allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

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

# Function to send acknowledgment email
def send_acknowledgment_email(sender_email, saved_folder):
    # Email configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    EMAIL_FROM = os.getenv('EMAIL_FROM')

    # Compose the message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = sender_email
    msg['Subject'] = 'Files Received and Saved'

    body = f'Dear Sir / Madam,\n\nYour files have been received and saved under the workspace folder: {saved_folder}. Please see the file in the seminar room {saved_folder} laptop.\n\nBest regards,\nTUBS IT'

    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, sender_email, msg.as_string())

# Function to send invalid file extension email
def send_invalid_extension_email(sender_email):
    # Email configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    EMAIL_FROM = os.getenv('EMAIL_FROM')

    # Compose the message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = sender_email
    msg['Subject'] = 'Invalid File Extension'

    body = 'Dear Sir / Madam,\n\nOne or more files you sent have an unsupported file extension. Please check the file and send a valid file.\n\nBest regards,\nTUBS IT'

    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, sender_email, msg.as_string())

def fetch_new_emails(last_check_time):
    new_attachments = []
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for emails since the last check time
    since_date = last_check_time.strftime('%d-%b-%Y')
    result, data = mail.search(None, f'(SINCE "{since_date}")')
    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract sender email
        sender_email = msg['From']

        # Extract subject
        subject = msg['subject']
        logger.info(f"Processing email with subject: {subject}")

        # Determine NEXTCLOUD_DIRECTORY based on subject
        if 'S1' in subject or 's1' in subject:
            saved_folder = 'euref-lecturer/Campus-Euref/S1'
        elif 'S2' in subject or 's2' in subject:
            saved_folder = 'euref-lecturer/Campus-Euref/S2'
        elif 'S3' in subject or 's3' in subject:
            saved_folder = 'euref-lecturer/Campus-Euref/S3'
        elif 'S4' in subject or 's4' in subject:
            saved_folder = 'euref-lecturer/Campus-Euref/S4'
        elif 'S5' in subject or 's5' in subject:
            saved_folder = 'euref-lecturer/Campus-Euref/S5'
        else:
            logger.warning(f"No specific directory found for subject: {subject}. Using fallback directory.")
            saved_folder = 'euref-lecturer/Campus-Euref/others'

        invalid_extension_found = False

        if msg.get_content_maintype() == 'multipart':
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                if part.get_filename():
                    attachment_filename = part.get_filename()
                    if is_allowed_file(attachment_filename):
                        attachment_path = os.path.join(ATTACHMENTS_DIR, attachment_filename)
                        if not os.path.isfile(attachment_path):
                            with open(attachment_path, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            logger.info(f'Saved attachment: {attachment_path}')
                            save_attachment_to_nextcloud(attachment_path, saved_folder)
                            new_attachments.append(attachment_path)
                        else:
                            logger.info(f'Attachment {part.get_filename()} already exists in the local directory.')
                    else:
                        logger.warning(f'Attachment {attachment_filename} has an unsupported file extension and was skipped.')
                        invalid_extension_found = True
    
        # Send acknowledgment email for valid attachments
        if new_attachments:
            send_acknowledgment_email(sender_email, saved_folder)

        # Send invalid extension email if any invalid extension found and sender not already notified
        if invalid_extension_found and sender_email not in notified_senders:
            send_invalid_extension_email(sender_email)
            notified_senders.add(sender_email)

    mail.close()
    mail.logout()

    return new_attachments

# Function to cleanup old attachments
def cleanup_old_attachments():
    now = datetime.now()
    threshold = timedelta(days=30)  # Remove attachments older than 30 days
    for filename in os.listdir(ATTACHMENTS_DIR):
        file_path = os.path.join(ATTACHMENTS_DIR, filename)
        if os.path.isfile(file_path):
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - modified_time > threshold:
                os.remove(file_path)
                logger.info(f'Removed old attachment: {file_path}')

if __name__ == "__main__":
    if not os.path.exists(ATTACHMENTS_DIR):
        os.makedirs(ATTACHMENTS_DIR)
    
    last_check_time = datetime.now()

    while True:
        logger.info("Fetching new emails...")
        new_attachments = fetch_new_emails(last_check_time)
        logger.info("Cleanup old attachments...")
        cleanup_old_attachments()
        logger.info("Waiting for 30 seconds...")
        time.sleep(30)
        last_check_time = datetime.now()  # Update last check time after each iteration
