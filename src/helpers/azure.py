from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import helpers.config as config
import logging

logger = logging.getLogger(__name__)

# Build Key Vault Secret Client Object
def build_secret_client():
    if config.azure_vault_id is not None:
        if config.debug_on:
            logger.debug("Building Azure Key Vault Secret Client.")
        try:
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=config.azure_vault_id, credential=credential)

            return secret_client

        except Exception as e:
            logger.info(f"Failed to build DefaultAzureCredential {e}")
    else:
        return None
