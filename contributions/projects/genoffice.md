# GenOffice

[← All projects](../README.md) · [Upstream repository](https://github.com/genspark-ai/genoffice)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Headless export language · #2847](https://github.com/genspark-ai/genoffice/pull/2847)**<br>I initialized the saved language before headless document export. Real hidden DOCX-to-PDF checks cover saved preferences, environment override and locale fallback; missing author initials and PDF text-layer fragmentation remain separate. |
| **Merged** | **[Creation paragraph spacing · #2822](https://github.com/genspark-ai/genoffice/pull/2822)**<br>I preserve public paragraph spacing when creating slide elements, including explicit zero values and omitted fields. Real PPTX save/reopen regressions cover creation, editing and table-cell controls; native PowerPoint was not tested. |
| **Merged** | **[Conformant new-document AppVersion · #2802](https://github.com/genspark-ai/genoffice/pull/2802)**<br>I corrected the default DOCX producer-version format while preserving explicit options and imported metadata. Real package round trips preserve every other OPC payload; the [reporter confirmed](https://github.com/genspark-ai/genoffice/issues/2801#issuecomment-6945025374) that the corrected document opens in Word for Mac 16.115, with its heading, list and footer intact. |
| **Merged** | **[Bounded NSS certificate reads · #2782](https://github.com/genspark-ai/genoffice/pull/2782)**<br>I overlap up to eight certificate reads per listing while preserving nickname order, skipped failures and password-file cleanup. Synthetic process-boundary tests verify scheduling; real NSS latency was not measured. |
| **Merged** | **[Unsupported text-insert isolation · #2800](https://github.com/genspark-ai/genoffice/pull/2800)**<br>I keep an unsupported character from discarding otherwise drawable insertions in the same font group. Native PDF save/readback tests use a public font fixture and preserve shared subsetting and untouched content. |
| **Merged** | **[Release completed PDF queue results · #2791](https://github.com/genspark-ai/genoffice/pull/2791)**<br>I release successful PDFium and font-subset outputs from the retained queue tails while preserving caller results, FIFO execution and failure recovery. Local GC probes and actual native output comparisons verify the change without an OOM claim. |

[All 2026 contributions and scope notes](genoffice/2026.md)
