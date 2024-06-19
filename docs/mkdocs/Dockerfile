From python:3.12

COPY ./aep-docs /aep-docs/

WORKDIR /aep-docs/

run pip install --no-cache-dir --upgrade mkdocs mkdocs-gitbook mkdocs-material

CMD ["mkdocs", "serve", "--dev-addr", "0.0.0.0:8000"]
