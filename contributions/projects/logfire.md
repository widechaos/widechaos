# Logfire

[← All projects](../README.md) · [Upstream repository](https://github.com/pydantic/logfire)

| Status | Contribution |
| :--- | :--- |
| **Under review** | **[Parent-span metrics · #2533](https://github.com/pydantic/logfire/pull/2533)**<br>Include metrics from sampled-out child spans in their recording parents, without exporting the children. |
| **Merged** | **[CLI global tracing · #2611](https://github.com/pydantic/logfire/pull/2611)**<br>Keep the CLI tracer provider local so application OpenTelemetry spans export correctly under `logfire run`, while preserving tracing on CLI API requests. |
| **Under review** | **[Anthropic message iterators · #2588](https://github.com/pydantic/logfire/pull/2588)**<br>Avoid consuming one-shot message iterators during instrumentation, leaving iteration to the SDK. |
