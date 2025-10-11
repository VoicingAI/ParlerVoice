# ParlerVoice

ParlerVoice is an expressive text-to-speech model fine‑tuned on ~650 hours of curated audio by VoicingAI RnD Labs, based on the Parler‑TTS Mini v1.1 architecture.

- Base: `parler-tts/parler-tts-mini-v1.1`
- Data: ~650 hours (curated)
- Controls: tone, emotion, pitch, pace, style, reverb, noise
- Two-tokenizer flow (prompt vs. description), same as upstream Parler‑TTS

Upstream project: [huggingface/parler-tts](https://github.com/huggingface/parler-tts)

Project repository: [VoicingAI/ParlerVoice](https://github.com/VoicingAI/ParlerVoice)

## 👨‍💻 Installation

```bash
pip install git+https://github.com/huggingface/parler-tts.git

pip install -r requirements.txt
```

## 🎯 Usage (Transformers API)

Below mirrors the upstream Parler‑TTS usage with separate tokenizers for description and prompt.

```python
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model_path = "/path/to/ckpt"
ckpt = "parler-tts/parler-tts-mini-v1.1"

model = ParlerTTSForConditionalGeneration.from_pretrained(model_path).to(device)

prompt_tokenizer = AutoTokenizer.from_pretrained(ckpt)
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

prompt = "Hey, how are you doing today?"
description = (
    "Connor conveys a neutral mood through a professional and controlled delivery. "
    "He speaks with a slightly low pitch, adding subtle weight to his delivery. "
    "His pace is moderate, keeping the speech easy to follow. "
    "His voice is slightly expressive, with subtle emotional inflections. "
    "The recording is exceptionally clean and close-sounding. "
    "The voice is very close, making it feel immediate and present."
)

desc_inputs = description_tokenizer(description, return_tensors="pt").to(device)
prompt_inputs = prompt_tokenizer(prompt, return_tensors="pt").to(device)

gen = model.generate(
    input_ids=desc_inputs.input_ids,
    attention_mask=desc_inputs.attention_mask,
    prompt_input_ids=prompt_inputs.input_ids,
    prompt_attention_mask=prompt_inputs.attention_mask,
)

audio_arr = gen.cpu().numpy().squeeze()
sf.write("parlervoice_out.wav", audio_arr, model.config.sampling_rate)
```

## ✅ Examples for better results (presets and rich descriptions)

Using presets (from our repo API):

```python
from parlervoice_infer.engine import ParlerTTSInference
from parlervoice_infer.config import GenerationConfig

infer = ParlerTTSInference(
    checkpoint_path="/path/to/ckpt",
    base_model_path="parler-tts/parler-tts-mini-v1.1",
)

cfg = GenerationConfig()
audio, path = infer.generate_with_speaker_preset(
    prompt="Welcome to ParlerVoice!",
    speaker="Connor",
    preset="professional",  # also: casual, narration, dramatic, podcast, news_anchor
    config=cfg,
    output_path="preset_out.wav",
)
```

Using a richer description (most control/consistency):

```python
from parlervoice_infer.engine import ParlerTTSInference

infer = ParlerTTSInference(
    checkpoint_path="/path/to/ckpt",
    base_model_path="parler-tts/parler-tts-mini-v1.1",
)

desc = (
    "Connor conveys a neutral mood through a professional and controlled delivery. "
    "He speaks with a slightly low pitch, adding subtle weight to his delivery. "
    "His pace is moderate, keeping the speech easy to follow. "
    "His voice is slightly expressive, with subtle emotional inflections. "
    "The recording is exceptionally clean and close-sounding. "
    "The voice is very close, making it feel immediate and present."
)

audio, path = infer.generate_audio(
    prompt="In a collaborative environment, success depends on strong communication.",
    description=desc,
    output_path="desc_out.wav",
)
```

CLI with presets (from the repo):

```bash
python -m parlervoice_infer \
  --checkpoint "/path/to/ckpt" \
  --prompt "Welcome to ParlerVoice!" \
  --speaker Connor \
  --preset professional \
  --output preset_cli.wav
```

## 🗣️ Using a specific speaker

To bias towards a named speaker, include the speaker name in the description. Example:

```text
Connor conveys a neutral mood through a professional and controlled delivery. He speaks with a slightly low pitch, adding subtle weight to his delivery. His pace is moderate, keeping the speech easy to follow. His voice is slightly expressive, with subtle emotional inflections. The recording is exceptionally clean and close-sounding. The voice is very close, making it feel immediate and present.
```

You can then vary emotion/tone to get different styles (e.g., professional, energetic, sad, dramatic).

## 🔧 Key capabilities
- Descriptive control via caption: background noise, reverberation, expressivity, pitch, pace
- Consistent "speaker names" referenced in the caption to bias style
- Compatible with performance optimizations from upstream Parler‑TTS (e.g., SDPA, compile)

For optimization tips, see Parler‑TTS docs: [INFERENCE.md](https://github.com/huggingface/parler-tts/blob/main/INFERENCE.md)

### Recommended usage for best results
- Use the presets and description builder in our repository to get consistent, high‑quality outputs.
- We actively refine description phrasing (tone/emotion/prosody) to improve naturalness—pull latest from the repo for updates.
- Bias generations by including a named speaker (see the tables below) in your description.

## 📦 Checkpoint notes
- This model was fine‑tuned from `parler-tts/parler-tts-mini-v1.1`.
- Approx. 650h of curated audio were used (Emilia YODAS subset + Expresso).
- We are iterating on description phrasing to improve naturalness and controllability.

## 🧑 Named speakers for consistency
We assign human‑readable names to 85 speakers to improve style and identity consistency across generations. Use names directly in captions, e.g., "Connor … speaks with a professional tone…".

**American — Male**

| Name    |
|---------|
| Tyler   |
| Ryan    |
| Jackson |
| Kyle    |
| Derek   |
| Cameron |
| Marcus  |
| Ethan   |
| Parker  |
| Hayden  |
| Grant   |
| Chase   |
| Tucker  |
| Dalton  |
| Zach    |

**American — Female**

| Name     |
|----------|
| Madison  |
| Ashley   |
| Jennifer |
| Samantha |

**English‑accented**

| Name   | Gender |
|--------|--------|
| Oliver | male   |
| Sophie | female |

**Australian / New‑Zealand**

| Name  | Gender |
|-------|--------|
| Liam  | male   |
| Ruby  | female |
| Finn  | male   |
| Emma  | female |
| Chloe | female |

**Other accents**

| Name   | Gender | Accent        |
|--------|--------|---------------|
| Connor | male   | Canadian      |
| Thabo  | male   | South african |
| Marco  | male   | Italian       |
| Cian   | male   | Irish         |

### Full list of speaker names

Connor, Thabo, Madison, Tyler, Mei, Jackson, Brandon, Ashley, Kyle, Jennifer, Ryan, Austin, Derek, Camille, Brittany, Johan, Trevor, Jordan, Nathan, Sophie, Cameron, Marcus, Blake, Samantha, Garrett, Caleb, Logan, Ethan, Hunter, Mason, Aoife, Chloe, Lin, Xiao, Colton, Flynn, Devin, Li, Marco, Emma, Carson, Rachel, Oliver, Preston, Wei, Landon, Liam, Bryce, Finn, Parker, Hayden, Grant, Chase, Siobhan, Tucker, Dalton, Zach, Jasper, Niamh, Jing, Erin, Cole, Yan, Paige, Noah, Taylor, Trent, Shane, Jared, Reid, Spencer, Wyatt, Ingrid, Luke, Zara, Alexis, Cody, Haley, Megan, Drew, Pieter, Priya, Henry, Vincent, Nolan, Kane, Grace, Ian, Ruby, Kent, Elena, Cian, Jace, Max, Reed, Wade, George, Seth, Cruz, Miles, John, Alice, Michael, Olivia.

## 📚 Citation
If you use this work, please consider citing upstream Parler‑TTS and the original paper.

```
@misc{lacombe-etal-2024-parler-tts,
  author = {Yoach Lacombe and Vaibhav Srivastav and Sanchit Gandhi},
  title = {Parler-TTS},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/huggingface/parler-tts}}
}
```

```
@misc{lyth2024natural,
  title={Natural language guidance of high-fidelity text-to-speech with synthetic annotations},
  author={Dan Lyth and Simon King},
  year={2024},
  eprint={2402.01912},
  archivePrefix={arXiv},
  primaryClass={cs.SD}
}
```


