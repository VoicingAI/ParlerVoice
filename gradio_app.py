import argparse
import tempfile
import os
from typing import Tuple

import gradio as gr

from parlervoice_infer.engine import ParlerVoiceInference
from parlervoice_infer.config import GenerationConfig
from parlervoice_infer.presets import PRESETS
from parlervoice_infer.constants import (
    GENDER_MAP,
    PITCH_BINS as pitch_mean_bins,
    RATE_BINS as speaker_rate_bins,
    MONOTONY_BINS as speech_monotony_bins,
    NOISE_BINS as noise_bins,
    REVERB_BINS as reverberation_bins,
)
from parlervoice_infer.description import build_advanced_description


_INFER: ParlerVoiceInference = None


def _ensure_infer(checkpoint: str, base_model: str) -> ParlerVoiceInference:
    global _INFER
    if _INFER is None:
        _INFER = ParlerVoiceInference(checkpoint_path=checkpoint, base_model_path=base_model)
    return _INFER


def generate_audio(
    prompt: str,
    speaker: str,
    tone: str,
    emotion: str,
    pitch: str,
    pace: str,
    monotony: str,
    noise: str,
    reverberation: str,
    checkpoint: str,
    base_model: str,
) -> Tuple[str, str]:
    try:
        infer = _ensure_infer(checkpoint, base_model)
        description = build_advanced_description(
            speaker=speaker,
            pace=pace,
            noise=noise,
            reverberation=reverberation,
            monotony=monotony,
            pitch=pitch,
            emotion=emotion,
            tone=tone,
            add_context=True,
        )
        cfg = GenerationConfig(max_length=512)
        with tempfile.TemporaryDirectory() as td:
            out_path = os.path.join(td, "parler_out.wav")
            _, saved = infer.generate_audio(prompt=prompt, description=description, config=cfg, output_path=out_path)
            return saved, "Success"
    except Exception as e:
        return "", f"Error: {e}"


def build_demo(checkpoint: str, base_model: str) -> gr.Blocks:
    SPEAKER_NAMES = sorted(GENDER_MAP.keys())
    preset_names = ["Custom"] + list(PRESETS.keys())

    with gr.Blocks() as demo:
        gr.Markdown("## ParlerVoice")

        with gr.Row():
            model_ckpt = gr.Textbox(value=checkpoint, label="Checkpoint (path or repo id)")
            model_base = gr.Textbox(value=base_model, label="Base model")

        prompt_input = gr.Textbox(label="Enter Text", placeholder="Type what the speaker says...")
        speaker_dropdown = gr.Dropdown(label="Select Speaker", choices=SPEAKER_NAMES, value=SPEAKER_NAMES[0], interactive=True)

        preset_dropdown = gr.Dropdown(
            label="Voice Preset",
            choices=preset_names,
            value="Custom",
            interactive=True,
        )

        with gr.Group():
            tone = gr.Dropdown(
                label="Tone",
                choices=["serious", "dramatic", "casual", "professional", "storytelling", "narrative"],
                value="serious",
            )
            emotion = gr.Dropdown(
                label="Emotion",
                choices=["neutral", "sad", "happy", "angry", "excited", "confused"],
                value="neutral",
            )
            pitch = gr.Dropdown(label="Pitch", choices=pitch_mean_bins, value="moderate pitch")
            pace = gr.Dropdown(label="Pace", choices=speaker_rate_bins, value="moderate speed")
            monotony = gr.Dropdown(label="Speech Style", choices=speech_monotony_bins, value="expressive and animated")
            noise = gr.Dropdown(label="Noise", choices=noise_bins, value="very clear")
            reverberation = gr.Dropdown(label="Reverberation", choices=reverberation_bins, value="very close-sounding")

        gr.Markdown(
            """
**Sample Descriptions:**  
- Connor delivers a serious and professional message with a calm, even pace and a moderate pitch. The recording is very clean and close-sounding.  
- Madison delivers a sad and disappointed speech. Her voice is slightly high-pitched and sounds like she's on the verge of crying. The recording has some background noise, as if she is in a café.  
- Jackson delivers a narrative with a slightly dramatic tone. The pitch is slightly low, and the pace is deliberate and even. The recording is very clean with a hint of echo, as if recorded in a large hall.
"""
        )

        def apply_preset(preset_name: str):
            if preset_name == "Custom" or preset_name not in PRESETS:
                return gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
            preset = PRESETS[preset_name]
            return (
                gr.update(value=preset.get("tone", None)),
                gr.update(value=preset.get("emotion", None)),
                gr.update(value=preset.get("pitch", None)),
                gr.update(value=preset.get("pace", None)),
                gr.update(value=preset.get("monotony", None)),
            )

        preset_dropdown.change(
            fn=apply_preset,
            inputs=preset_dropdown,
            outputs=[tone, emotion, pitch, pace, monotony],
        )

        generate_btn = gr.Button("Generate Audio")
        audio_output = gr.Audio(type="filepath", label="Generated Audio")
        status_output = gr.Textbox(label="Status", interactive=False)

        generate_btn.click(
            fn=generate_audio,
            inputs=[
                prompt_input,
                speaker_dropdown,
                tone,
                emotion,
                pitch,
                pace,
                monotony,
                noise,
                reverberation,
                model_ckpt,
                model_base,
            ],
            outputs=[audio_output, status_output],
        )

    return demo


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ParlerVoice Gradio App")
    p.add_argument("--checkpoint", required=False, default=os.getenv("PARLER_CHECKPOINT", ""))
    p.add_argument("--base-model", required=False, default=os.getenv("PARLER_BASE_MODEL", "parler-tts/parler-tts-mini-v1.1"))
    p.add_argument("--server-name", default="0.0.0.0")
    p.add_argument("--server-port", type=int, default=7860)
    p.add_argument("--share", action="store_true")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    demo = build_demo(checkpoint=args.checkpoint, base_model=args.base_model)
    demo.launch(server_name=args.server_name, server_port=args.server_port, share=args.share)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

