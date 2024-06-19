import time
import helpers.config as config
import helpers.prompts as prompts
from openai import OpenAI, OpenAIError, AzureOpenAI
from logger.logger import event_logger
from middleware.metrics import update_last_request_time

def call_openai(system_prompt, user_prompt, query, model):
  tic = time.perf_counter()
  if config.debug_on:
    event_logger.debug("Loading environment variables")

  # Check if OpenAI or Azure is being used
  if config.openai_api_type == "openai":
    if config.debug_on:
      event_logger.debug("OpenAI type is openai")
    client = OpenAI(api_key=config.openai_api_key)
  elif config.openai_api_type == "azure":
    if config.debug_on:
      event_logger.debug("OpenAI type is azure")
    try:
      client = AzureOpenAI(api_key=config.openai_api_key, api_version=config.azure_openai_api_version, azure_endpoint=config.azure_openai_endpoint)
    except Exception as e:
      event_logger.error(f"Failed to create AzureOpenAI client {e}")
  else:
    event_logger.error("Cannot determine whether client is OpenAI or Azure.")
  
  # Attempt call to OpenAI
  try:
    event_logger.info("Calling "+config.openai_api_type+" API")
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
    event_logger.error(err)
    return {"success": False, "error": str(err), "time": f"0.0"}

  except Exception as err:
    event_logger.error(err)
    return {"success": False, "error": str(err), "time": f"0.0"}
