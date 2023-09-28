Assumptions:

- We are picking up mail from Migadu's imap servers
- We only accept mail from allowed senders.

Usage:

Create an .env file similar to this:
```
IMAP_PASSWORD="xxxxxxxxxx"
IMAP_USER="xxxxxxxxxxx"
ALLOWED_SENDERS="davidin@example.com,sender1@example.com,sender2@example.com"
SENDGRID_APIKEY="SGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxx"
```

The script runs twice a day and looks for emails that have been sent to `IMAP_USER`. 
It must match a specific pattern and com from a specific sender.
