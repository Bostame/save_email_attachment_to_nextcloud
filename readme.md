# Save Email Attachment to Nextcloud 

## Overview
This Python script automates the process of fetching emails from an IMAP server, extracting attachments, and uploading them to a Nextcloud instance. It periodically checks for new emails, processes them, and uploads any attachments to Nextcloud, organized into directories based on the email subjects.

## Setup
1. **Environment Variables**: Ensure you have a `.env` file in the same directory as the script. Define the following environment variables:
    - `IMAP_SERVER`: Your IMAP server address.
    - `EMAIL`: Your email address.
    - `IMAP_PASSWORD`: Your IMAP password.
    - `IMAP_FOLDER`: The IMAP folder to search for emails (default is INBOX).
    - `NEXTCLOUD_BASE_URL`: Base URL of your Nextcloud instance.
    - `NEXTCLOUD_DIRECTORY`: Default directory to save attachments in Nextcloud.
    - `NEXTCLOUD_USERNAME`: Your Nextcloud username.
    - `NEXTCLOUD_PASSWORD`: Your Nextcloud password.

2. **Dependencies**: Make sure to install the required Python packages. You can install them using `pip`:
    ```
    pip install imaplib email requests python-dotenv
    ```

## Usage
Run the script by executing the `email_attachment_to_nextcloud.py` file. It will continuously check for new emails, download attachments, and upload them to Nextcloud.

## Implementation Details
### Functions
1. **save_attachment_to_nextcloud(attachment_path, nextcloud_directory)**:
    - Uploads the specified attachment to Nextcloud under the given directory.
    - Parameters:
        - `attachment_path`: Path to the attachment file.
        - `nextcloud_directory`: Destination directory in Nextcloud.
    
2. **fetch_emails()**:
    - Connects to the IMAP server, fetches emails from the specified folder, and processes them.
    - Extracts attachments from emails and saves them locally.
    - Uploads attachments to Nextcloud based on the email subjects.
    
### IMAP Settings
- `IMAP_SERVER`: The IMAP server address.
- `EMAIL`: Your email address.
- `IMAP_PASSWORD`: Your IMAP password.
- `IMAP_FOLDER`: The IMAP folder to search for emails (default is INBOX).

### Nextcloud Configuration
- `NEXTCLOUD_BASE_URL`: Base URL of your Nextcloud instance.
- `NEXTCLOUD_USERNAME`: Your Nextcloud username.
- `NEXTCLOUD_PASSWORD`: Your Nextcloud password.
- `NEXTCLOUD_DIRECTORY`: Default directory to save attachments in Nextcloud. If not specified, the attachments will be saved in the root directory.

## Logging
The script logs its activities using Python's logging module. It provides information about the processing of emails, saving of attachments, and uploading to Nextcloud. Logs are displayed at the INFO level and above.

## File Management
Attachments are saved locally in the `attachments` directory. If the attachment already exists locally, it will not be downloaded again. Ensure the `attachments` directory exists in the same directory as the script.

## Continuous Execution
The script runs indefinitely in a loop, periodically fetching emails, processing them, and uploading attachments to Nextcloud. It waits for 30 seconds between each iteration.

---

Include this documentation alongside your code in your GitHub repository for clear understanding and usage by others.