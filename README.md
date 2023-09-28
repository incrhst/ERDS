# ERDS - Email Reading and Distribution Script

> Warning: This is "almost-works-ware". It is scheduled to be "works-ware" by mid October 2023.

## Purpose:
Provide the simplest possible email distribution list. An authorised user sends an email to a single email address and this triggers a script which does the rest of distribution. The final version will retrieve the email list using the API of the Breeze Church Management System.

## Assumptions:

- We are picking up mail from Migadu's imap servers
- We only accept mail from allowed senders.
- The script uses Python 3

## Installation
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> On some systems such as Linux on Chromebooks, Python 3 uses the command `python3` instead of `python`
## Usage:

Create an .env file similar to this:
```
IMAP_PASSWORD="xxxxxxxxxx"
IMAP_USER="xxxxxxxxxxx"
ALLOWED_SENDERS="davidin@example.com,sender1@example.com,sender2@example.com"
SENDGRID_APIKEY="SGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxx"
```

The script runs twice a day and looks for emails that have been sent to `IMAP_USER`. 
It must match a specific pattern and com from a specific sender.

Once setup, simply run the script using the command:

```
python main.py
```