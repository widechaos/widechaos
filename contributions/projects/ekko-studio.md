# Ekko Studio

[← All projects](../README.md) · [Upstream repository](https://github.com/EKKOLearnAI/ekko-studio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Streamed tool-call identity · #3647](https://github.com/EKKOLearnAI/ekko-studio/pull/3647)**<br>I preserved tool-call IDs and names across empty continuation chunks while keeping argument fragments intact. Local HTTP/SSE regressions cover the reported shape; no live provider account was used. |
| **Merged** | **[Public Agent availability for Workflow and Group Chat · #3546](https://github.com/EKKOLearnAI/ekko-studio/pull/3546)**<br>I moved Agent selection to public execution eligibility while retaining administrator inventory permissions and Hermes executable-path checks. Role-route and headless page tests use synthetic fixtures. |
| **Merged** | **[Safe group-routing failure diagnostics · #3498](https://github.com/EKKOLearnAI/ekko-studio/pull/3498)**<br>I added bounded routing diagnostics without logging message bodies, credentials or provider responses. This does not add persistent decisions for every failure or diagnose the reporter's exact incident. |

| **Under review** | **[Named-profile model picker · #3343](https://github.com/EKKOLearnAI/ekko-studio/pull/3343)**<br>Show inherited root OAuth providers in named-profile model pickers without copying or refreshing credentials. |

[All 2026 contributions and scope notes](ekko-studio/2026.md)
