from typing import Optional, Sequence, Union
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import (
    REGISTRY, CollectorRegistry, Histogram,
    Counter
)

class Info:
    def __init__(
        self, 
        request: Request, 
        response: Optional[Response],
        method: str,
        handler: str,
        status: str,
        duration: float
    ) -> None:
        self.request = request
        self.response = response
        self.method = method
        self.handler = handler
        self.status = status
        self.duration = duration


def latency(
    metric_name: str ='http_request_duration_seconds',
    metric_doc: str = "Duration of HTTP requests in seconds",
    metric_namespace: str = "",
    buckets: Sequence[Union[float, str]] = Histogram.DEFAULT_BUCKETS,
    registry: CollectorRegistry = REGISTRY,
):
    if buckets[-1] != float("inf"):
        buckets = [*buckets, float("inf")]
    
    labelnames = ["handler", "method", "status"]


    metric = Histogram(
        name=metric_name,
        documentation=metric_doc,
        namespace=metric_namespace,
        labelnames=labelnames,
        buckets=buckets,
        registry=registry
    )

    def instrumentation(info: Info):
        label_values = [
            getattr(info, attribute_name)
            for attribute_name in labelnames
        ]
        metric.labels(*label_values).observe(info.duration)
    
    return instrumentation


def rps(
    metric_name: str ='http_requests_total',
    metric_doc: str = "Total number of requests by method, status and handler.",
    metric_namespace: str = "",
    registry: CollectorRegistry = REGISTRY,
):
    labelnames = ["handler", "method", "status"]
    
    metric = Counter(
        name=metric_name,
        documentation=metric_doc,
        namespace=metric_namespace,
        labelnames=labelnames,
        registry=registry
    )

    def instrumentation(info: Info):
        label_values = [
            getattr(info, attribute_name)
            for attribute_name in labelnames
        ]
        metric.labels(*label_values).inc()
    
    return instrumentation

    