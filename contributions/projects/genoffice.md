# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[DFKai-SB PostScript font alias · #2025](https://github.com/genspark-ai/genoffice/pull/2025)**<br>I mapped the exact PDFMaker font name to DFKai-SB so PDF-to-Word output retains the installed family name. Synthetic PDFium-to-DOCX tests verify the text and Word font fields. |

| **Merged** | **[Watermarks across active section headers · #2057](https://github.com/genspark-ai/genoffice/pull/2057)**<br>I applied watermark updates to active default, first-page and even-page headers across sections, preserving linked headers and existing content. Removing watermarks no longer creates empty headers. Synthetic DOCX regressions verify structure and relationships. |

The watermark fix has not been visually checked in Word/LibreOffice; picture auto-fit retains its existing final-section sizing behavior.

The font-alias change covers the font-name case only, not the remaining character-spacing issue or Windows visual rendering.

| **Merged** | **[Modern sheet-protection metadata · #2075](https://github.com/genspark-ai/genoffice/pull/2075)**<br>I corrected Rust enum-field serialization to match the strict desktop IPC contract, allowing worksheets with modern protection metadata to load. Synthetic XLSX tests use the actual native sidecar; legacy and password-free protection remain compatible. |

This change concerns worksheet protection metadata, not file-level Excel encryption or password prompts.
