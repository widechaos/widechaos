# mlx-audio

[← All projects](../README.md) · [Upstream repository](https://github.com/Neywa-Labs/mlx-audio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Documentation entry link · #1178](https://github.com/Neywa-Labs/mlx-audio/pull/1178)**<br>I corrected the README documentation link after the repository move. Independent HTTP checks confirmed the old address returned 404 and the new project documentation returned 200. |
| **Merged** | **[FIR upsampling for audio loading · #1021](https://github.com/Neywa-Labs/mlx-audio/pull/1021)**<br>I routed upsampling through the existing chunked FIR resampler, removing spectral images introduced by linear interpolation. Synthetic WAV regressions cover file and memory inputs, mono/stereo audio, and unchanged same-rate decoding. |

Model output and the additional FIR cost were not measured.
