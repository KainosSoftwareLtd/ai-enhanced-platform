import os
import logging

logger = logging.getLogger(__name__)

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
    logger.info(f"PROMPT FILE IS: {system_prompt_file}")
    # Retrieve the AZURE_CS_KEY from environment variables
    azure_cs_key = os.environ.get("AZURE_CS_KEY")
    # Retrieve the AZURE_CS_ENDPOINT from environment variables
    azure_cs_endpoint = os.environ.get("AZURE_CS_ENDPOINT")
    # Retrieve ALLOWED_FILE_TYPES from environment variables
    allowed_file_types = os.environ.get("ALLOWED_FILE_TYPES", "png, jpg, jpeg")
    # Retrieve the APPINSIGHTS_KEY from environment variables
    appinsights_key = os.environ.get("APPINSIGHTS_KEY")
    # Retrieve the LOGGING_LEVEL from environment variables
    logging_level = os.environ.get("LOGGING_LEVEL", "INFO")
    # Retrieve the OTEL_LIVE_METRICS_ENABLED from environment variables
    otel_live_metrics_enabled = (os.environ.get("OTEL_LIVE_METRICS_ENABLED") == 'True')
    # Retrieve the OTEL_DISABLE_OFFLINE_STORAGE from environment variables
    otel_disable_offline_storage = (os.environ.get("OTEL_DISABLE_OFFLINE_STORAGE") == 'True')

except Exception as e:
    logger.error(f"Unable to retrieve environment variables. Make sure the .env file exists and has the correct permissions. Exception: {e}")
