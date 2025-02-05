from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Gauge, Counter
from typing import Callable
import logging 

logger = logging.getLogger(__name__)

# custom AEP metrics
last_request_time_elapsed = Gauge('last_request_time_elapsed', 'Time elapsed for last request')
number_of_tokens_saved = Gauge('number_of_tokens_saved', 'Number of tokens saved in last request')
perc_of_tokens_saved = Gauge('perc_of_tokens_saved', 'Percent of tokens saved in last request')

# add custom handler for requests per consumer id
def requests_per_consumer() -> Callable[[Info], None]:
    METRIC = Counter(
        "requests_per_consumer",
        "Number of requests per consumer",
        labelnames=("consumer_id",)
    )

    def instrumentation(info: Info) -> None:
        consumer_ids = set()
        consumer_str = info.request.headers.get("x-api-consumer")
        for item in consumer_str.split(","):
            item = item.split(";")[0].strip().lower()
            consumer_ids.add(item)
        for consumer_id in consumer_ids:
            METRIC.labels(consumer_id).inc()

    return instrumentation

# begin instrumentation
def begin_instrumentation():
    logger.info("Beginning metric insrumentation")

    # define instrumentator
    instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=False,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    ).add(metrics.latency(
    )).add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="a",
        metric_subsystem="b",
    )).add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="namespace",
        metric_subsystem="subsystem",
    )).add(metrics.default(
    )).add(requests_per_consumer())

    return instrumentator


def update_last_request_time(last_request_time: int):
    last_request_time_elapsed.set(last_request_time)

def update_number_of_tokens_saved(no_of_tokens: int):
    number_of_tokens_saved.set(no_of_tokens)

def update_perc_of_tokens_saved(perc_of_tokens: int):
    perc_of_tokens_saved.set(perc_of_tokens)
