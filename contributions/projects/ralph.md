# Ralph

[← All projects](../README.md) · [Upstream repository](https://github.com/frankbria/ralph-claude-code)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Production-function regression tests · #380](https://github.com/frankbria/ralph-claude-code/pull/380)**<br>I replaced copied implementations in exit-detection, rate-limit, and session-reset tests with the production functions, so implementation regressions are detected. |
| **Under review** | **[Unused bootstrap generator removal · #377](https://github.com/frankbria/ralph-claude-code/pull/377)**<br>Remove the unused bootstrap generator that embedded outdated scripts. |

The maintainer independently confirmed that all seven tested production mutations were caught and added a safety-breaker regression. That additional regression is the maintainer’s contribution.
