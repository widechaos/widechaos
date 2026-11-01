# wcmatch

[← All projects](../README.md) · [Upstream repository](https://github.com/facelessuser/wcmatch)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Combined pattern limit for duplicate exclusions · #263](https://github.com/facelessuser/wcmatch/pull/263)**<br>I reproduced duplicate exclusions bypassing the combined pattern limit in compile and translate, added regression coverage, and contributed the initial fix. The maintainer replaced the recursive counter with a shared non-recursive expansion iterator; I reviewed that change and completed the spelling follow-up. |

The merged checks cover Windows and Ubuntu Python 3.11–3.15. Native invalid-byte filenames were unavailable on my macOS filesystem; that local limitation was recorded separately.
