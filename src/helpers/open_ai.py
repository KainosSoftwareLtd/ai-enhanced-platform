import time
import helpers.config as config
import helpers.prompts as prompts
from openai import OpenAI, OpenAIError, AzureOpenAI
from middleware.metrics import update_last_request_time
import logging
import requests

logger = logging.getLogger(__name__)

def call_openai(system_prompt, user_prompt, query, model):
  tic = time.perf_counter()
  if config.debug_on:
    logger.debug("Loading environment variables")

  # Check if OpenAI or Azure is being used
  if config.openai_api_type == "openai":
    if config.debug_on:
      logger.debug("OpenAI type is openai")
    client = OpenAI(api_key=config.openai_api_key)
  elif config.openai_api_type == "azure":
    if config.debug_on:
      logger.debug("OpenAI type is azure")
    try:
      client = AzureOpenAI(api_key=config.openai_api_key, api_version=config.azure_openai_api_version, azure_endpoint=config.azure_openai_endpoint)
    except Exception as e:
      logger.error(f"Failed to create AzureOpenAI client {e}")
  else:
    logger.error("Cannot determine whether client is OpenAI or Azure.")
  
  # Attempt call to OpenAI
  try:
    logger.info("Calling "+config.openai_api_type+" API")
    # add prompt delimiter
    query_delimiter = f"```{query}```"
    completion = client.chat.completions.create(
      model=model,
      messages=[
       {"role": "system", "content": system_prompt},
       {"role": "user", "content": user_prompt + query_delimiter}
      ]
    )

    # Return first message choice if successful
    tic_elapsed = time.perf_counter() - tic
    update_last_request_time(tic_elapsed)
    return {"success": True, "data": completion.choices[0].message.content, "time": f"{tic_elapsed: .2f}"}

  # Catch exceptions and pass error back to main.py
  except OpenAIError as err:
    logger.error(err)
    return {"success": False, "error": str(err), "time": f"0.0"}


def call_ai_content_safety(prompt):
  """
  Check for prompt injection in a single chunk of the prompt.
  Args:
    chunk (str): The prompt to check for injection.
  """
  
  url = config.azure_cs_endpoint + "/contentsafety/text:shieldPrompt?api-version=2024-02-15-preview"
  headers = {
    'Ocp-Apim-Subscription-Key': config.azure_cs_key,
    'Content-Type': 'application/json'
  }

  # Use the prompt argument as the document value
  data = {
    "documents": [
      f"{prompt}"
    ]
  }

  # Make a POST request to the AI Content Safety API
  try:
    response = requests.post(url, headers=headers, json=data)
    # Log the response
    response_json = response.json()
    logger.info(f"Response from AI ContentSafety: {response_json}")
  except Exception as err:
    logger.error(f"{err}")
    logger.error("Failed to make request to AI Content Safety")
    return False

  # Check if attackDetected is True in documentsAnalysis
  try:
    if response_json['documentsAnalysis'][0]['attackDetected']:
      logger.info(f"Prompt injection Detected in: {prompt}")
      return False  # Fail if attackDetected is True
  except Exception as err:
    logger.error("Failed to check for prompt injection in response from AI Content Safety")
    logger.error(f"{err}")
    return False
  
  return True