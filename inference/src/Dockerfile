FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt --use-deprecated=legacy-resolver

COPY . /app

RUN guardrails hub install hub://guardrails/detect_prompt_injection

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]