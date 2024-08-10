import os
from dotenv import load_dotenv 

load_dotenv()

from contextlib import asynccontextmanager
from uuid import uuid1, UUID
from fastapi import FastAPI, HTTPException, Request
from pydantic.fields import Field
from logger.logger import event_logger, request_logger
from helpers.prompts import read_prompt, retrieve_prompts, reduce_prompt_tokens, check_for_prompt_inj
from helpers.open_ai import call_openai
from helpers.r_digest import inspect_headers
import helpers.config as config
from middleware.auth import authenticate
from pydantic import BaseModel
from middleware import metrics


# Define pydantic model and include unique id per request
class PredefinedQuery(BaseModel):
    prompt_type: str
    prompt: str
    request_id: UUID = Field(default_factory=uuid1)

# Define pydantic model and include unique id per request
class CustomQuery(BaseModel):
    system_prompt: str
    user_prompt: str
    prompt: str
    compression_enabled: bool = False
    model: str = config.openai_model
    request_id: UUID = Field(default_factory=uuid1)

class NoQuery(BaseModel):
    request_id: UUID = Field(default_factory=uuid1)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    if config.debug_on:
        event_logger.info("Started AEP API Service in DEBUG mode")
    else:
        event_logger.info("Started AEP API Service")
    yield

app = FastAPI(lifespan=app_lifespan)

# Apply the authentication middleware to the app
app.middleware('http')(authenticate)
# Instrument application with Prometheus metrics
metrics.begin_instrumentation(app)

# GET - API Root
@app.get("/")
def hello(request: Request):
    event_logger.info(f"Request ID: API Root Called")
    if config.debug_on:
        inspect_headers(request, NoQuery())
    try:
        prompt_list = retrieve_prompts()
        return prompt_list
    except Exception as err:
        event_logger.error(f"Error: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# POST - Match against a prompt from the dictionary and return the response
@app.post("/predefined")
async def create_predefined_query(request: Request, query: PredefinedQuery):
    if config.debug_on:
        inspect_headers(request, query)

    # Read in prompts defined for vulnerability checks and make call to OpenAI
    try:
        prompt_dict = read_prompt(query.prompt_type, query.request_id, query.prompt)
    except Exception as err:
        event_logger.info(f"Request ID: {query.request_id} | Error: {err}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Request ID: {query.request_id}")
    
    # Check for prompt injection
    result = check_for_prompt_inj(prompt_dict["prompt"])
    if not result:
        event_logger.warning(f"Possible malicious content detected, including prompt injection in request ID: {query.request_id}")
        raise HTTPException(status_code=400, detail=f"Bad Request: Possible malicious content detected in prompt. If you believe this is a mistake, reference: {query.request_id}")
    event_logger.info(f"Checked for injection")

    response = call_openai(prompt_dict["system"], prompt_dict["user"], prompt_dict["prompt"], prompt_dict["model"])

    # If response is not successful, raise a 500 status code and log error in logs/requests.log
    if not response["success"]:
        error = response["error"]
        request_logger.info(f"Request ID: {query.request_id} | Error: {error} | Time Elapsed: {response['time']}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Request ID: {query.request_id} | Error: {error}")
    else: 
        request_logger.info(f"Request ID: {query.request_id} | Successful: True | Time Elapsed: {response['time']}")
        return response["data"]

# POST - Read in a custom prompt and return the response
@app.post("/custom")
async def create_info_query(request: Request, info_query: CustomQuery):
    if config.debug_on:
        inspect_headers(request, info_query)

    # If compression is enabled, reduce the prompt tokens
    if info_query.compression_enabled:
        info_query.prompt = reduce_prompt_tokens(info_query.prompt)
    
    # Check for prompt injection
    result = check_for_prompt_inj(info_query.prompt)
    if not result:
        event_logger.warning(f"Possible malicious content detected, including prompt injection in request ID: {info_query.request_id}")
        raise HTTPException(status_code=400, detail=f"Bad Request: Possible malicious content detected in prompt. If you believe this is a mistake, reference: {info_query.request_id}")
    event_logger.info(f"Checked for injection")

    # Read in custom prompt defined in the request and make call to OpenAI
    response = call_openai(info_query.system_prompt, info_query.user_prompt, info_query.prompt, info_query.model)

    # If response is not successful, raise a 500 status code and log error in logs/requests.log
    if not response["success"]:
        error = response["error"]
        request_logger.error(f"Request ID: {info_query.request_id} | Error: {error} | Time Elapsed: {response['time']}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Request ID: {info_query.request_id}")
    else: 
        request_logger.info(f"Request ID: {info_query.request_id} | Successful: True | Time Elapsed: {response['time']}")
        return response["data"]
    
# GET - Healthcheck endpoint
@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


