# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Restyle existing tables from Home · #2164](https://github.com/genspark-ai/genoffice/pull/2164)**<br>I routed a second Format as Table style selection through the existing restyle handler, preserving the table instead of reporting an overlap. Regressions reopen saved XLSX files; Chromium verifies the actual Univer model. Windows Beta rendering was not tested. |
| **Merged** | **[Inline equation indentation · #2148](https://github.com/genspark-ai/genoffice/pull/2148)**<br>I isolated inline math from inherited paragraph indentation and alignment, following the issue reporter’s diagnosis. Chromium editor and HTML export checks verify the geometry; save/reopen retains OMML and paragraph formatting. |
| **Merged** | **[Clickable Markdown graph close button · #2138](https://github.com/genspark-ai/genoffice/pull/2138)**<br>I excluded the close button from Electron’s native window drag region so a mouse click reaches its existing handler. Native mouse input on macOS verified the source-revert failure and patched success while keeping the editor open; Windows installers were not tested. |
| **Merged** | **[Single active home navigation entry · #2135](https://github.com/genspark-ai/genoffice/pull/2135)**<br>I made the current content view determine the highlighted sidebar entry and aria-current, so opening Ask AI from Recent or Starred selects only Ask AI. React interaction regressions and light/dark Chromium checks cover the transitions. |
| **Merged** | **[DFKai-SB PostScript font alias · #2025](https://github.com/genspark-ai/genoffice/pull/2025)**<br>I mapped the exact PDFMaker font name to DFKai-SB so PDF-to-Word output retains the installed family name. Synthetic PDFium-to-DOCX tests verify the text and Word font fields. |
| **Merged** | **[Watermarks across active section headers · #2057](https://github.com/genspark-ai/genoffice/pull/2057)**<br>I applied watermark updates to active default, first-page and even-page headers across sections, preserving linked headers and existing content. Removing watermarks no longer creates empty headers. Synthetic DOCX regressions verify structure and relationships. |
| **Merged** | **[Modern sheet-protection metadata · #2075](https://github.com/genspark-ai/genoffice/pull/2075)**<br>I corrected Rust enum-field serialization to match the strict desktop IPC contract, allowing worksheets with modern protection metadata to load. Synthetic XLSX tests use the actual native sidecar; legacy and password-free protection remain compatible. |
| **Merged** | **[Footer statistics menu targeting · #2083](https://github.com/genspark-ai/genoffice/pull/2083)**<br>I restricted the statistics menu to the sheet footer so right-clicking the grid keeps only the cell menu. The tab strip and editable controls retain their existing behavior. DOM regressions and the actual Sheets renderer verify the routing. |

The watermark fix has not been visually checked in Word/LibreOffice; picture auto-fit retains its existing final-section sizing behavior.

The font-alias change covers the font-name case only, not the remaining character-spacing issue or Windows visual rendering.

This change concerns worksheet protection metadata, not file-level Excel encryption or password prompts.

The menu fix does not change Univer dismissal logic. Windows’ two-Escape symptom was not reproduced, and a separate direct-click dismissal check left the cell menu visible.
