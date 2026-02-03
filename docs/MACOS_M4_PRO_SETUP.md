# Mac mini M4 Pro 配置指南

本文档提供专为 Mac mini M4 Pro (Apple Silicon) 优化的 VibeVoice-Realtime 部署配置。

## 系统信息

- **机器**: Mac mini M4 Pro (基础版)
- **芯片**: Apple Silicon (arm64)
- **推荐内存**: 16GB+
- **GPU**: 8核或10核 GPU (MPS 支持)

## ✅ 环境验证

### 已验证兼容

- ✅ **PyTorch 2.10.0**: 完整的 MPS (Metal Performance Shaders) 支持
- ✅ **Python 3.13.7**: 超过推荐的 3.11 版本
- ✅ **MPS GPU 加速**: 已启用，M4 Pro GPU 加速可用
- ✅ **所有核心依赖**: 已安装且兼容 arm64

## 🚀 快速开始

### 1. 创建虚拟环境（推荐使用 uv）

```bash
# 安装 uv（如果未安装）
brew install uv

# 创建虚拟环境
cd ~/VibeVoice-Realtime
uv venv .venv
source .venv/bin/activate

# 安装依赖
uv pip install -e .
```

### 2. 验证配置

```bash
# 验证 MPS 支持
python -c "import torch; print(f'MPS 可用: {torch.backends.mps.is_available()}')"

# 验证模块导入
python -c "from vibevoice import *; print('✅ vibevoice 模块加载成功')"
```

## 🎙️ 运行演示

### Web 演示（推荐）

使用 MPS GPU 加速运行实时 TTS 演示：

```bash
python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --port 8001
```

然后在浏览器中打开：`http://localhost:8001/`

### 批量推理

从文本文件生成音频：

```bash
python demo/realtime_model_inference_from_file.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --txt_path demo/text_examples/1p_vibevoice.txt \
  --speaker_name Emma \
  --output_dir ./outputs \
  --device mps \
  --cfg_scale 1.5
```

### 自定义语音预设

选择不同的语音：

```bash
# 列出可用语音
ls demo/voices/streaming_model/

# 使用特定语音
VOICE_PRESET=en-Grace_woman python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps
```

可用英文语音：
- `en-Carter_man`
- `en-Davis_man`
- `en-Emma_woman`
- `en-Frank_man`
- `en-Grace_woman`
- `en-Mike_man`

## ⚙️ 性能优化建议

### 内存管理

```bash
# 如果遇到内存不足，可以设置以下环境变量
export PYTORCH_ENABLE_MPS_FALLBACK=1  # MPS 不支持的操作自动回退到 CPU
```

### GPU 内存优化

```bash
# 对于 8GB 基础配置，推荐启用这些优化
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0  # 更激进的内存管理
```

### 并发推理

M4 Pro 支持较好的并发性能：

```bash
# 使用多进程批量处理
python -m concurrent.futures demo/realtime_model_inference_from_file.py ...
```

## 🔧 高级配置

### 使用 uvicorn 自定义服务器

```bash
# 更多控制的方式启动服务器
MODEL_PATH=microsoft/VibeVoice-Realtime-0.5B \
MODEL_DEVICE=mps \
uvicorn demo.web.app:app \
  --host 0.0.0.0 \
  --port 8080 \
  --workers 2 \
  --reload
```

### 开发模式

```bash
# 启用自动重载（开发时使用）
python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --reload
```

## 🐛 常见问题

### 问题 1: OpenSSL 警告

**症状**: 看到 `NotOpenSSLWarning` 警告

**解决方案**:
```bash
# 使用 Homebrew 的 Python（包含 OpenSSL）
brew install python@3.11
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
uv pip install -e .
```

### 问题 2: MPS 不可用

**症状**: `torch.backends.mps.is_available()` 返回 `False`

**检查清单**:
- ✓ 确认运行在 Apple Silicon（arm64）
- ✓ PyTorch 版本 ≥ 1.12.0
- ✓ 虚拟环境配置正确

**解决方案**:
```bash
# 重新安装 PyTorch（确保 arm64 版本）
pip uninstall torch
pip install --upgrade torch
```

### 问题 3: 模型下载缓慢

**症状**: 首次运行下载 2-3GB 模型很慢

**解决方案**:
```bash
# 1. 检查网络连接
# 2. 使用 HuggingFace 代理（如果在中国）
export HF_ENDPOINT=https://hf-mirror.com

# 3. 或手动下载后指定路径
huggingface-cli download microsoft/VibeVoice-Realtime-0.5B --local-dir ./models
python demo/vibevoice_realtime_demo.py --model_path ./models
```

### 问题 4: MPS 内存不足

**症状**: `RuntimeError: out of memory` 相关错误

**解决方案**:
```bash
# 启用 MPS 回退到 CPU
export PYTORCH_ENABLE_MPS_FALLBACK=1

# 减小批处理大小或使用 CPU 模式
python demo/vibevoice_realtime_demo.py \
  --device cpu \
  --port 8001
```

## 📊 性能基准

在 Mac mini M4 Pro 基础配置上的预期性能：

| 任务 | 设备 | 速度 | 备注 |
|------|------|------|------|
| 初始化 | MPS | ~30秒 | 首次加载模型 |
| 实时 TTS | MPS | 300ms+ | 生成首个可听音频 |
| 批量推理 | MPS | ~0.5x实时 | 依赖文本长度 |
| 初始化 | CPU | ~60秒 | 不推荐用于实时 |

## 🔗 相关资源

- [PyTorch MPS 文档](https://pytorch.org/docs/stable/notes/mps.html)
- [VibeVoice 技术报告](https://arxiv.org/pdf/2508.19205)
- [Hugging Face 模型](https://huggingface.co/microsoft/VibeVoice-Realtime-0.5B)

## 📝 环境信息

此配置基于以下环境验证：

```
Platform: macOS-26.2-arm64 (Sonoma/Sequoia)
Machine: arm64
Python: 3.13.7
PyTorch: 2.10.0
MPS: Enabled ✅
```

---

如有问题，请参考主 [README.md](../README.md) 或提交 Issue。
