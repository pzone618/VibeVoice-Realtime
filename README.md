<div align="center">

## 🎙️ VibeVoice: Frontier Open-Source Voice AI
[![Project Page](https://img.shields.io/badge/Project-Page-blue?logo=microsoft)](https://microsoft.github.io/VibeVoice)
[![Hugging Face](https://img.shields.io/badge/HuggingFace-Collection-orange?logo=huggingface)](https://huggingface.co/collections/microsoft/vibevoice-68a2ef24a875c44be47b034f)
[![Technical Report](https://img.shields.io/badge/Technical-Report-red?logo=adobeacrobatreader)](https://arxiv.org/pdf/2508.19205)


</div>


<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Figures/VibeVoice_logo_white.png">
  <img src="Figures/VibeVoice_logo.png" alt="VibeVoice Logo" width="300">
</picture>
</div>

<div align="left">

<h3>📰 News</h3>

<img src="https://img.shields.io/badge/Status-New-brightgreen?style=flat" alt="New" />
<img src="https://img.shields.io/badge/Feature-Realtime_TTS-blue?style=flat&logo=soundcharts" alt="Realtime TTS" />

<strong>2025-12-03: 📣 We open-sourced <a href="docs/vibevoice-realtime-0.5b.md"><strong>VibeVoice‑Realtime‑0.5B</strong></a>, a real‑time text‑to‑speech model that supports streaming text input and robust long-form speech generation.</strong>
<br>

https://github.com/user-attachments/assets/0901d274-f6ae-46ef-a0fd-3c4fba4f76dc

> (Launch your own realtime demo via the websocket example in [Usage](docs/vibevoice-realtime-0.5b.md#usage-1-launch-real-time-websocket-demo)).

</div>

2025-09-05: VibeVoice is an open-source research framework intended to advance collaboration in the speech synthesis community. After release, we discovered instances where the tool was used in ways inconsistent with the stated intent. Since responsible use of AI is one of Microsoft’s guiding principles, we have disabled this repo until we are confident that out-of-scope use is no longer possible.


### Overview

VibeVoice is a novel framework designed for generating **expressive**, **long-form**, **multi-speaker** conversational audio, such as podcasts, from text. It addresses significant challenges in traditional Text-to-Speech (TTS) systems, particularly in scalability, speaker consistency, and natural turn-taking.

VibeVoice currently includes two model variants:

- **Long-form multi-speaker model**: Synthesizes conversational/single-speaker speech up to **90 minutes** with up to **4 distinct speakers**, surpassing the typical 1–2 speaker limits of many prior models.
- **[Realtime streaming TTS model](docs/vibevoice-realtime-0.5b.md)**: Produces initial audible speech in ~**300 ms** and supports **streaming text input** for single-speaker **real-time** speech generation; designed for low-latency generation.

A core innovation of VibeVoice is its use of continuous speech tokenizers (Acoustic and Semantic) operating at an ultra-low frame rate of 7.5 Hz. These tokenizers efficiently preserve audio fidelity while significantly boosting computational efficiency for processing long sequences. VibeVoice employs a [next-token diffusion](https://arxiv.org/abs/2412.08635) framework, leveraging a Large Language Model (LLM) to understand textual context and dialogue flow, and a diffusion head to generate high-fidelity acoustic details.


<p align="left">
  <img src="Figures/MOS-preference.png" alt="MOS Preference Results" height="260px">
  <img src="Figures/VibeVoice.jpg" alt="VibeVoice Overview" height="250px" style="margin-right: 10px;">
</p>


### 🎵 Demo Examples


**Video Demo**

We produced this video with [Wan2.2](https://github.com/Wan-Video/Wan2.2). We sincerely appreciate the Wan-Video team for their great work.

**English**
<div align="center">

https://github.com/user-attachments/assets/0967027c-141e-4909-bec8-091558b1b784

</div>


**Chinese**
<div align="center">

https://github.com/user-attachments/assets/322280b7-3093-4c67-86e3-10be4746c88f

</div>

**Cross-Lingual**
<div align="center">

https://github.com/user-attachments/assets/838d8ad9-a201-4dde-bb45-8cd3f59ce722

</div>

**Spontaneous Singing**
<div align="center">

https://github.com/user-attachments/assets/6f27a8a5-0c60-4f57-87f3-7dea2e11c730

</div>


**Long Conversation with 4 people**
<div align="center">

https://github.com/user-attachments/assets/a357c4b6-9768-495c-a576-1618f6275727

</div>

For more examples, see the [Project Page](https://microsoft.github.io/VibeVoice).


## 🚀 Quick Start

### Prerequisites

- Python 3.9+ (Python 3.11 recommended for better OpenSSL support)
- For GPU acceleration:
  - NVIDIA GPU with CUDA support (recommended: T4 or better)
  - Apple Silicon Mac with MPS support (M1/M2/M3/M4)
- 8GB+ RAM (16GB+ recommended)

### Installation

#### Option 1: Standard Installation (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice
```

2. **Create and activate virtual environment:**
```bash
# Using venv
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using conda
conda create -n vibevoice python=3.11
conda activate vibevoice
```

3. **Install dependencies:**
```bash
pip install -e .
```

#### Option 2: Using NVIDIA Docker (For CUDA users)

```bash
# Launch NVIDIA PyTorch Container (24.07 or later)
docker run --privileged --net=host --ipc=host \
  --ulimit memlock=-1:-1 --ulimit stack=-1:-1 \
  --gpus all --rm -it nvcr.io/nvidia/pytorch:24.07-py3

# Inside container
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice
pip install -e .
```

### Usage

#### 1️⃣ Real-time WebSocket Demo (Recommended)

Launch the web-based interactive demo:

```bash
# For CUDA GPU
python3 demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device cuda \
  --port 8001

# For Apple Silicon (MPS)
python3 demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --port 8001

# For CPU (slower)
python3 demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device cpu \
  --port 8000
```

Then open your browser and navigate to: `http://localhost:8000/`

**Available Options:**
- `--host`: Host to bind (default: `127.0.0.1`)
- `--port`: Port to bind (default: `8001`)
- `--device`: Device for inference (`cuda`, `mps`, or `cpu`)
- `--model_path`: Model path or HuggingFace model ID
- `--reload`: Enable auto-reload for development

**Using Custom Voice Presets:**
```bash
VOICE_PRESET=en-Emma_woman python3 demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps
```

Available voices are located in `demo/voices/streaming_model/`.

#### 2️⃣ Batch Inference from Text Files

Generate audio from text files:

```bash
python3 demo/realtime_model_inference_from_file.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --txt_path demo/text_examples/1p_vibevoice.txt \
  --speaker_name Carter \
  --output_dir ./outputs \
  --device mps \
  --cfg_scale 1.5
```

**Options:**
- `--txt_path`: Path to input text file
- `--speaker_name`: Voice preset name (e.g., `Carter`, `Emma`, `Davis`)
- `--output_dir`: Directory for output audio files (default: `./outputs`)
- `--cfg_scale`: Classifier-Free Guidance scale (default: `1.5`)

#### 3️⃣ Jupyter Notebook

For interactive experimentation:
```bash
jupyter notebook demo/vibevoice_realtime_colab.ipynb
```

Or run directly in [Google Colab](https://colab.research.google.com/github/microsoft/VibeVoice/blob/main/demo/vibevoice_realtime_colab.ipynb).

### 🎛️ Advanced Configuration

#### Custom Port with uvicorn

For more control over the server:
```bash
MODEL_PATH=microsoft/VibeVoice-Realtime-0.5B \
MODEL_DEVICE=mps \
uvicorn demo.web.app:app --host 0.0.0.0 --port 8080 --reload
```

#### Model Variants

| Model | Context Length | Generation Length | Language Support | Speakers | Link |
|-------|----------------|-------------------|------------------|----------|------|
| VibeVoice-Realtime-0.5B | 8K | ~10 min | English only | Single | [HF](https://huggingface.co/microsoft/VibeVoice-Realtime-0.5B) |
| VibeVoice-Long-Form* | 64K+ | ~90 min | English + Chinese | Up to 4 | [Collection](https://huggingface.co/collections/microsoft/vibevoice-68a2ef24a875c44be47b034f) |

*Long-form multi-speaker model demos coming soon.

### 🐛 Troubleshooting

#### LibreSSL/OpenSSL Warning on macOS

If you see `NotOpenSSLWarning` with LibreSSL:

**Quick Fix:**
```bash
pip install 'urllib3<2' requests certifi
```

**Recommended Fix** (using Homebrew Python with OpenSSL):
```bash
brew install python@3.11
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

#### Model Download Issues

The first run will download the model from Hugging Face (~2-3GB). If download fails:
1. Check internet connection
2. Set HuggingFace token if needed:
   ```bash
   huggingface-cli login
   ```
3. Manually download and specify local path:
   ```bash
   huggingface-cli download microsoft/VibeVoice-Realtime-0.5B
   python3 demo/vibevoice_realtime_demo.py --model_path /path/to/local/model
   ```

#### Performance Issues

- **GPU not detected:** Verify CUDA/MPS availability:
  ```bash
  python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, MPS: {torch.backends.mps.is_available()}')"
  ```
- **Out of memory:** Reduce batch size or use CPU mode
- **Slow generation:** Ensure you're using GPU; CPU inference is significantly slower


## 📁 Project Structure

```
VibeVoice-Realtime/
├── demo/
│   ├── vibevoice_realtime_demo.py      # Main web demo entry point
│   ├── realtime_model_inference_from_file.py  # Batch inference script
│   ├── vibevoice_realtime_colab.ipynb  # Jupyter notebook
│   ├── voices/streaming_model/          # Voice preset files (.pt)
│   ├── text_examples/                   # Sample input texts
│   └── web/
│       ├── app.py                       # FastAPI backend
│       └── index.html                   # Web UI
├── vibevoice/
│   ├── modular/                         # Model architecture
│   ├── processor/                       # Text/audio processing
│   └── schedule/                        # Diffusion schedulers
├── docs/                                # Documentation
├── pyproject.toml                       # Project dependencies
└── README.md
```


## Risks and limitations

While efforts have been made to optimize it through various techniques, it may still produce outputs that are unexpected, biased, or inaccurate. VibeVoice inherits any biases, errors, or omissions produced by its base model (specifically, Qwen2.5 1.5b in this release).
Potential for Deepfakes and Disinformation: High-quality synthetic speech can be misused to create convincing fake audio content for impersonation, fraud, or spreading disinformation. Users must ensure transcripts are reliable, check content accuracy, and avoid using generated content in misleading ways. Users are expected to use the generated content and to deploy the models in a lawful manner, in full compliance with all applicable laws and regulations in the relevant jurisdictions. It is best practice to disclose the use of AI when sharing AI-generated content.

English and Chinese only: Transcripts in languages other than English or Chinese may result in unexpected audio outputs.

Non-Speech Audio: The model focuses solely on speech synthesis and does not handle background noise, music, or other sound effects.

Overlapping Speech: The current model does not explicitly model or generate overlapping speech segments in conversations.

We do not recommend using VibeVoice in commercial or real-world applications without further testing and development. This model is intended for research and development purposes only. Please use responsibly.
