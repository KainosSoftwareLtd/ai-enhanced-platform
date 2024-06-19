# Usage

## Authentication

AEP ensures secure access through flexible authentication mechanisms:

1. **LOCAL AUTHENTICATION**: If the API is running locally, you can use the `.env` file to set the `'system'` user API key.
	* If the `X-API-CONSUMER` is `'system'` then the local API key will be used.


2. **AZURE AUTHENTICATION**: If the API is running in Azure, it will use the Azure Key Vault to get the API key.
	* If the `X-API-CONSUMER` is anything other than `'system'` then the Azure Key Vault will be used.
	* A lookup will be used to get the API key from the Key Vault using the `X-API-CONSUMER` as the identifier.

## Endpoints

### `GET /`

Root endpoint and will return a list of available system prompts with their descriptions.

### `POST /predefined`

Retrieve prompts based on predefined types, providing parameters for customised assessment:

- `prompt_type`The name of the predefined prompt to use.
- `prompt`: The content that you want the model to assess based on the predefined prompt type.

### `POST /custom` 

Tailor prompts to your specific needs using custom system and user prompts for precise model guidance:

- `system_prompt`: The system prompt is used to orient the model towards a personality or desired output.
- `user_prompt`: The user prompt should tell the model what it is you want it to do with the prompt.
- `prompt`: The content that you want the model to assess based on the custom prompt.
- `compression_enabled`(optional): Compresses the input prompt to reduce the number of tokens. Default is false.
- `model`(optional): The model you want to use as a string, currently available ["gpt-4-turbo", "gpt-35-turbo"]. Default is 'gpt-35-turbo'.