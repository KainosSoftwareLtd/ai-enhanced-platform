import logging

logger = logging.getLogger(__name__)

def inspect_headers(request, query):
    logger.debug(f"Inspecting header object for request ID {query.request_id}")

    headers_dict = dict(request.headers)
    logger.info(f"{query.request_id} Headers: {headers_dict}")
