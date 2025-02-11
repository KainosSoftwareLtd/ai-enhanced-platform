FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN mkdir logs

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
