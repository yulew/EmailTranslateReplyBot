from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI


def auto_reply(email_message, model='gpt-3.5-turbo', temperature=0):
    """
    Automatically generates a reply to a given email message using the specified model and temperature.

    :param email_message: The email message to which a reply is to be generated.
    :param model: The model name to be used for generating the reply (default is 'gpt-3.5-turbo').
                  You can set model='gpt-4' as it can better interpret the email content and decide
                  whether the email should be auto-replied.
    :param temperature: The temperature setting for the model's response generation (default is 0).
                        The higher the temperature, the more random and creative the GPT generation will be.

    :return: A dictionary containing two keys:
             - 'reply': The generated reply to the original email.
             - 'reply_confidence': A confidence score ranging from 0 to 1, indicating the appropriateness of an automatic reply.
               A score of 0 means a personalized response is needed, and a score of 1 means the email can be confidently auto-replied.

    Example return format:
    {
        'reply': 'Hello Love, I appreciate your kind words. Best, Yule.',
        'reply_confidence': '1'
    }
    """

    # Initialize the model
    model_instance = OpenAI(model_name=model, temperature=temperature)

    # Define the response schemas
    response_schemas = [
        ResponseSchema(name="reply", description="Reply to the original email."),
        ResponseSchema(name="reply_confidence",
                       description=("A confidence score to determine if an email should receive an automatic reply. "
                                    "A score of 0 indicates that the email requires a personalized response from the user. "
                                    "Conversely, a score of 1 means the email can be confidently auto-replied. "
                                    "For instance, if someone inquires about the best time to schedule a meeting with me, "
                                    "the score should be near 0 since my personal schedule is unknown."))
    ]

    # Initialize the output parser
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # Define the prompt template
    prompt = PromptTemplate(
        template=("Automatically reply to this email. "
                  "If you find a response inappropriate, especially in cases like an email explicitly stating not to respond, "
                  "assign a reply_confidence score of 0. However, still craft a response from my personal perspective."
                  "\n{format_instructions}\n{email_message}"),
        input_variables=["email_message"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    # Format the prompt with the email message
    formatted_prompt = prompt.format_prompt(email_message=email_message)

    # Get the model's response
    output = model_instance(formatted_prompt.to_string())
    output_dict = output_parser.parse(output)

    # Return the parsed output
    return output_dict


if __name__ == '__main__':
    import env_config_loader

    message = "Hello Yule.\n I love you! Will you marry me?\n Best, Love"
    resp = auto_reply(email_message=message)
    print(resp)
