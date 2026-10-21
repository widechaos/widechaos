# Ekko Studio

[← All projects](../README.md) · [Upstream repository](https://github.com/EKKOLearnAI/ekko-studio)

| Status | Contribution |
| :--- | :--- |
| **Under review** | **[Named-profile model picker · #3343](https://github.com/EKKOLearnAI/ekko-studio/pull/3343)**<br>Show inherited root OAuth providers in named-profile model pickers without copying or refreshing credentials. |
| **Merged** | **[Managed MCP credential inheritance · #3359](https://github.com/EKKOLearnAI/ekko-studio/pull/3359)**<br>Prevent stale parent bearer tokens from overriding the current profile credential in built-in managed MCP subprocesses. |
| **Merged** | **[Thinking reply visibility · #3365](https://github.com/EKKOLearnAI/ekko-studio/pull/3365)**<br>Keep an unfinished leading thinking block out of the settled chat reply. |
| **Merged** | **[Scrollable category submenu · #3374](https://github.com/EKKOLearnAI/ekko-studio/pull/3374)**<br>Keep every category reachable in the session context menu, including in short windows. |
| **Merged** | **[Cross-profile attachment runs · #3439](https://github.com/EKKOLearnAI/ekko-studio/pull/3439)**<br>I made attachment runs use their authorized run profile while preserving stored-session profile and user-access checks. Actual handler regressions cover allowed runs and denied profile/path cases. |
| **Under review** | **[Hermes CLI display versions · #3444](https://github.com/EKKOLearnAI/ekko-studio/pull/3444)**<br>I switched discovery to the canonical display-version API with legacy fallback, preserving stamp and Git identities instead of showing the placeholder version. |
| **Merged** | **[Completed-abort thinking indicator · #3473](https://github.com/EKKOLearnAI/ekko-studio/pull/3473)**<br>Stop the thinking indicator and timer after abort completion while keeping active runs and pending aborts visible. Session-switch residue and broader resume races remain outside this fix. |
| **Merged** | **[Unicode tool-result boundaries · #3457](https://github.com/EKKOLearnAI/ekko-studio/pull/3457)**<br>Keep UTF-16 surrogate pairs intact at tool-context truncation boundaries. Existing malformed sessions and provider-specific errors remain outside this fix. |

The attachment fix is limited to run requests; other cross-profile approval, abort and queue operations are unchanged. Handler tests use synthetic sessions and a stub agent rather than a real Socket.IO transport. CLI discovery tests do not cover Windows launcher paths or installation and upgrade flows.
