# Ekko Studio

[← All projects](../README.md) · [Upstream repository](https://github.com/EKKOLearnAI/ekko-studio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Consolidated chat system instructions · #3728](https://github.com/EKKOLearnAI/ekko-studio/pull/3728)**<br>I consolidated system instructions at the OpenAI chat request boundary, preserving instruction order and tool constraints for strict compatible backends. |
| **Merged** | **[Indexed pending Person deliveries · #3723](https://github.com/EKKOLearnAI/ekko-studio/pull/3723)**<br>I added a guarded origin-session index and aligned the pending-delivery query to avoid repeated scans while tolerating malformed legacy JSON. |
| **Merged** | **[Realtime voice playback identity · #3708](https://github.com/EKKOLearnAI/ekko-studio/pull/3708)**<br>I fixed replay after an in-place message ID change and added focused queue regressions. The maintainer extended the fix to object replacement, reconnect and history pagination, corrected the audio fixture, and supplied browser/Edge validation and the CI runner correction; those additions retain their authorship. |

| **Under review** | **[Named-profile model picker · #3343](https://github.com/EKKOLearnAI/ekko-studio/pull/3343)**<br>Show inherited root OAuth providers in named-profile model pickers without copying or refreshing credentials. |

[All 2026 contributions and scope notes](ekko-studio/2026.md)
