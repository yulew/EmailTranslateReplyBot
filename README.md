# Email Auto-Translate and Auto-Reply Package

This package provides tools to automatically translate and reply to emails using OpenAI's large language models (LLMs).

## Features

- **Automated Email Replies**: Automatically generate replies for incoming emails.
- **Translation Support**: Offers support for multiple languages, enabling translation to English and facilitating diverse communication requirements.
- **Easy Integration**: Seamlessly integrates with popular email services.

## Requirements

- Python 3.6 +
- IMAP-enabled email account
- [OpenAI API key](https://platform.openai.com/account/api-keys)

## Setup

1. Rename `.env.example` to `.env`. You can execute the following command in your terminall:
    ```bash
    cp .env.example .env
    ```
   
2. Open `.env` and fill in your own values for each key
    ```
    IMAP_SERVER='Your_IMAP_Server'
    EMAIL_ADDRESS='Your_Email_Address'
    EMAIL_PASSWORD='Your_Email_Password'
    OPENAI_API_KEY='Your_OpenAI_API_Key'
    ```
3. To install the necessary packages, run the following commands in your terminal:

   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   conda install -r requirements.txt
   ```
## Run the codes

To automatically reply to and translate your emails, execute the following commands in your terminal.

   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.