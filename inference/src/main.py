from fastapi import FastAPI, HTTPException, Request
from prompt_cleanse import classify
import logging
from pydantic import BaseModel

event_logger = logging.getLogger("event_logger")

app = FastAPI()

# define pydantic model for injection check request
class InjectionCheck(BaseModel):
    prompt_string: str

# GET - api root
@app.get("/")
def hello(request: Request):
    event_logger.info("Prompt Cleanse API is running")
    return {"message": "Prompt Cleanse API is running"}

# POST - prompt injection check
@app.post("/injection-check")
async def injection_check(request: Request, query: InjectionCheck):

    # get consumer id from headers
    consumer_id = request.headers.get("X-API-CONSUMER")
    if consumer_id is None:
        consumer_id = "unknown"

    event_logger.info(f"Consumer ID: {consumer_id} | Running prompt injection check")

    # Load classifier
    classifier = classify.configure_classifier()

    # Pass prompt string to classifier and return result
    result = classify.classify_injection(classifier, query.prompt_string)

    # if result is populated, pass too decision classifier
    if result is not None:
        decision = classify.classify_decision(result)
        if decision['result'] == 'ERROR':
            event_logger.error(f"Consumer ID: {consumer_id} | Error occurred during decision classification")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            event_logger.info(f"Consumer ID: {consumer_id} | Decision: {decision['result']} | Reason: {decision['reason']} | Score: {decision['score']}")
            return decision
