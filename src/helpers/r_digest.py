from logger.logger import event_logger

def inspect_headers(request, query):
    event_logger.debug(f"Inspecting header object for request ID {query.request_id}")

    headers_dict = dict(request.headers)
    event_logger.info(f"{query.request_id} Headers: {headers_dict}")
