import argparse
import json
import logging
from typing import Optional

from .config import GenerationConfig
from .engine import ParlerVoiceInference


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ParlerVoice TTS Inference CLI")
    p.add_argument("--checkpoint", required=True, help="Path to fine-tuned checkpoint")
    p.add_argument("--base-model", default="parler-tts/parler-tts-mini-v1.1", help="Base model path")
    p.add_argument("--prompt", help="Text to speak")
    p.add_argument("--speaker", default="Connor", help="Speaker name")
    p.add_argument("--preset", default="natural", help="Preset name")
    p.add_argument("--description", help="Override auto-built description")
    p.add_argument("--output", default="output.wav", help="Output wav path")
    p.add_argument("--jobs", help="JSONL of batch jobs: prompt,speaker,preset,output")
    p.add_argument("--output-dir", default="outputs", help="Dir for batch outputs")

    # generation args
    p.add_argument("--temperature", type=float, default=0.9)
    p.add_argument("--top-k", type=int, default=50)
    p.add_argument("--top-p", type=float, default=0.95)
    p.add_argument("--repetition-penalty", type=float, default=1.1)
    p.add_argument("--max-length", type=int, default=2048)
    p.add_argument("--min-length", type=int, default=10)
    p.add_argument("--num-beams", type=int, default=1)
    p.add_argument("--no-sample", action="store_true", help="Disable sampling")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    config = GenerationConfig(
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        max_length=args.max_length,
        min_length=args.min_length,
        do_sample=not args.no_sample,
        num_beams=args.num_beams,
    )

    infer = ParlerVoiceInference(checkpoint_path=args.checkpoint, base_model_path=args.base_model)

    if args.jobs:
        count = 0
        with open(args.jobs, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                job = json.loads(line)
                prompt: str = job["prompt"]
                speaker: str = job.get("speaker", args.speaker)
                preset: str = job.get("preset", args.preset)
                output: str = job.get("output", f"{args.output_dir}/job_{count:03d}.wav")
                desc = job.get("description")
                if not desc:
                    desc = infer.build_advanced_description(speaker=speaker, **{})
                    # If preset provided, use preset builder
                    desc = infer.build_advanced_description(speaker=speaker, **{})
                # Prefer preset when specified
                if preset:
                    _, _ = infer.generate_with_speaker_preset(
                        prompt=prompt, speaker=speaker, preset=preset, config=config, output_path=output
                    )
                else:
                    _, _ = infer.generate_audio(prompt=prompt, description=desc, config=config, output_path=output)
                count += 1
        return 0

    # Single job path
    description: Optional[str] = args.description
    if not description:
        # Prefer preset if provided
        _, _ = infer.generate_with_speaker_preset(
            prompt=args.prompt or "",
            speaker=args.speaker,
            preset=args.preset,
            config=config,
            output_path=args.output,
        )
    else:
        _, _ = infer.generate_audio(
            prompt=args.prompt or "",
            description=description,
            config=config,
            output_path=args.output,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

