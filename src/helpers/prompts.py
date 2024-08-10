import json
import tiktoken
import re
from logger.logger import event_logger
import helpers.config as config
import helpers.open_ai as openai
from middleware.metrics import update_number_of_tokens_saved, update_perc_of_tokens_saved

def read_prompt(prompt_type, request_id, prompt):
    event_logger.info(f"Request ID: {request_id} Searching Prompt File")
    try: 
     with open(config.system_prompt_file, 'r', encoding='utf-8') as prompt_file:
        prompts = json.load(prompt_file)
        check_prompts = prompts[prompt_type]
        system_prompt = check_prompts["system-prompt"]
        user_prompt = check_prompts["user-prompt"]
        compression_enabled = check_prompts["compression_enabled"]
        model = check_prompts["model"]

        if compression_enabled:
          prompt = reduce_prompt_tokens(prompt)

        return { 'system': system_prompt, 'user': user_prompt, 'prompt': prompt, 'model': model}

    except(ValueError, FileNotFoundError) as err:
      event_logger.error(f"Request ID: {request_id} ERR: {err}")
      event_logger.error("Prompt file could not be found or is in an invalid format")
      
      return { 'system': '', 'user': '', 'prompt': '', 'model': ''}

def retrieve_prompts():
  try:
    with open(config.system_prompt_file, 'r', encoding='utf-8') as prompt_file:
      prompts = json.load(prompt_file)
      
      # Create an empty dictionary to store the prompt type and descriptions
      prompt_list = []

      # Iterate through the prompts and append the prompt type and description to the dictionary
      for prompt in prompts:
        prompt_list.append({
          'prompt_type': prompt,
          'description': prompts[prompt]['description'],
          'compression_enabled': prompts[prompt]['compression_enabled'],
          'model': prompts[prompt]['model']
        })
      
      return prompt_list

  except (ValueError, FileNotFoundError) as err:
    event_logger.error(f"ERR: {err}")
    event_logger.error("Prompt file could not be found or is in an invalid format")

    return []

def reduce_prompt_tokens(prompt):
    try:
      # Initialize a new variable to store the compressed prompt
      compressed_prompt = prompt
      # Remove comments
      compressed_prompt = re.sub(r'#.*', '', compressed_prompt)
      # Remove extra spaces
      compressed_prompt = re.sub(r'\s+', ' ', compressed_prompt)
      # Remove unnecessary special characters
      compressed_prompt = re.sub(r'\.{2,}', '.', compressed_prompt)

      # Initialize the tokenizer and get token savings
      enc = tiktoken.get_encoding("cl100k_base")
      token_count = len(enc.encode(prompt))
      new_token_count = len(enc.encode(compressed_prompt))
      event_logger.info(f"Total token saving is {(token_count - new_token_count)} | Percent is {((token_count - new_token_count) / token_count) * 100}%")
      # update number of tokens saved in last request metric
      update_number_of_tokens_saved(token_count - new_token_count)
      # update % of token savings in last request metric
      update_perc_of_tokens_saved(((token_count - new_token_count) / token_count) * 100)

      # Return the compressed prompt
      return compressed_prompt

    except Exception as err:
      event_logger.error(f"ERR: {err}")
      event_logger.error("Failed to reduce prompt tokens")
      # Return the original prompt if an error occurs
      return prompt
    

def check_for_prompt_inj(prompt): 
  """
  Check for prompt injection in the given prompt. 
  
  If the prompt contains more than 10000 unicode characters, it will be split into chunks of 10000 characters.

  If the prompt contains more than 100000 unicode characters, the function will return False.

  Args:
    prompt (str): The prompt to check for injection.
  Returns:
    bool: True if no prompt injection is detected, False otherwise.
  """
  # Calculate number of unicode characters in the prompt
  unicode_count = len(prompt.encode('utf-8'))

  # If the number of unicode characters exceeds 100000 then return False
  if unicode_count > 100000:
    event_logger.warning("Prompt contained more than 100000 unicode characters.")
    return False

  # If the number of unicode characters exceeds 10000 then split the prompt into chunks of 10000 characters
  if unicode_count > 10000:
    prompt = [prompt[i:i+10000] for i in range(0, len(prompt), 10000)]
  else:
    prompt = [prompt]

  # Loop through the number of prompt chunks and check for prompt injection if any return False then return False
  for chunk in prompt:
    result = openai.call_ai_content_safety(chunk)
    if not result:
      return False

  return True