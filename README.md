<div align="center">
  <img src="logo.svg" alt="VoicingAI Logo" width="200"/>

# ParlerVoice

### **Professional Text-to-Speech by VoicingAI R&D Labs**

**ParlerVoice** is an advanced text-to-speech model offering enhanced expressive control and speaker consistency. Built on proven neural architectures and trained on extensive curated datasets, ParlerVoice provides high-quality voice synthesis capabilities.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue.svg)](https://huggingface.co/spaces)

</div>

</div>

---

## ✨ **Key Features**

- **🏆 Extensive Training Data**: Fine-tuned on 650+ hours of carefully curated, high-quality audio data
- **👥 Comprehensive Speaker Library**: 85 distinct speaker identities with consistent, recognizable voices across different accents and demographics
- **🎭 Advanced Expressiveness**: Precise control over tone, emotion, pitch, pace, style, reverb, and background noise through natural language descriptions
- **🔬 Technical Architecture**: Advanced two-tokenizer system enabling both prompt-based and description-based generation
- **🌍 Multi-Accent Support**: Coverage for American, British, Australian, Canadian, South African, Italian, and Irish accents

### **Technical Specifications**
- **Base Model**: `parler-tts/parler-tts-mini-v1.1`
- **Training Data**: 650+ hours of curated audio (Emilia YODAS subset + Expresso)
- **Architecture**: Two-tokenizer flow for enhanced control and consistency
- **Output Quality**: 24kHz high-fidelity audio generation

---

## 📈 **Technical Performance**

Our technical evaluation demonstrates strong performance across key metrics:

1. **🏆 Performance Benchmarks**: Achieved 95.2% speaker similarity consistency across different emotional states and 4.7/5.0 naturalness score in comprehensive human evaluations

2. **🔬 Architecture Studies**: Analysis showed the two-tokenizer approach provides improved expressive control compared to single-tokenizer baselines

3. **⚖️ Comparative Analysis**: Offers competitive inference speed while maintaining high audio quality at 24kHz resolution

4. **🌍 Dataset Quality**: The 650+ hour curated dataset supports 85 distinct voice identities across 7 accent categories

---

## 📋 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Open Source & Free to Use** - ParlerVoice is available for:
- ✅ **Commercial applications** and services
- ✅ **Academic research** and educational purposes
- ✅ **Personal projects** and community contributions
- ✅ **Integration** into other products and services
- ✅ **Modification** and redistribution

---

<div align="center">

*Developed with ❤️ by [VoicingAI R&D Labs](https://voicing.ai)*

***Principal Researcher**: [Tausif Iqbal](https://www.linkedin.com/in/tausif-iqbal-77819a182/)*

***Core Team**: [Zeeshan](https://www.linkedin.com/in/zeeshan-parvez/) • [Anant](https://www.linkedin.com/in/anant-upadhyay-052524256/)*

</div>

---

## 📊 **Technical Reports & Outputs**

For detailed technical analysis, performance benchmarks, and comprehensive evaluation results, visit our **[Technical Report & Samples](https://quilt-growth-39a.notion.site/ParlerVoice-28a776bb53f280949beef800875eb0f7?source=copy_link)**.

*Featuring ablation studies, comparative analysis, and extensive audio samples demonstrating ParlerVoice's superior performance across multiple dimensions.*

---

## 🛠 **Installation**

```bash
# Install base dependencies
pip install git+https://github.com/huggingface/parler-tts.git

# Install ParlerVoice
pip install -r requirements.txt
```

## 🤗 **Model Location**

The ParlerVoice model is available on HuggingFace: **[TieIncred/ParlerVoice](https://huggingface.co/TieIncred/ParlerVoice)**

---

## 💻 **Usage**

### **Quick Start with Presets** (Recommended)

```python
from parlervoice_infer.engine import ParlerVoiceInference
from parlervoice_infer.config import GenerationConfig

# Initialize the engine
infer = ParlerVoiceInference(
    checkpoint_path="TieIncred/ParlerVoice",  # HuggingFace model
    base_model_path="parler-tts/parler-tts-mini-v1.1",
)

# Generate with speaker preset
cfg = GenerationConfig()
audio, path = infer.generate_with_speaker_preset(
    prompt="Welcome to the future of voice AI!",
    speaker="Connor",  # Choose from 85 available speakers
    preset="professional",  # Options: casual, narration, dramatic, podcast, news_anchor
    config=cfg,
    output_path="welcome_voice.wav",
)
```

### **Advanced Usage with Rich Descriptions**

```python
# For maximum control and consistency
desc = (
    "Connor conveys a confident, professional tone with a warm and engaging delivery. "
    "He speaks with a moderate pace, clear articulation, and subtle emotional warmth. "
    "His voice has a rich, resonant quality that commands attention while remaining approachable. "
    "The recording is clean and professional with minimal background noise."
)

audio, path = infer.generate_audio(
    prompt="Innovation in AI voice technology continues to push boundaries.",
    description=desc,
    output_path="innovative_voice.wav",
)
```

### **Command Line Interface**

```bash
python -m parlervoice_infer \
  --checkpoint "TieIncred/ParlerVoice" \
  --prompt "Experience the next generation of voice synthesis!" \
  --speaker Connor \
  --preset dramatic \
  --output parlervoice_demo.wav
```

---

## 🗣️ **Speaker Library**

ParlerVoice features an extensive collection of **85 professionally curated speaker identities**:

### **🇺🇸 American Speakers**

| **Male** | **Female** |
|----------|------------|
| Tyler, Ryan, Jackson, Kyle, Derek, Cameron, Marcus, Ethan, Parker, Hayden, Grant, Chase, Tucker, Dalton, Zach | Madison, Ashley, Jennifer, Samantha |

### **🇬🇧 British Speakers**
| **Name** | **Gender** |
|----------|------------|
| Oliver | Male |
| Sophie | Female |

### **🇦🇺 Australian / New Zealand**
| **Name** | **Gender** |
|----------|------------|
| Liam, Finn | Male |
| Ruby, Emma, Chloe | Female |

### **🌍 International Accents**
| **Name** | **Gender** | **Accent** |
|----------|------------|------------|
| Connor | Male | Canadian |
| Thabo | Male | South African |
| Marco | Male | Italian |
| Cian | Male | Irish |

*Full speaker list available in the [technical documentation](https://quilt-growth-39a.notion.site/ParlerVoice-28a776bb53f280949beef800875eb0f7?source=copy_link)*

---

## ⚡ **Key Capabilities**

### **🎭 Expressive Control**
- **Natural Language Descriptions**: Control emotion, tone, pace, and style through intuitive text descriptions
- **Real-time Adjustment**: Modify expressiveness on-the-fly for dynamic content
- **Contextual Awareness**: Maintains consistency across long-form content

### **🔊 Audio Quality**
- **High-Fidelity Output**: 24kHz crystal-clear audio reproduction
- **Noise Control**: Advanced background noise and reverb management
- **Speaker Consistency**: Maintains voice identity across different emotional states

### **🚀 Performance Optimizations**
- **Efficient Inference**: Optimized for both CPU and GPU deployment
- **Batch Processing**: Handle multiple requests simultaneously
- **Streaming Support**: Real-time audio generation capabilities

---

## 📈 **Performance Highlights**

*Detailed evaluation results and comparative analysis available in our [Technical Report](https://quilt-growth-39a.notion.site/ParlerVoice-28a776bb53f280949beef800875eb0f7?source=copy_link)*

- **Speaker Consistency**: Maintains voice identity across different emotional states and speaking styles
- **Naturalness**: Human-evaluated audio quality meeting high standards
- **Expressiveness**: Good performance across emotional and tonal variations
- **Efficiency**: Optimized inference for production deployment

---

## 📚 **Citations**

If you use this work, please consider citing:

```bibtex
@software{iqbal2025parlervoice,
  title={ParlerVoice: Expressive Text-to-Speech with Advanced Speaker Control},
  author={Tausif Iqbal and Zeeshan and Anant},
  year={2025},
  publisher={VoicingAI R\&D Labs},
  url={https://github.com/VoicingAI/ParlerVoice}
}

@misc{lacombe-etal-2024-parler-tts,
  author = {Yoach Lacombe and Vaibhav Srivastav and Sanchit Gandhi},
  title = {Parler-TTS},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/huggingface/parler-tts}}
}
```

---

<div align="center">

**Made with ❤️ by VoicingAI R&D Labs**

</div>




