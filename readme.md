# Save Email Attachment to Nextcloud

## Overview
This Python script automates the process of fetching emails from an IMAP server, extracting attachments, and uploading them to a Nextcloud instance. It periodically checks for new emails, processes them, and uploads any attachments to Nextcloud, organized into directories based on the email subjects. If an email contains files with invalid extensions, the script sends a notification to the sender.

## Setup

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Bostame/save_email_attachment_to_nextcloud.git
    ```

2. Navigate to the project directory:

    ```bash
    cd save_email_attachment_to_nextcloud
    ```

3. Create a conda environment and install dependencies:

    ```bash
    conda env create -f environment.yml
    ```

4. **Environment Variables**: Ensure you have correct definition of the following environment variables in the `.env` file. 

    - **IMAP Configuration**:
        - `IMAP_SERVER`: Your IMAP server address.
        - `IMAP_PORT`: Port number for IMAP server.
        - `EMAIL`: Your email address.
        - `IMAP_PASSWORD`: Your IMAP password.
        - `IMAP_FOLDER`: The IMAP folder to search for emails (default is INBOX).

    - **SMTP Configuration**:
        - `SMTP_SERVER`: Your SMTP server address.
        - `SMTP_PORT`: Port number for SMTP server.
        - `EMAIL`: Your email address.
        - `SMTP_PASSWORD`: Your SMTP password.

    - **Nextcloud Configuration**:
        - `NEXTCLOUD_BASE_URL`: Base URL of your Nextcloud instance.
        - `NEXTCLOUD_DIRECTORY`: Default directory to save attachments in Nextcloud.
        - `NEXTCLOUD_USERNAME`: Your Nextcloud username.
        - `NEXTCLOUD_PASSWORD`: Your Nextcloud password.

## Usage

1. Create a text file named `extensions.txt` in the project directory with the list of allowed file extensions, one per line. Example:

    ```
    .pdf
    .png
    .jpg
    .jpeg
    .doc
    .docx
    .ppt
    .pptx
    .txt
    .csv
    .xlsx
    .xls
    .zip
    .7z
    .rar
    .gif
    .bmp
    .tif
    .tiff
    .rtf
    .mp3
    .wav
    .mp4
    .avi
    .mov
    .svg
    .odt
    .ods
    .odp
    .json
    .xml
    ```

2. Activate the conda environment:

    ```bash
    conda activate save-email-attachment
    ```

3. Run the script by executing the `email_attachment_to_nextcloud.py` file. It will continuously check for new emails, download attachments, and upload them to Nextcloud.

    ```bash
    python email_attachment_to_nextcloud.py
    ```

## Implementation Details

### Functions

1. **load_allowed_extensions(file_path='extensions.txt')**:
    - Loads the allowed file extensions from a text file.

2. **is_allowed_file(filename)**:
    - Checks if the file extension is allowed.

3. **save_attachment_to_nextcloud(attachment_path, nextcloud_directory)**:
    - Uploads the specified attachment to Nextcloud under the given directory.
    - Parameters:
        - `attachment_path`: Path to the attachment file.
        - `nextcloud_directory`: Destination directory in Nextcloud.
    
4. **fetch_new_emails(last_check_time)**:
    - Connects to the IMAP server, fetches emails from the specified folder, and processes them.
    - Extracts attachments from emails and saves them locally.
    - Uploads attachments to Nextcloud based on the email subjects.
    - Sends acknowledgment email for valid attachments.
    - Sends notification email for invalid file extensions if not already notified.

5. **send_acknowledgment_email(sender_email, saved_folder)**:
    - Sends an acknowledgment email to the sender notifying them that their files have been received and saved to Nextcloud.
    - Parameters:
        - `sender_email`: Email address of the sender.
        - `saved_folder`: Directory where the files are saved in Nextcloud.

6. **send_invalid_extension_email(sender_email)**:
    - Sends an email to the sender notifying them of an invalid file extension.
    - Parameters:
        - `sender_email`: Email address of the sender.
    
### IMAP Settings

- `IMAP_SERVER`: The IMAP server address.
- `IMAP_PORT`: Port number for IMAP server.
- `EMAIL`: Your email address.
- `IMAP_PASSWORD`: Your IMAP password.
- `IMAP_FOLDER`: The IMAP folder to search for emails (default is INBOX).

### SMTP Settings

- `SMTP_SERVER`: Your SMTP server address.
- `SMTP_PORT`: Port number for SMTP server.
- `SMTP_PASSWORD`: Your SMTP password.

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

# Save Email Attachment to Nextcloud - Using systemd

This script automates the process of extracting files from emails and saving them to Nextcloud.

1. Create a systemd service unit:

    ```bash
    sudo nano /etc/systemd/system/save-email-attachment.service
    ```

2. Modify the systemd service unit file `save-email-attachment.service` as follows:

    ```plaintext
    [Unit]
    Description=Script for extracting files from email and saving to Nextcloud
    After=network.target

    [Service]
    User=root
    Environment="PATH=/root/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    WorkingDirectory=/the directory where you cloned the repo/
    ExecStart=/bin/bash -lc 'source /root/miniconda3/etc/profile.d/conda.sh && conda activate save-email-attachment && /root/miniconda3/envs/save-email-attachment/bin/python email_attachment_to_nextcloud.py'
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

3. Reload systemd and start the service:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start save-email-attachment.service
    ```

## Additional Notes

- To stop the service:

    ```bash
    sudo systemctl stop save-email-attachment.service
    ```

- To enable the service to start automatically at boot:

    ```bash
    sudo systemctl enable save-email-attachment.service
    ```

- To check the service status:

    ```bash
    sudo systemctl status save-email-attachment.service
    ```

---