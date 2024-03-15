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
    pip install requests python-dotenv
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


If you're using an `.env` file for storing passwords and credentials, you can adjust the README accordingly. Here's the updated README:

---

# Save Email Attachment to Nextcloud - Using systemd

This script automates the process of extracting files from emails and saving them to Nextcloud.

## Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system

## Installation

1. Clone this repository to your local machine:

2. Navigate to the project directory:

    ```bash
    cd save_email_attachment_to_nextcloud
    ```

3. Create a conda environment and install dependencies:

    ```bash
    conda env create -f environment.yml
    ```

## Usage

1. Activate the conda environment:

    ```bash
    conda activate save-email-attachment
    ```

2. Create a systemd service unit: 

    ```bash
    sudo nano /etc/systemd/system/save-email-attachment.service
    ```

3. Modify the systemd service unit file `save-email-attachment.service` as follows:

    ```plaintext
    [Unit]
    Description=Script for extracting files from email and saving to Nextcloud
    After=network.target

    [Service]
    User=root
    Environment="PATH=/root/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    WorkingDirectory=/the directory where you cloned the repo/
    ExecStart=/bin/bash -lc 'source /root/miniconda3/etc/profile.d/conda.sh && conda activate save-email-attachment && /root/miniconda3/envs/save-email-attachment/bin python savefile.py'
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

4. Reload systemd and start the service:

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

- To check the service to start automatically at boot:

    ```bash
    sudo systemctl status save-email-attachment.service
    ```
