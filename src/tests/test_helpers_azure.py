import os
import pytest
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

class TestAzure:
    def setup_class(self):
       self.vault_url = os.getenv("AZURE_VAULT_ID")

    def test_default_azure_credential(self):
        credential = DefaultAzureCredential()
        assert isinstance(credential, DefaultAzureCredential)

    def test_secret_client(self):
        secret_client = SecretClient(vault_url=self.vault_url, credential=DefaultAzureCredential())
        assert isinstance(secret_client, SecretClient)

if __name__ == '__main__':
    pytest.main()