# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Save As with an unusable default folder · #2433](https://github.com/genspark-ai/genoffice/pull/2433)**<br>I kept Docs Save As available when its optional default directory cannot be used. Real IPC and filesystem tests preserve the selected file bytes; silent saves keep their existing directory checks. |
| **Merged** | **[PDF open buffer ownership · #2415](https://github.com/genspark-ai/genoffice/pull/2415)**<br>I preserved the source bytes when PDF.js transfers its input buffer, allowing the existing decryption path to open the reported PDF. Renderer checks confirm that read-only permissions remain intact. |
| **Merged** | **[CJK font selection slots · #2392](https://github.com/genspark-ai/genoffice/pull/2392)**<br>I added recognition for the reported CJK font families so font picks update the East Asian slot. Real ribbon and DOCX round-trip tests preserve independent Latin behavior and untouched parts; general glyph-coverage detection remains outside this fix. |

[All 2026 contributions and scope notes](genoffice/2026.md)
