# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Hyperlink frame and document location · #2982](https://github.com/genspark-ai/genoffice/pull/2982)**<br>I preserved imported hyperlink attributes through nearby text edits, including the editor save path and distinct adjacent links. Real DOCX round trips and editor regressions pass; native Word was not tested. |
| **Merged** | **[Literal dollars in lists and shapes · #2979](https://github.com/genspark-ai/genoffice/pull/2979)**<br>I kept dollar sequences literal when saving numbering labels and the first text in shapes without body properties. Synthetic package and text-generation regressions verify exact text on reopen. |
| **Merged** | **[Picture links in nested header parts · #2978](https://github.com/genspark-ai/genoffice/pull/2978)**<br>I resolved picture relationships beside nested header and footer parts so external target edits retain the embedded image. Real package regressions verify links, PNG bytes and untouched content. |
| **Merged** | **[Pictures with empty relationship roots · #2976](https://github.com/genspark-ai/genoffice/pull/2976)**<br>I expanded self-closing empty relationship roots before appending header or footer picture targets. Real package round trips verify image relationships and reopening while preserving untouched parts. |
| **Merged** | **[Fast wheel zoom gesture context · #2923](https://github.com/genspark-ai/genoffice/pull/2923)**<br>I moved fast fixed-notch recognition into the shared classifier and removed the Docs-only bypass so varying Ctrl/Cmd swipe tails stay suppressed. Synthetic regressions cover Docs, Sheets and Slides; native input hardware was not tested. |
| **Merged** | **[Comments on PDF text markups · #2896](https://github.com/genspark-ai/genoffice/pull/2896)**<br>I exposed saved comments on Highlight, Underline, Squiggly and StrikeOut annotations and preserved their original identity through replies, edits, deletion and save/reopen. Real PDF-byte regressions verify the four supported types; no native Preview or Acrobat session was tested. |

[All 2026 contributions and scope notes](genoffice/2026.md)
