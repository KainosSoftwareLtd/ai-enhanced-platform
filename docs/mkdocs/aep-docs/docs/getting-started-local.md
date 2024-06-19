# Getting Started - local

Here's how to run the API locally.

- [Getting Started](#getting-started)
  - [Secrets Setup](#secrets-setup)
    - [Requirements](#requirements)
      - [Start Server](#start-server)
    - [Docker](#docker)
      - [Build and Run](#build-and-run)

## Secrets Setup

To run the API locally, you will need to create a `.env` file in the root of the project with the following content:

```
OPENAI_API_TYPE=<openai_api_type>
OPENAI_MODEL=<openai_model>
AZURE_OPENAI_ENDPOINT=<azure_openai_endpoint>
OPENAI_API_KEY=<openai_api_key>
SYSTEM_API_KEY=<system_api_key>
AZURE_VAULT_ID=<azure_vault_id>
AZURE_CS_ENDPOINT=<azure_cs_endpoint>
AZURE_CS_KEY=<azure_cs_key>
```

The `OPENAI_API_TYPE` can be either `openai` or `azure`.
The `OPENAI_MODEL` can be either `gpt-4-turbo` or `gpt-35-turbo`.
The `AZURE_OPENAI_ENDPOINT` is the Azure OpenAI endpoint.
The `OPENAI_API_KEY` is the OpenAI or Azure API key.
The `SYSTEM_API_KEY` is the system API key you can use to authenticate as the 'system' consumer.
The `AZURE_VAULT_ID` is your Azure Key Vault ID where consumer keys are stored.
The `AZURE_CS_ENDPOINT` is the Azure Cognitive Services Content Safety endpoint.
The `AZURE_CS_KEY` is the Azure Cognitive Services Content Safety key.

### Requirements

To install the requirements:

```
make build-local
```

This installs:

```
-- fastapi
-- uvicorn
-- requests
-- pytest
-- openai
-- python-dotenv
-- azure-identity
-- azure-keyvault-secrets
-- starlette
-- tiktoken
-- prometheus_fastapi_instrumentator
-- pydantic-core
```

#### Start Server
```
make run-local
```

### Docker
To run the API using Docker, you can use the following commands:

#### Build and Run
```
make build
make run
```