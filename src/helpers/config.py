import os
from logger.logger import event_logger

try:
    # Retrieve the OPENAI_API_KEY from environment variables
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    # Retrieve the SYSTEM_API_KEY from environment variables
    system_api_key = os.environ.get("SYSTEM_API_KEY")
    # Retrieve the AZURE_VAULT_ID from environment variables
    azure_vault_id = os.environ.get("AZURE_VAULT_ID")
    # Retrieve the OPENAI_API_TYPE from environment variables, if not set default to openai
    openai_api_type = os.environ.get("OPENAI_API_TYPE", "openai")
    # Retrieve the name of the model to be used, if not set default to gpt-3.5-turbo
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    # Retrieve the AZURE_OPENAI_API_VERSION from environment variables
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    # Retrieve the AZURE_OPENAI_ENDPOINT from environment variables
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    # Retrieve the DEBUG_ON from environment variables
    debug_on = (os.environ.get("DEBUG_ON") == 'True')
    # Retrieve the PROMPT_FILE from environment variables
    system_prompt_file = os.environ.get("SYSTEM_PROMPT_FILE", "system_prompts/prompts.json")
    event_logger.info(f"PROMPT FILE IS: {system_prompt_file}")
    # Retrieve the AZURE_CS_KEY from environment variables
    azure_cs_key = os.environ.get("AZURE_CS_KEY")
    # Retrieve the AZURE_CS_ENDPOINT from environment variables
    azure_cs_endpoint = os.environ.get("AZURE_CS_ENDPOINT")

except:
    event_logger.error(f"Unable to retrieve environment variables. Make sure the .env file exists and has the correct permissions.")
