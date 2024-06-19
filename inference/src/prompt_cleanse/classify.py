from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import logging
import torch

event_logger = logging.getLogger("event_logger")

def configure_classifier():
    event_logger.info("Configuring classifier")
    
    # load tokeniser and model for sequence classification
    tokenizer = AutoTokenizer.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection-v2")
    model = AutoModelForSequenceClassification.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection-v2")

    # create classifier object
    classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    truncation=True,
    max_length=512,
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    )

    event_logger.info("Classifier configured")
    return classifier


def classify_injection(classifier, prompt_string):
    result = classifier(prompt_string)
    return result


def classify_decision(result):
    # retrieve result label and score
    result_label = result[0]["label"]
    result_score = result[0]["score"]

    try:
        if result_label == "INJECTION":
            print("Prompt Injection has been detected")
            return {
                "result": "FAIL",
                "reason": "Prompt injection has been detected",
                "score": {result_score}
            }
        elif result_label == "SAFE":
            print("No malicious tokens have been found")
            return {
                "result": "PASS",
                "reason": "No malicious tokens have been found",
                "score": {result_score}
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "result": "ERROR",
            "reason": "An error has occurred",
            "score": 0
        }
