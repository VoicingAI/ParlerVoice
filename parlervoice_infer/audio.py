import numpy as np
import soundfile as sf


def normalize_audio(audio: np.ndarray, target_level_db: float = -20.0) -> np.ndarray:
    """Normalize audio to a target RMS level in dB."""
    rms = float(np.sqrt(np.mean(np.square(audio))))
    if rms == 0.0:
        return audio
    target_linear = 10 ** (target_level_db / 20.0)
    normalized = audio * (target_linear / rms)
    max_val = float(np.max(np.abs(normalized)))
    if max_val > 1.0:
        normalized = normalized / max_val * 0.95
    return normalized


def save_wav(path: str, audio: np.ndarray, samplerate: int) -> None:
    """Save audio as WAV file."""
    sf.write(path, audio, samplerate=samplerate)


def shorten_long_silences(
    audio: np.ndarray,
    samplerate: int,
    silence_threshold_db: float = -40.0,
    max_silence_ms: int = 800,
    collapse_trigger_ms: int = 2000,
) -> np.ndarray:
    """
    Collapse continuous silences longer than collapse_trigger_ms down to max_silence_ms.

    A simple amplitude-threshold based detector is used to find silent frames.
    """
    if audio.size == 0:
        return audio

    # Compute frame-wise RMS in small windows (10ms) for robust silence detection
    window_ms = 10
    window = max(1, int(samplerate * window_ms / 1000))
    if window <= 1:
        window = 2

    # Pad to multiple of window
    pad = (window - (audio.shape[0] % window)) % window
    if pad:
        audio_padded = np.pad(audio, (0, pad), mode="constant")
    else:
        audio_padded = audio

    frames = audio_padded.reshape(-1, window)
    rms = np.sqrt(np.mean(frames ** 2, axis=1) + 1e-12)
    rms_db = 20 * np.log10(np.maximum(rms, 1e-12))

    silence_mask = rms_db < silence_threshold_db

    # Find silent runs (in frames)
    max_keep_frames = max(1, int(max_silence_ms / window_ms))
    collapse_trigger_frames = max(1, int(collapse_trigger_ms / window_ms))

    kept_frames = []
    i = 0
    total = silence_mask.shape[0]
    while i < total:
        if silence_mask[i]:
            j = i
            while j < total and silence_mask[j]:
                j += 1
            run = j - i
            if run > collapse_trigger_frames:
                kept_frames.extend([False] * max_keep_frames)
            else:
                kept_frames.extend([False] * run)
            i = j
        else:
            kept_frames.append(True)
            i += 1

    kept_frames = np.array(kept_frames[: frames.shape[0]], dtype=bool)

    # Reconstruct audio: keep non-silent frames fully; for silent frames, keep only first max_keep_frames
    out_frames = []
    i = 0
    while i < frames.shape[0]:
        if not silence_mask[i]:
            out_frames.append(frames[i])
            i += 1
        else:
            # Copy limited silent frames
            j = i
            while j < frames.shape[0] and silence_mask[j]:
                j += 1
            run = j - i
            keep = min(run, collapse_trigger_frames, max_keep_frames)
            for k in range(keep):
                out_frames.append(frames[i + k])
            i = j

    out = np.concatenate(out_frames, axis=0)
    # Trim the padding if added
    return out[: max(0, out.shape[0] - 0)]

