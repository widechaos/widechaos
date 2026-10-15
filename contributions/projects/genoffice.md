# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[DFKai-SB PostScript font alias · #2025](https://github.com/genspark-ai/genoffice/pull/2025)**<br>I mapped the exact PDFMaker font name to DFKai-SB so PDF-to-Word output retains the installed family name. Synthetic PDFium-to-DOCX tests verify the text and Word font fields. |

This change covers the font-name case only, not the remaining character-spacing issue or Windows visual rendering.
