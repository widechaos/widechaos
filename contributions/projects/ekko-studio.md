# Ekko Studio

[← All projects](../README.md) · [Upstream repository](https://github.com/EKKOLearnAI/ekko-studio)

| Status | Contribution |
| :--- | :--- |
| **Under review** | **[Task-plan field contract · #3530](https://github.com/EKKOLearnAI/ekko-studio/pull/3530)**<br>I documented the canonical step shape and clarified missing-field diagnostics without changing accepted inputs. |
| **Under review** | **[Device-manager exit · #3732](https://github.com/EKKOLearnAI/ekko-studio/pull/3732)**<br>I added a localized Close action and Escape dismissal to the native device manager. Headless checks cover the close path; macOS fullscreen and Spaces behavior remains unverified. |
| **Merged** | **[Empty STT proxy results · #3753](https://github.com/EKKOLearnAI/ekko-studio/pull/3753)**<br>I kept successful empty OpenAI-compatible transcripts from becoming proxy errors, while retaining upstream and malformed-response failures. Real HTTP route tests use synthetic audio bytes and a mock upstream; voice configuration sync is unchanged. |
| **Merged** | **[Consolidated chat system instructions · #3728](https://github.com/EKKOLearnAI/ekko-studio/pull/3728)**<br>I consolidated system instructions at the OpenAI chat request boundary, preserving instruction order and tool constraints for strict compatible backends. |
| **Merged** | **[Indexed pending Person deliveries · #3723](https://github.com/EKKOLearnAI/ekko-studio/pull/3723)**<br>I added a guarded origin-session index and aligned the pending-delivery query to avoid repeated scans while tolerating malformed legacy JSON. |

| **Under review** | **[Named-profile model picker · #3343](https://github.com/EKKOLearnAI/ekko-studio/pull/3343)**<br>Show inherited root OAuth providers in named-profile model pickers without copying or refreshing credentials. |

[All 2026 contributions and scope notes](ekko-studio/2026.md)
