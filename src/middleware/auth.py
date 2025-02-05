import helpers.config as config
from helpers import azure
from fastapi import Depends, FastAPI, Header, HTTPException
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)


async def authenticate(request: Request, call_next):
    # Check if the request is a healthcheck, if so skip authentication
    if request.url.path == "/healthcheck":
        logger.info(f"Healthcheck request.")
        response = await call_next(request)
        return response
    
    try:
        # Check if the X-API-CONSUMER and X-API-KEY headers are set
        x_api_consumer = check_header_is_set(request.headers.get('X-API-CONSUMER'))
        x_api_key = check_header_is_set(request.headers.get('X-API-KEY'))

        # Check if the consumer is the system consumer
        if x_api_consumer == 'system' and x_api_key == config.system_api_key:
            logger.info(f"Authenticated system consumer.")
        # Else try to authenticate the consumer
        elif x_api_key == lookup_consumer_key(x_api_consumer):
            logger.info(f"Authenticated consumer {x_api_consumer}.")
        # If all else fails, return a 401
        else:
            logger.error(f"Failed to authenticate consumer {x_api_consumer}.")
            return Response(status_code=401)
    except Exception as e:
        logger.warning(f"Failed to authenticate. Error: {e}")
        return Response(status_code=401)

    response = await call_next(request)
    return response

# Check to see if the header is set
def check_header_is_set(header):
    if header is None:
        raise ValueError("Header not set")
    return header

# Get the consumer key from Azure Key Vault
def lookup_consumer_key(consumer_id):
    if config.debug_on:
        logger.debug(f"Looking up secret value for consumer {consumer_id}")

    secret_client = azure.build_secret_client() 
    # Get the secret value from Azure Key Vault
    secret_name = f"{consumer_id}"
    if secret_client:
        try:
            secret_value = secret_client.get_secret(secret_name).value
            return secret_value
        except Exception as e:
            logger.error(f"Failed to get secret from vault {e}")
    else: 
        logger.warning("Failed to create secret_client object")
        return None
