from typing import Optional, Any, Union, List

from imap_connection import connect_to_server


def fetch_email_ids(mail, fetch_option: Union[str, int]) -> List[str]:
    try:
        limit = None  # Initialize limit
        if fetch_option == 'unread':
            status, email_ids = mail.search(None, 'UNSEEN')
            if not email_ids[0]:
                print("No unread emails. Fetching all emails instead.")
                status, email_ids = mail.search(None, 'ALL')
                if len(email_ids[0].split()) > 20:
                    limit = input(
                        "Fetching all unread emails may use a lot of memory. Limit the number? Enter a number or 'No': ")
                    email_ids = ' '.join(email_ids[0].decode().split()[-int(limit):])
        elif isinstance(fetch_option, int):
            status, all_email_ids = mail.search(None, 'ALL')
            email_ids = ' '.join(all_email_ids[0].decode().split()[-fetch_option:])
        elif fetch_option == 'all':
            status, email_ids = mail.search(None, 'ALL')
            if len(email_ids[0].split()) > 20:
                limit = input("Fetching all emails may use a lot of memory. Limit the number? Enter a number or 'No': ")
                if limit.lower() != 'no':
                    email_ids = ' '.join(email_ids[0].decode().split()[-int(limit):])
        else:
            print("Invalid fetch option.")
            return []

        if status != 'OK':
            print("Failed to fetch email IDs.")
            return []

        return email_ids[0].split()

    except Exception as e:
        print(f"Error fetching email IDs: {str(e)}")  # Replace with proper logging
        return []

def fetch_emails(imap_server: Optional[str] = None,
                 email_address: Optional[str] = None,
                 email_password: Optional[str] = None,
                 fetch_option=5) -> Any:
    """
    Fetch emails from the server.

    :param imap_server: Address of the IMAP server.
    :param email_address: Email address for login.
    :param email_password: Email password for login.
    :return: Processed email data or raises an exception if unable to connect.
    """
    # If imap_server is not provided, use default credentials to connect
    if imap_server is None:
        mail = connect_to_server()
    # If imap_server is provided, use the specified credentials to connect
    else:
        mail = connect_to_server(imap_server, email_address, email_password)

    # Select the 'inbox' folder in the email account
    mail.select('inbox')

    # Fetch email IDs and process emails
    email_ids = fetch_email_ids(mail, fetch_option)
    if email_ids == []:
        print("No emails to load.")
        return []
    result_email_data = iter(
        [{'email_id': e_id, 'result': mail.fetch(e_id, '(RFC822)')[0], 'email_data': mail.fetch(e_id, '(RFC822)')[1]} for e_id in
         email_ids])  # If 'result' is not 'ok', print "cannot fetch e_id"

    print("Emails successfully fetched.")
    return result_email_data


if __name__ == '__main__':
    emails = fetch_emails()
    print(list(emails))
    # Further processing of emails
