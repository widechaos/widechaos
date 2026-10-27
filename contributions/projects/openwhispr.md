# OpenWhispr

[← All projects](../README.md) · [Upstream repository](https://github.com/OpenWhispr/openwhispr)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Hyprland configuration updates · #2742](https://github.com/OpenWhispr/openwhispr/pull/2742)**<br>I fixed Hyprland configuration updates to respect sourced loader files and write configuration atomically. The maintainer extended nested-loader and settings-failure coverage; those additions retain their authorship. |
| **Merged** | **[Uploaded transcripts and mobile note tabs · #2880](https://github.com/OpenWhispr/openwhispr/pull/2880)**<br>I saved uploaded speech in the transcript field and kept the mobile Transcript tab alongside editable notes after a summary is generated. The maintainer added speaker/timing preservation and desktop acceptance checks. Historical-upload migration and transcript search indexing remain outside this change. |
| **Under review** | **[Voice Assistant prompt selection · #2629](https://github.com/OpenWhispr/openwhispr/pull/2629)**<br>Use the Voice Assistant custom prompt in its panel while keeping typed Chat prompts separate. The existing conversational default stays in place when no custom prompt is set. |
| **Merged** | **[Saved speaker edits in notes · #2672](https://github.com/OpenWhispr/openwhispr/pull/2672)**<br>Use the saved transcript with speaker edits when generating notes after transcription stops. Active transcription keeps the live input. |
| **Under review** | **[Selection completion markers · #2700](https://github.com/OpenWhispr/openwhispr/pull/2700)**<br>I ended request markers at the complete random nonce while retaining strict parser checks. This addresses marker formatting only. |
| **Under review** | **[KDE shortcut conflict queries · #2751](https://github.com/OpenWhispr/openwhispr/pull/2751)**<br>I used the single-key KGlobalAccel compatibility query and corrected owner identification, preserving best-effort fallback behavior. |
| **Under review** | **[Gemini-compatible endpoint routing · #2873](https://github.com/OpenWhispr/openwhispr/pull/2873)**<br>I preserved the compatible base URL and routed raw cleanup to Chat Completions. Thinking-control compatibility remains outside this change. |
