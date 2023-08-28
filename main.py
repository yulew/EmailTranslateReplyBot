from auto_reply import auto_reply
from auto_translation import auto_translate
from email_parser import email_parser
from email_puller import fetch_emails
import env_config_loader

emails = fetch_emails()
for email in emails:
    email_id, result, email_data = email['email_id'], email['result'], email['email_data']
    if result != 'OK':
        print(f"Error fetching {email_id}")
        continue
    parsed_email = email_parser(email_data)
    from_address, subject, email_message = parsed_email["from_address"], parsed_email["subject"], parsed_email["body"]
    resp = auto_reply(email_message=email_message)
    auto_rep, auto_reply_score = resp["reply"], resp["reply_confidence"]
    auto_translation = auto_translate(email_message)
    print(f"Subject: {subject}\nFrom Address: from_address\n\n"
          f"Auto Translation:\n{auto_translation}\n\n"
          f"Auto Reply:\n{auto_rep}\n{'-' * 30}\n\n{'-' * 30}\n\n\n ")
