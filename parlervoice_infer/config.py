from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """Configuration for audio generation with enhanced parameters."""
    temperature: float = 0.9
    top_k: int = 50
    top_p: float = 0.95
    repetition_penalty: float = 1.1
    max_length: int = 2048
    min_length: int = 10
    do_sample: bool = True
    num_beams: int = 1
    early_stopping: bool = False

