# ParlerVoice

ParlerVoice — an open‑source, expressive text‑to‑speech model fine‑tuned on ~650 hours of curated audio by VoicingAI RnD Labs, based on `parler-tts-mini-v1.1`.


## Parlervoice Inference

This repo gives you two friendly ways to try it:
- A simple Python API to generate WAVs
- A Gradio app where you can type a prompt, pick a speaker/style, and listen

### Highlights
- Clean Python API for generation
- Presets for common styles plus a flexible description builder
- WAV export with sensible normalization
- One‑file Gradio app for interactive use

### Installation

```bash
pip install -r requirements.txt
```

### Quickstart (Gradio)

```bash
python gradio_app.py \
  --checkpoint "/path/to/checkpoint_or_repo" \
  --base-model "parler-tts/parler-tts-mini-v1.1" \
  --share
```

Then open the URL printed by Gradio. You can also set env vars:

```bash
export PARLER_CHECKPOINT=/path/to/ckpt
export PARLER_BASE_MODEL=parler-tts/parler-tts-mini-v1.1
python gradio_app.py
```

### Python API

```python
from parlervoice_infer.engine import ParlerTTSInference
from parlervoice_infer.config import GenerationConfig
from parlervoice_infer.description import build_advanced_description

infer = ParlerTTSInference(
    checkpoint_path="/path/to/ckpt",
    base_model_path="parler-tts/parler-tts-mini-v1.1",
)

desc = build_advanced_description(speaker="Connor", tone="professional")
audio, path = infer.generate_audio(
    prompt="Hello world",
    description=desc,
    config=GenerationConfig(),
    output_path="out.wav",
)
print(path)
```

### Presets
See `parlervoice_infer/presets.py` for preset names and defaults. Good starters: `professional`, `casual`, `narration`. Tweak tone/emotion/pitch/pace to taste.

### A few things to know
- Base checkpoint: `parler-tts/parler-tts-mini-v1.1`
- Data: ~650 hrs of curated speech
- We keep improving the description prompts (tone/emotion/prosody) to get more natural deliveries.


