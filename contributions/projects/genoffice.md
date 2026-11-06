# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Worksheet-level table parts · #2511](https://github.com/genspark-ai/genoffice/pull/2511)**<br>I kept new table parts at worksheet level when conditional-formatting rules contain nested extension lists. Round-trip tests preserve the original CF and x14 payload bytes. Clearing protected x14 formatting remains refused; this does not resolve all of #2510. |
| **Merged** | **[Save As with an unusable default folder · #2433](https://github.com/genspark-ai/genoffice/pull/2433)**<br>I kept Docs Save As available when its optional default directory cannot be used. Real IPC and filesystem tests preserve the selected file bytes; silent saves keep their existing directory checks. |
| **Merged** | **[PDF open buffer ownership · #2415](https://github.com/genspark-ai/genoffice/pull/2415)**<br>I preserved the source bytes when PDF.js transfers its input buffer, allowing the existing decryption path to open the reported PDF. Renderer checks confirm that read-only permissions remain intact. |

[All 2026 contributions and scope notes](genoffice/2026.md)
