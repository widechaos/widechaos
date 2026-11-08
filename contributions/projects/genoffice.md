# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Nonblocking recent-file probes · #2541](https://github.com/genspark-ai/genoffice/pull/2541)**<br>I moved background recent-file metadata checks off the main thread and kept startup menus from probing unavailable paths. Offline filesystem tests preserve ordering, paging and unavailable entries. |
| **Merged** | **[Worksheet-level table parts · #2511](https://github.com/genspark-ai/genoffice/pull/2511)**<br>I kept new table parts at worksheet level when conditional-formatting rules contain nested extension lists. Round-trip tests preserve the original CF and x14 payload bytes. Clearing protected x14 formatting remains refused; this does not resolve all of #2510. |
| **Merged** | **[Save As with an unusable default folder · #2433](https://github.com/genspark-ai/genoffice/pull/2433)**<br>I kept Docs Save As available when its optional default directory cannot be used. Real IPC and filesystem tests preserve the selected file bytes; silent saves keep their existing directory checks. |

[All 2026 contributions and scope notes](genoffice/2026.md)
