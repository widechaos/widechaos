# Ralph

[← All projects](../README.md) · [Upstream repository](https://github.com/frankbria/ralph-claude-code)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Unused bootstrap generator removal · #377](https://github.com/frankbria/ralph-claude-code/pull/377)**<br>Remove the unused bootstrap generator that embedded outdated scripts. |
| **Merged** | **[Single root-config upload · #390](https://github.com/frankbria/ralph-claude-code/pull/390)**<br>I kept the root config in the E2B upload list once, preserving its original order and the allowlist fallback. Actual local upload tests use a capturing transport; cloud E2B behavior was not tested. |
| **Merged** | **[Production-function regression tests · #380](https://github.com/frankbria/ralph-claude-code/pull/380)**<br>I replaced copied implementations in exit-detection, rate-limit, and session-reset tests with the production functions, so implementation regressions are detected. |

The maintainer independently confirmed that all seven tested production mutations were caught and added a safety-breaker regression. That additional regression is the maintainer’s contribution.
