# Logfire

[← All projects](../README.md) · [Upstream repository](https://github.com/pydantic/logfire)

| Status | Contribution |
| :--- | :--- |
| **Closed · unmerged** | **[Missing template dependency error · #2745](https://github.com/pydantic/logfire/pull/2745)**<br>I proposed deferring the missing-dependency error. The maintainer rejected that direction, and the PR was closed without merging. |
| **Under review** | **[Parent-span metrics · #2533](https://github.com/pydantic/logfire/pull/2533)**<br>Include metrics from sampled-out child spans in their recording parents, without exporting the children. |
| **Merged** | **[CLI global tracing · #2611](https://github.com/pydantic/logfire/pull/2611)**<br>Keep the CLI tracer provider local so application OpenTelemetry spans export correctly under `logfire run`, while preserving tracing on CLI API requests. |
| **Closed · unmerged** | **[Anthropic message iterators · #2588](https://github.com/pydantic/logfire/pull/2588)**<br>Avoid consuming one-shot message iterators during instrumentation, leaving iteration to the SDK. |
