# AEP: AI Enhanced Platform

[![aep](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/actions/workflows/run-test-suite.yml/badge.svg)](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/actions/workflows/run-test-suite.yml)

Welcome to AEP, your companion for enhancing your build system with Generative AI workflows. With AEP, you can effortlessly add GenAI enhanced pull requester summarisation, code reviews, and more. 

Request your API key and empower your DevOps journey with AI-driven insights and assistance today. 🚀

Website: [AEP Docs](https://fuzzy-adventure-p8nllom.pages.github.io/)

## Features of AEP

Currently, AEP supports the following features:

- **AI-Driven Pull Request Summary**: Get a summary of your pull request using AI.
- **AI-Driven Pull Request Insights**: Get AI-driven insights on DevOps tasks and vulnerabilities.
- **Custom AI-Driven Prompts**: Tailor prompts to your specific needs using custom system and user prompts for precise model guidance.

## Usage

## Authentication
AEP ensures secure access through flexible authentication mechanisms:
1. LOCAL AUTHENTICATION: If the API is running locally, you can use the `.env` file to set the 'system' user API key.
   1. If the X-API-CONSUMER is 'system' then the local API key will be used.
2. AZURE AUTHENTICATION: If the API is running in Azure, it will use the Azure Key Vault to get the API key.
   1. If the X-API-CONSUMER is anything other than 'system' then the Azure Key Vault will be used.
   2. A lookup will be used to get the API key from the Key Vault using the X-API-CONSUMER as the identifier.

## Endpoints

### GET /
Root endpoint and will return a list of available system prompts with their descriptions.

### POST /predefined
Retrieve prompts based on predefined types, providing parameters for customised assessment:
- `prompt_type`: The name of the predefined prompt to use.
- `prompt`: The content that you want the model to assess based on the predefined prompt type.

### POST /custom
Tailor prompts to your specific needs using custom system and user prompts for precise model guidance:
- `system_prompt`: The system prompt is used to orient the model towards a personality or desired output.
- `user_prompt`: The user prompt should tell the model what it is you want it to do with the prompt.
- `prompt`: The content that you want the model to assess based on the custom prompt.
- `compression_enabled`(optional): Compresses the input prompt to reduce the number of tokens. Default is false.
- `model`(optional): The model you want to use as a string, currently available ["gpt-4-turbo", "gpt-35-turbo"]. Default is 'gpt-35-turbo'.

## Local Development
### Secrets setup
To run the API locally, you will need to create a `.env` file in the root of the project with the following content:
```
OPENAI_API_KEY=<your_openai_api_key>
SYSTEM_API_KEY=<your_system_api_key>
AZURE_VAULT_ID=<your_azure_key_vault_id>
```

### Local Setup
To run the API locally, you can use the following commands:

#### Requirements
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


# Terraform Setup and Usage

This project uses Terraform to manage infrastructure. The Terraform scripts are located in the `terraform/envs/stable` directory.

## Prerequisites

- Terraform >= 0.14
- Azure CLI
- Make

### Environment Variables
The following environment variables are required to be set in your environment:
```
ARM_CLIENT_ID
ARM_CLIENT_SECRET
ARM_SUBSCRIPTION_ID
ARM_TENANT_ID
BACKEND_RESOURCE_GROUP
BACKEND_STORAGE_ACCOUNT
BACKEND_CONTAINER_NAME
OPENAI_API_KEY
SYSTEM_API_KEY
AZURE_VAULT_ID
```


## Linting

Before running any Terraform commands, it's a good practice to lint your Terraform scripts to catch any syntax or formatting issues. You can do this by running the following command:

```
make tf-lint
```

If the linting fails, you will need to fix the issues before you can proceed. You can also run the following command to automatically fix some of the issues:

```
make tf-fmt
```

## Initialization
Before you can apply any Terraform configuration, you need to initialize your Terraform working directory. You can do this by running the following command:

```
make tf-init
```

This command is also defined in the Makefile and it runs the init_terraform.sh script located in the buildscripts directory.


## Planning
The terraform plan command is used to create an execution plan. This step is necessary to see which actions Terraform will perform to reach the desired state defined in the Terraform scripts. 

You can do this by running the following command:

```
make tf-plan
```

## Applying
After planning, the next step is to apply the changes required to reach the desired state of the configuration, or the pre-determined set of actions generated by a terraform plan execution plan. 

You can do this by running the following command:

```
make tf-apply
```

## Destroying
If you want to destroy all resources created by Terraform, you can do this by running the following command:

```
make tf-destroy
```

Please note that this command will destroy all resources managed by Terraform in your Azure subscription.

## Continuous Deployment
This project is set up to use GitHub Actions for continuous deployment. The workflow is defined in .github/workflows/deploy-terraform.yml. On every push to the main branch, the workflow lints and initializes Terraform, creates an execution plan, and applies it. Ensure that the required environment variables are set in your GitHub repository secrets.

## Metrics and Monitoring
The application is instrumented with `Prometheus FastAPI Instrumentator`. In order to enable the collection of these metrics, the environment variable `ENABLE_METRICS` must be set to `True`. Once set, metrics can be scraped from the `/metrics` path.
