from opentelemetry import trace, baggage
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPSpanGrpcExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource, HOST_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind


def inner_method():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("child_span", kind=SpanKind.CLIENT):
        print("hello world")


def outer_method():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("parent_span", kind=SpanKind.SERVER):
        inner_method()


def baggage_and_attribute_usage():
    tracer = trace.get_tracer(__name__)
    global_ctx = baggage.set_baggage("key", "value_from_global_ctx")  # 使用baggage api，在不同span之间传递数据
    with tracer.start_as_current_span(name='baggage_parent_span', attributes={'attribute_key': 'value'},
                                      kind=SpanKind.SERVER):
        parent_ctx = baggage.set_baggage("key", "value_from_parent_ctx")
        with tracer.start_as_current_span(name='baggage_child_span', context=parent_ctx,
                                          kind=SpanKind.INTERNAL):
            child_ctx = baggage.set_baggage("key", "value_from_child_ctx")

    print(baggage.get_baggage("key", global_ctx))
    print(baggage.get_baggage("key", parent_ctx))
    print(baggage.get_baggage("key", child_ctx))


def init_opentelemetry():
    # 设置服务名、主机名
    resource = Resource(attributes={
        SERVICE_NAME: "PythonTest",
        HOST_NAME: "MyComputer",
        "token": "xxxxxxxxxx"  # 替换成控制台上的 Token
    })

    # 使用GRPC协议上报
    span_processor = BatchSpanProcessor(OTLPSpanGrpcExporter(
        endpoint="http://ap-guangzhou.apm.tencentcs.com:4317",  # 替换成控制台上的接入点
    ))

    trace_provider = TracerProvider(resource=resource, active_span_processor=span_processor)
    trace.set_tracer_provider(trace_provider)


if __name__ == '__main__':
    init_opentelemetry()
    outer_method()
    baggage_and_attribute_usage()
