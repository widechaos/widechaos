# PeonPing

[← All projects](../README.md) · [Upstream repository](https://github.com/PeonPing/peon-ping)

| Status | Contribution |
| :--- | :--- |
| **Integrated in upstream batch** | **[Relay playback · #603](https://github.com/PeonPing/peon-ping/pull/603)**<br>Allow relay playback with a symlinked packs directory, preserving path checks. |
| **Integrated in upstream batch** | **[Codex command hook detection · #611](https://github.com/PeonPing/peon-ping/pull/611)**<br>Detect command hooks in hooks.json for status reporting without executing them; retain existing TOML detection. |
| **Integrated in upstream batch** | **[Symlinked hook configuration · #613](https://github.com/PeonPing/peon-ping/pull/613)**<br>Use the configuration beside the invoked hook symlink before profile and shared fallbacks, preserving explicit overrides. |

The maintainer included these contributions in [merged upstream batch #619](https://github.com/PeonPing/peon-ping/pull/619), now on the main branch at [3008c0f](https://github.com/PeonPing/peon-ping/commit/3008c0fff4b9a658378644d9223975acd0e7cc6f). The original PRs were closed without merging. The batch also contains other contributors’ work; I claim only the three fixes linked above. Installer/uninstaller JSON preservation and the other batch changes are not attributed to my status-detection patch.
