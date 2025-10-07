from .constants import GENDER_MAP


def build_advanced_description(
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
    gender = GENDER_MAP.get(speaker, "male")
    he_she = "he" if gender == "male" else "she"
    his_her = "his" if gender == "male" else "her"

    tone_phrases = {
        "serious": "serious and focused",
        "dramatic": "dramatic and compelling",
        "casual": "casual and relaxed",
        "professional": "professional and articulate",
        "storytelling": "narrative and engaging",
        "narrative": "storytelling and captivating",
    }

    emotion_phrases = {
        "neutral": "a neutral, balanced composure",
        "sad": "a sad, melancholic undertone",
        "happy": "a happy, cheerful and uplifting energy",
        "angry": "an angry, intense and forceful emotion",
        "excited": "an excited, enthusiastic and vibrant spirit",
        "confused": "a confused, uncertain and questioning demeanor",
    }

    tone_desc = tone_phrases.get(tone, tone)
    emotion_desc = emotion_phrases.get(emotion, emotion)
    sentence1 = f"{speaker} speaks with a {tone_desc} manner, conveying {emotion_desc}."

    pitch_descriptions = {
        "very low-pitch": f"{he_she.capitalize()} possesses a very low pitch, creating deep resonance and gravitas.",
        "low-pitch": f"{he_she.capitalize()} has a low pitch that sounds calm, grounded, and authoritative.",
        "slightly low-pitch": f"{he_she.capitalize()} speaks with a slightly low pitch, adding subtle depth.",
        "moderate pitch": f"{he_she.capitalize()} maintains a moderate pitch with natural vocal balance.",
        "slightly high-pitch": f"{he_she.capitalize()} uses a slightly high pitch, enhancing expressiveness.",
        "high-pitch": f"{he_she.capitalize()} speaks in a high pitch with bright, energetic quality.",
        "very high-pitch": f"{he_she.capitalize()} has a very high pitch, creating animated intensity.",
    }
    pace_descriptions = {
        "very slowly": f"{his_her.capitalize()} delivery is very slow and methodical, emphasizing clarity.",
        "slowly": f"{his_her.capitalize()} pace is slow and deliberate, creating contemplative rhythm.",
        "slightly slowly": f"{his_her.capitalize()} pace is slightly measured, ensuring clear articulation.",
        "moderate speed": f"{his_her.capitalize()} speaking rate is moderate and naturally flowing.",
        "slightly fast": f"{his_her.capitalize()} pace is slightly brisk, maintaining engagement.",
        "fast": f"{his_her.capitalize()} delivery is fast and dynamic with energetic momentum.",
        "very fast": f"{his_her.capitalize()} pace is very rapid, creating urgency and excitement.",
    }
    monotony_descriptions = {
        "very monotone": f"{his_her.capitalize()} speech is very monotone with consistent, steady delivery.",
        "monotone": f"{his_her.capitalize()} voice is monotone, maintaining even emotional range.",
        "slightly expressive and animated": f"{his_her.capitalize()} voice shows subtle variation and life.",
        "expressive and animated": f"{his_her.capitalize()} delivery is expressive with dynamic modulation.",
        "very expressive and animated": f"{his_her.capitalize()} speech is highly animated and captivating.",
    }

    sentence2 = " ".join(
        [
            pitch_descriptions.get(pitch, ""),
            pace_descriptions.get(pace, ""),
            monotony_descriptions.get(monotony, ""),
        ]
    ).strip()

    if noise in ["very clear", "almost no noise"]:
        noise_desc = "The recording quality is pristine and professional-grade"
    else:
        noise_desc = f"The audio contains {noise}, adding environmental texture"

    reverb_descriptions = {
        "very distant-sounding": "with expansive, hall-like acoustics creating spacious depth",
        "distant-sounding": "with noticeable spatial distance and ambient character",
        "slightly distant-sounding": "with subtle room presence and mild spaciousness",
        "slightly close-sounding": "with intimate proximity and warm presence",
        "very close-sounding": "with immediate, close-mic intimacy and clarity",
    }
    sentence3 = f"{noise_desc} {reverb_descriptions.get(reverberation, '')}."

    full_description = f"{sentence1} {sentence2} {sentence3}".strip()
    if add_context:
        full_description += (
            f" The overall vocal presentation is coherent and well-suited for {tone} communication."
        )
    return full_description

