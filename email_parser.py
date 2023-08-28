from typing import Dict, Any
import email
import email.header
from bs4 import BeautifulSoup


def email_parser(email_data: Any) -> Dict[str, Any]:
    """
    Parse email data to extract relevant information.

    :param email_data: Raw email data.
    :return: Dictionary containing email details.
    """
    raw_email = email_data[0][1]

    # Parsing the raw email
    message = email.message_from_bytes(raw_email)

    # Extracting headers
    from_address = message['From']
    to_address = message['To']
    subject = email.header.decode_header(message['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode('utf-8')

    # Initializing body
    body = ""

    # Extracting the body
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Skip any text/plain (txt) attachments
            if "attachment" not in content_disposition:
                if content_type == "text/html":
                    body = part.get_payload(decode=True).decode()
                    body = extract_html_text(body)
                elif content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()

    else:
        # Not multipart - i.e., plain text, no attachments
        body = message.get_payload(decode=True).decode()

    return {
        "to_address": to_address,
        "from_address": from_address,
        "subject": subject,
        "body": body
    }


def extract_html_text(html_content: str) -> str:
    """
    Extract text content from HTML.

    :param html_content: Raw HTML content.
    :return: Text content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


if __name__ == "__main__":
    from email_puller import fetch_emails

    email_server_data = fetch_emails()
    print(email_server_data)

    for server in email_server_data:
        result, fetched_email_data = server['result'], server['email_data']
        if result == 'OK':
            parsed_email = email_parser(fetched_email_data)
            email_message = parsed_email["from_address"], parsed_email["subject"], parsed_email["body"]
            print(f'body: {email_message}\n')
