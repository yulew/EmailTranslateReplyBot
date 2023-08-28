from imaplib import IMAP4_SSL
from typing import Optional
from env_config_loader import IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD

class EmailConnectionError(Exception):
    """Exception raised when unable to connect to the email server."""


def connect_to_server(imap_server: Optional[str] = None,
                      email_address: Optional[str] = None,
                      email_password: Optional[str] = None) -> IMAP4_SSL:
    """
    Connect to an IMAP server and log in.

    :param imap_server: Address of the IMAP server.
    :param email_address: Email address for login.
    :param email_password: Email password for login.
    :return: IMAP4_SSL object if successful, raises an exception otherwise.
    """
    imap_server = imap_server or IMAP_SERVER
    email_address = email_address or EMAIL_ADDRESS
    email_password = email_password or EMAIL_PASSWORD

    try:
        mail = IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        print(f"Successfully logged in to the server using the email address {email_address}.")
        return mail
    except Exception as e:
        raise EmailConnectionError(f"Error connecting to server: {str(e)}")


if __name__ == '__main__':
    emails = connect_to_server()
    # Further processing of emails
