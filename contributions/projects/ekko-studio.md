# Ekko Studio

[← All projects](../README.md) · [Upstream repository](https://github.com/EKKOLearnAI/ekko-studio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Broker startup from worker shells · #3915](https://github.com/EKKOLearnAI/ekko-studio/pull/3915)**<br>I isolated broker startup from inherited worker endpoints and identity while preserving custom broker configuration and explicitly pinned clients. Local socket/process regressions passed for my patch. Upstream added stale-worker recovery and Desktop/Python launch safeguards; I did not retest those additions or validate Windows and the real Hermes runtime. |
| **Merged** | **[Responses reasoning effort · #3884](https://github.com/EKKOLearnAI/ekko-studio/pull/3884)**<br>I preserve request reasoning effort during Responses-to-Chat conversion when the route has no valid override. Explicit route settings, including none, still win. Converter and proxy regressions cover both streaming modes; a separate contributor reported deployment verification on 0.8.29. |
| **Merged** | **[Rolling-summary account context · #3885](https://github.com/EKKOLearnAI/ekko-studio/pull/3885)**<br>I bind background base summaries to the persisted, authorized room owner only when caller scope is absent. Tests cover permission rejection and concurrent account isolation. Legacy rooms without an owner and optional JEV summary revision remain outside this fix. |
| **Merged** | **[Configured memory approval limits · #3872](https://github.com/EKKOLearnAI/ekko-studio/pull/3872)**<br>I made write approval load configured memory limits through the runtime loader. Offline tests cover actual approval and atomic rejection with synthetic data and the public runtime; native UI was not tested. |
| **Merged** | **[Plugin host context optionals · #3827](https://github.com/EKKOLearnAI/ekko-studio/pull/3827)**<br>I kept optional host context fields from aborting plugin-enabled conversations while preserving strict plugin-return validation. Tests use the actual runtime with an in-memory plugin; the packaged Windows app and third-party plugin were not tested. |
| **Under review** | **[Task-plan field contract · #3530](https://github.com/EKKOLearnAI/ekko-studio/pull/3530)**<br>I documented the canonical step shape and clarified missing-field diagnostics without changing accepted inputs. |
| **Under review** | **[Device-manager exit · #3732](https://github.com/EKKOLearnAI/ekko-studio/pull/3732)**<br>I added a localized Close action and Escape dismissal to the native device manager. Headless checks cover the close path; macOS fullscreen and Spaces behavior remains unverified. |
| **Merged** | **[Empty STT proxy results · #3753](https://github.com/EKKOLearnAI/ekko-studio/pull/3753)**<br>I kept successful empty OpenAI-compatible transcripts from becoming proxy errors, while retaining upstream and malformed-response failures. Real HTTP route tests use synthetic audio bytes and a mock upstream; voice configuration sync is unchanged. |
| **Merged** | **[Consolidated chat system instructions · #3728](https://github.com/EKKOLearnAI/ekko-studio/pull/3728)**<br>I consolidated system instructions at the OpenAI chat request boundary, preserving instruction order and tool constraints for strict compatible backends. |
| **Merged** | **[Indexed pending Person deliveries · #3723](https://github.com/EKKOLearnAI/ekko-studio/pull/3723)**<br>I added a guarded origin-session index and aligned the pending-delivery query to avoid repeated scans while tolerating malformed legacy JSON. |

| **Under review** | **[Named-profile model picker · #3343](https://github.com/EKKOLearnAI/ekko-studio/pull/3343)**<br>Show inherited root OAuth providers in named-profile model pickers without copying or refreshing credentials. |

[All 2026 contributions and scope notes](ekko-studio/2026.md)
