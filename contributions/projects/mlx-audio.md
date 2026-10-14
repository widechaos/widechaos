# mlx-audio

[← All projects](../README.md) · [Upstream repository](https://github.com/Blaizzy/mlx-audio)

| Status | Contribution |
| :--- | :--- |
| **Merged** | **[FIR upsampling for audio loading · #1021](https://github.com/Blaizzy/mlx-audio/pull/1021)**<br>I routed upsampling through the existing chunked FIR resampler, removing spectral images introduced by linear interpolation. Synthetic WAV regressions cover file and memory inputs, mono/stereo audio, and unchanged same-rate decoding. |

Model output and the additional FIR cost were not measured.
