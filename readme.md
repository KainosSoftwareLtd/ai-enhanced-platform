# AEP: AI Enhanced Platform

![Kainos AEP](docs/kainos_aep_header.png)

[![aep](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/actions/workflows/run-test-suite.yml/badge.svg)](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/actions/workflows/run-test-suite.yml)

Welcome to AEP, your comprehensive solution for integrating Generative AI workflows into your build system. Enhance your DevOps processes with AI-driven pull request summarization, code reviews, and more.

Get your API key and revolutionize your DevOps journey with AI-powered insights and assistance today. 🚀

Website: [AEP Docs](https://kainossoftwareltd.github.io/ai-enhanced-platform/)

## Features of AEP

AEP currently offers the following features:

- **AI-Driven Pull Request Summary**: Automatically generate summaries of your pull requests using AI.
- **AI-Driven Pull Request Insights**: Obtain AI-driven insights on DevOps tasks and identify potential vulnerabilities.
- **Custom AI-Driven Prompts**: Customize prompts for specific needs using tailored system and user prompts for precise model guidance.

## Usage

### Authentication

AEP provides secure access through flexible authentication mechanisms:

1. **Local Authentication**: 
   - Use the `.env` file to set the 'system' user API key when running the API locally.
   - If `X-API-CONSUMER` is 'system', the local API key will be used.

2. **Azure Authentication**: 
   - When running the API in Azure, it retrieves the API key from the Azure Key Vault.
   - If `X-API-CONSUMER` is not 'system', the Azure Key Vault is used, with the `X-API-CONSUMER` acting as the identifier.

### Endpoints

#### GET /

Returns a list of available system prompts with their descriptions.

#### POST /predefined

Retrieve prompts based on predefined types, with parameters for customized assessment:
- `prompt_type`: The predefined prompt to use.
- `prompt`: The content for the model to assess based on the predefined prompt type.

#### POST /custom

Customize prompts for specific needs using system and user prompts:
- `system_prompt`: Directs the model towards a desired output.
- `user_prompt`: Specifies the desired action for the prompt.
- `prompt`: The content for the model to assess based on the custom prompt.
- `compression_enabled` (optional): Compresses the input prompt to reduce token count (default: false).
- `model` (optional): The model to use, currently available options are ["gpt-4-turbo", "gpt-35-turbo"] (default: 'gpt-35-turbo').

## Local Development

### Secrets Setup

Create a `.env` file in the root of the project with the following content:

```
OPENAI_API_KEY=<your_openai_api_key>
SYSTEM_API_KEY=<your_system_api_key>
AZURE_VAULT_ID=<your_azure_key_vault_id>
```

### Local Setup

Install the required dependencies and start the server using the following commands:

#### Requirements

To install the dependencies:

```
make build-local
```

Dependencies include:
- fastapi
- uvicorn
- requests
- pytest
- openai
- python-dotenv
- azure-identity
- azure-keyvault-secrets
- starlette
- tiktoken
- prometheus_fastapi_instrumentator
- pydantic-core

#### Start Server

To start the server:

```
make run-local
```

### Docker

To run the API using Docker, use the following commands:

#### Build and Run

```
make build
make run
```

## Terraform Setup and Usage

This project uses Terraform to manage infrastructure. Terraform scripts are located in the `terraform/envs/stable` directory.

### Prerequisites

- Terraform >= 0.14
- Azure CLI
- Make

### Environment Variables

Set the following environment variables:

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

### Linting

Lint your Terraform scripts to catch syntax or formatting issues:

```
make tf-lint
```

To automatically fix some issues:

```
make tf-fmt
```

### Initialization

Initialize your Terraform working directory:

```
make tf-init
```

### Planning

Create an execution plan to see the actions Terraform will perform:

```
make tf-plan
```

### Applying

Apply the changes to reach the desired state:

```
make tf-apply
```


### Destroying

Destroy all resources managed by Terraform:

```
make tf-destroy
```

Note: This command will remove all resources in your Azure subscription managed by Terraform.

## Continuous Deployment

This project uses GitHub Actions for continuous deployment. The workflow is defined in `.github/workflows/deploy-terraform.yml`. On each push to the main branch, the workflow lints, initializes, plans, and applies Terraform changes. Ensure required environment variables are set in your GitHub repository secrets.

## Metrics and Monitoring

The application is instrumented with `Prometheus FastAPI Instrumentator`. Enable metrics collection by setting the `ENABLE_METRICS` environment variable to `True`. Metrics can then be scraped from the `/metrics` path.

## Contributing

We welcome contributions to AEP! To contribute, please follow these steps:

1. **Fork the repository**: Create a fork of the repository on GitHub.

2. **Clone the repository**: Clone your fork locally.
    ```
    git clone https://github.com/your-username/ai-enhanced-platform.git
    ```

3. **Create a branch**: Create a new branch for your feature or bugfix.
    ```
    git checkout -b feature/your-feature-name
    ```

4. **Make your changes**: Implement your changes and commit them with descriptive messages.
    ```
    git commit -m "Add feature/your-feature-name: description of changes"
    ```

5. **Push to GitHub**: Push your changes to your forked repository.
    ```
    git push origin feature/your-feature-name
    ```

6. **Create a Pull Request**: Open a pull request against the main repository. Provide a detailed description of your changes and any relevant context.

7. **Review Process**: Your pull request will be reviewed by project maintainers. Please be responsive to feedback and make any necessary adjustments.

8. **Merge**: Once approved, your pull request will be merged into the main branch.

Thank you for contributing to AEP!
