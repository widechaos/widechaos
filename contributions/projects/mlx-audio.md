# mlx-audio

[← All projects](../README.md) · [Upstream repository](https://github.com/Neywa-Labs/mlx-audio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[Ming Tiny seeded first request · #1209](https://github.com/Neywa-Labs/mlx-audio/pull/1209)**<br>I seed sampling after lazy speaker initialization, before reference-latent sampling, so initialization no longer consumes the seeded random stream. Isolated MLX regressions cover the ordering; full-model cloned audio was not evaluated. Lucas Newman merged upstream main before merging the fix. |
| **Merged** | **[Ming Tiny posterior scale · #1216](https://github.com/Neywa-Labs/mlx-audio/pull/1216)**<br>I corrected the reference-latent posterior parameterization while preserving the shared VAE formula, weight layout and random draw order. Lucas Newman replaced the equivalent expression with native MLX softplus. Numerical and small-model regressions cover the change; cloning quality was not measured. |
| **Merged** | **[Documentation entry link · #1178](https://github.com/Neywa-Labs/mlx-audio/pull/1178)**<br>I corrected the README documentation link after the repository move. Independent HTTP checks confirmed the old address returned 404 and the new project documentation returned 200. |
| **Merged** | **[FIR upsampling for audio loading · #1021](https://github.com/Neywa-Labs/mlx-audio/pull/1021)**<br>I routed upsampling through the existing chunked FIR resampler, removing spectral images introduced by linear interpolation. Synthetic WAV regressions cover file and memory inputs, mono/stereo audio, and unchanged same-rate decoding. |

Model output and the additional FIR cost were not measured.
