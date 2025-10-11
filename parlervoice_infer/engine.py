import logging
from typing import Optional, List, Tuple

import numpy as np
import torch
from transformers import AutoTokenizer

from parler_tts import ParlerTTSForConditionalGeneration

from .config import GenerationConfig
from .presets import PRESETS
from .audio import normalize_audio, save_wav, shorten_long_silences
from .description import build_advanced_description


logger = logging.getLogger(__name__)


class ParlerVoiceInference:
    """ParlerVoice inference engine with enhanced generation options."""

    def __init__(
        self,
        checkpoint_path: str,
        base_model_path: str = "parler-tts/parler-tts-mini-v1.1",
        device: Optional[str] = None,
    ) -> None:
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        logger.info("Using device: %s", self.device)

        logger.info("Loading model from %s", checkpoint_path)
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(checkpoint_path).to(
            self.device
        )
        self.model.eval()

        logger.info("Loading tokenizers from %s", base_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
        self.description_tokenizer = AutoTokenizer.from_pretrained(
            self.model.config.text_encoder._name_or_path
        )
        self.sampling_rate = int(self.model.config.sampling_rate)
        logger.info("Model loaded. Sampling rate: %d Hz", self.sampling_rate)

    def build_advanced_description(
        self,
        speaker: str,
        pace: str = "moderate speed",
        noise: str = "very clear",
        reverberation: str = "very close-sounding",
        monotony: str = "expressive and animated",
        pitch: str = "moderate pitch",
        emotion: str = "neutral",
        tone: str = "neutral",
        add_context: bool = True,
    ) -> str:
        return build_advanced_description(
            speaker=speaker,
            pace=pace,
            noise=noise,
            reverberation=reverberation,
            monotony=monotony,
            pitch=pitch,
            emotion=emotion,
            tone=tone,
            add_context=add_context,
        )

    def generate_audio(
        self,
        prompt: str,
        description: str,
        config: Optional[GenerationConfig] = None,
        output_path: Optional[str] = None,
    ) -> Tuple[np.ndarray, str]:
        if config is None:
            config = GenerationConfig()

        input_ids = self.description_tokenizer(
            description, return_tensors="pt", padding=True, truncation=True
        ).input_ids.to(self.device)
        prompt_input_ids = self.tokenizer(
            prompt, return_tensors="pt", padding=True, truncation=True
        ).input_ids.to(self.device)

        with torch.no_grad():
            generation_output = self.model.generate(
                input_ids=input_ids,
                prompt_input_ids=prompt_input_ids,
                temperature=config.temperature,
                do_sample=config.do_sample,
                top_k=config.top_k,
                top_p=config.top_p,
                repetition_penalty=config.repetition_penalty,
                max_length=config.max_length,
                min_length=config.min_length,
                num_beams=config.num_beams,
                early_stopping=config.early_stopping,
            )

        audio_array = generation_output.cpu().numpy().squeeze()
        audio_array = normalize_audio(audio_array)
        # Post-process: collapse long silences (>2s) down to 800ms
        audio_array = shorten_long_silences(
            audio_array,
            samplerate=self.sampling_rate,
            silence_threshold_db=-40.0,
            max_silence_ms=800,
            collapse_trigger_ms=2000,
        )

        if output_path:
            save_wav(output_path, audio_array, samplerate=self.sampling_rate)
            logger.info("Audio saved to: %s", output_path)
        else:
            output_path = "output.wav"
        return audio_array, output_path

    def generate_with_speaker_preset(
        self,
        prompt: str,
        speaker: str,
        preset: str = "natural",
        config: Optional[GenerationConfig] = None,
        output_path: Optional[str] = None,
    ) -> Tuple[np.ndarray, str]:
        if preset not in PRESETS:
            logger.warning("Unknown preset '%s', using 'natural'", preset)
            preset = "natural"
        preset_config = PRESETS[preset]
        description = self.build_advanced_description(speaker=speaker, **preset_config)
        return self.generate_audio(prompt, description, config, output_path)

    def batch_generate(
        self,
        prompts: List[str],
        descriptions: List[str],
        config: Optional[GenerationConfig] = None,
        output_dir: str = "outputs",
    ) -> List[Tuple[np.ndarray, str]]:
        import os

        os.makedirs(output_dir, exist_ok=True)
        results: List[Tuple[np.ndarray, str]] = []
        for idx, (prompt, description) in enumerate(zip(prompts, descriptions)):
            output_path = os.path.join(output_dir, f"output_{idx:03d}.wav")
            audio_array, saved_path = self.generate_audio(
                prompt, description, config, output_path
            )
            results.append((audio_array, saved_path))
        logger.info("Batch generation complete. Generated %d audio files.", len(results))
        return results

