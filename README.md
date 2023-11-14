### 安装所需的依赖包
``` bash
pip install django
pip install requests
pip install opentelemetry-distro \
	opentelemetry-exporter-otlp
 
opentelemetry-bootstrap -a install
```

### 上报 Python 应用数据
1. 引入 OpenTelemetry SDK 依赖，进行 SDK 埋点上报，首先对 trace 进行构造。

   ``` python
   from opentelemetry import trace, baggage
   from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPSpanGrpcExporter
   from opentelemetry.sdk.resources import SERVICE_NAME, Resource, HOST_NAME
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.sdk.trace.export import BatchSpanProcessor
   
   def init_opentelemetry():
       # 设置服务名、主机名
       resource = Resource(attributes={
           SERVICE_NAME: "your-service-name",
           HOST_NAME: "your-host-name",
           "token": "xxxxxxxxxx" # 此处替换成控制台中获得的 Token
       })
   
       # 使用GRPC协议上报
       span_processor = BatchSpanProcessor(OTLPSpanGrpcExporter(
           endpoint="http://ap-guangzhou.apm.tencentcs.com:4317", # 此处替换成控制台中获得的接入点信息
       ))
   
       trace_provider = TracerProvider(resource=resource, active_span_processor=span_processor)
       trace.set_tracer_provider(trace_provider)
   ```
2. 在业务代码执行前，进行 trace 的初始化。

   ``` python
   if __name__ == '__main__':
       init_opentelemetry()
       # 写一些业务方法
   ```
### 完整接入文档可参考 [腾讯云观测平台官方文档](https://cloud.tencent.com/document/product/248/101072)。

