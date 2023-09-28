import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from environs import Env  # Import Env from environs

# Load environment variables from the .env file
env = Env()
env.read_env()

# Retrieve the IMAP password from the environment
imap_password = env("IMAP_PASSWORD")
sendgrid_apikey = env("SENDGRID_APIKEY")

# IMAP settings
imap_server = 'imap.migadu.com'
imap_port = 993
username = 'erds@monachapel.org'


sg = sendgrid.SendGridAPIClient(api_key=sendgrid_apikey)
from_email = Email("notices@monachapel.org")  # Change to your verified sender
to_email = To("david.bain@incrementic.com")  # Change to your recipient


# List of allowed sender email addresses
allowed_senders = env("ALLOWED_SENDERS").split(',')

# Connect to the IMAP server with the retrieved password
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, imap_password)
mail.select("inbox")  # Select the inbox folder

# Calculate the date 3 days ago from today
three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%d-%b-%Y")

# Search for emails with subjects containing "[hello]" sent in the last 3 days
subject_to_trigger = "[hello]"  # Updated subject criteria
search_criteria = f'(SINCE "{three_days_ago}")'
status, email_ids = mail.search(None, search_criteria)

if status == "OK":
    email_ids = email_ids[0].split()
    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status == "OK":
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # Check if the subject contains "[hello]" (case-insensitive)
            if "[notices]" in subject.lower():
                # Check if the sender is in the list of allowed senders
                sender = msg.get("From", "")
                if any(allowed_sender in sender for allowed_sender in allowed_senders):
                    # Print a message indicating that a matching email from an allowed sender is found
                    message = f"Found an email from '{sender}' with the subject: '{subject}'"
                    subject = "We got a message"
                    content = Content("text/plain", f"{message} ... and easy to do anywhere, even with Python")
                    sgmail = Mail(from_email, to_email, subject, content)
                    mail_json = sgmail.get()

                    # Send an HTTP POST request to /mail/send
                    response = sg.client.mail.send.post(request_body=mail_json)
                    print(response.status_code)
                    print(response.headers)

else:
    print("Failed to search for emails.")

# Logout from the IMAP server
mail.logout()
