# Open-source contributions

## more-itertools — bug report resolved

I found and reported that `bucket` ignored a supplied validator when the callable was falsey, letting rejected keys return data. [Report #1308](https://github.com/more-itertools/more-itertools/issues/1308) was resolved by [merged PR #1309](https://github.com/more-itertools/more-itertools/pull/1309), submitted by DawnofGenX. My contribution was the defect discovery, reproduction, and report.

## Pull requests awaiting review

- **Tornado** — return a lock or semaphore permit when async context entry is cancelled after handoff. [PR #3770](https://github.com/tornadoweb/tornado/pull/3770)
- **HTTPX** — raw-deflate decoding with a one-byte initial chunk. [Discussion #3799](https://github.com/encode/httpx/discussions/3799); a candidate patch is available, with an upstream PR awaiting maintainer agreement.
- **python-dotenv** — preserve correct warning line numbers during CRLF parser recovery. [PR #722](https://github.com/theskumar/python-dotenv/pull/722)
- **dateutil** — reject unclosed weekday ordinals that silently change recurrence dates. [PR #1597](https://github.com/dateutil/dateutil/pull/1597)
- **PeonPing** — relay playback with a symlinked packs directory, preserving path checks. [Draft PR #603](https://github.com/PeonPing/peon-ping/pull/603)

## Closed without merge

- **faster-whisper** — [offline guide #1554](https://github.com/SYSTRAN/faster-whisper/pull/1554) and [PCM guide #1556](https://github.com/SYSTRAN/faster-whisper/pull/1556). Both were closed without merge.
