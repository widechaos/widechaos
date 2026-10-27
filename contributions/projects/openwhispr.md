# OpenWhispr

[← All projects](../README.md) · [Upstream repository](https://github.com/OpenWhispr/openwhispr)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Hyprland configuration updates · #2742](https://github.com/OpenWhispr/openwhispr/pull/2742)**<br>I fixed Hyprland configuration updates to respect sourced loader files and write configuration atomically. The maintainer extended nested-loader and settings-failure coverage; those additions retain their authorship. |
| **Merged** | **[Uploaded transcripts and mobile note tabs · #2880](https://github.com/OpenWhispr/openwhispr/pull/2880)**<br>I saved uploaded speech in the transcript field and kept the mobile Transcript tab alongside editable notes after a summary is generated. The maintainer added speaker/timing preservation and desktop acceptance checks. Historical-upload migration and transcript search indexing remain outside this change. |
| **Under review** | **[Voice Assistant prompt selection · #2629](https://github.com/OpenWhispr/openwhispr/pull/2629)**<br>Use the Voice Assistant custom prompt in its panel while keeping typed Chat prompts separate. The existing conversational default stays in place when no custom prompt is set. |
| **Merged** | **[Saved speaker edits in notes · #2672](https://github.com/OpenWhispr/openwhispr/pull/2672)**<br>Use the saved transcript with speaker edits when generating notes after transcription stops. Active transcription keeps the live input. |
