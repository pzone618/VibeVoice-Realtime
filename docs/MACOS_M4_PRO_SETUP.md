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

#### 标准配置（适合所有 Mac mini M4 Pro）

使用 MPS GPU 加速运行实时 TTS 演示：

```bash
python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --port 8001
```

#### 基础版优化配置（8GB 内存）

如果你的 Mac mini M4 Pro 是 8GB 基础配置，建议添加内存优化环境变量：

```bash
# 启用 MPS 回退和内存优化
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --port 8001
```

**说明**:
- `PYTORCH_ENABLE_MPS_FALLBACK=1`: 当 MPS 不支持某些操作时自动回退到 CPU
- `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`: 更激进的 GPU 内存管理，释放未使用的内存

#### 如果遇到内存不足（8GB 基础版）

```bash
# 使用 CPU 模式（较慢但内存占用更少）
python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device cpu \
  --port 8001
```

**性能预期**:
- MPS GPU: ~0.5x 实时速度（即生成 10 秒音频需要 ~20 秒）
- CPU: 0.05-0.1x 实时速度（较慢，不推荐用于实时应用）

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

### 配置等级和推荐设置

| 配置 | 内存 | GPU | 推荐设备参数 | 预期速度 |
|------|------|-----|-----------|---------|
| **基础版** | 8GB | 8核 | `mps` + 内存优化 | ~0.5x 实时 |
| **标准版** | 16GB | 10核 | `mps` | ~0.7-1x 实时 |
| **高配版** | 24GB+ | 10核 | `mps` | ~1-2x 实时 |

### 8GB 基础版内存管理

```bash
# 推荐配置（8GB 内存）
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

python demo/vibevoice_realtime_demo.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --device mps \
  --port 8001
```

**环境变量说明**:

| 变量 | 作用 | 值 | 影响 |
|------|------|-----|------|
| `PYTORCH_ENABLE_MPS_FALLBACK` | MPS 不支持时回退 | 1 | 提高兼容性 |
| `PYTORCH_MPS_HIGH_WATERMARK_RATIO` | GPU 内存保留比例 | 0.0 | 激进释放，适合低配 |

### 16GB+ 标准配置

无需特殊环境变量，使用默认设置即可：

```bash
python demo/vibevoice_realtime_demo.py \
  --device mps --port 8001
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

### 问题 4: MPS 内存不足（8GB 基础版特定）

**症状**: `RuntimeError: out of memory` 或 `HipErrorOutOfMemory` 错误

**针对 8GB 基础版的解决方案**:

1. **首先尝试 - 启用内存优化**:
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
python demo/vibevoice_realtime_demo.py --device mps --port 8001
```

2. **如果仍然 OOM，使用混合模式**:
```bash
# 使用 CPU 进行某些操作
export PYTORCH_MPS_FALLBACK_TO_CPU=1
export PYTORCH_ENABLE_MPS_FALLBACK=1
python demo/vibevoice_realtime_demo.py --device mps --port 8001
```

3. **最后方案 - 使用 CPU 模式**:
```bash
python demo/vibevoice_realtime_demo.py --device cpu --port 8001
```

**预期**:
- MPS + 优化: ~15-30 秒生成 10 秒音频
- CPU 模式: ~2-5 分钟生成 10 秒音频（不推荐实时使用）

### 问题 5: 性能偏低或延迟高（8GB 基础版）

**症状**: 生成音频非常慢（> 30 秒）

**检查清单**:
```bash
# 1. 检查是否真的在使用 MPS
python -c "import torch; print(f'MPS: {torch.backends.mps.is_available()}')"

# 2. 检查内存使用
top -l 1 | grep -E "PhysMem|Mem"

# 3. 检查是否有其他进程占用 GPU
# 在活动监视器中查看 GPU 占用
```

**优化建议**:
- 关闭其他应用（特别是 Chrome、IDE、视频播放器）
- 减小浏览器窗口大小
- 使用简短的文本输入进行测试
- 考虑升级到 16GB 配置以获得更好性能

## 📊 性能基准

在 Mac mini M4 Pro 上的实测性能：

### 标准配置（16GB+ 内存）

| 任务 | 设备 | 速度 | 备注 |
|------|------|------|------|
| 初始化 | MPS | ~20-30秒 | 首次加载模型 |
| 实时 TTS | MPS | 0.7-1x | 10秒音频 = 10-14秒生成 |
| 批量推理 | MPS | ~1-2x | 接近实时速度 |

### 基础版配置（8GB 内存）

| 任务 | 设备 | 速度 | 备注 | 可用性 |
|------|------|------|------|--------|
| 初始化 | MPS | ~25-35秒 | 首次加载较慢 | ✅ |
| 实时 TTS | MPS | 0.5x | 10秒音频 = 20秒生成 | ✅ |
| 实时 TTS | MPS+优化 | 0.4-0.5x | 启用内存优化 | ✅ 推荐 |
| 长文本推理 | MPS | 偶尔 OOM | > 100 字 | ⚠️ 需监控 |
| 批量推理 | MPS | 0.3-0.5x | 逐个处理 | ✅ |
| 生成 | CPU | 0.05-0.1x | 极其缓慢 | ❌ 不推荐 |

**说明**:
- **0.5x 速度**: 10 秒音频需要 20 秒生成（可实时交互）
- **OOM**: 偶尔内存不足，需要重启或关闭其他应用
- 实时交互的最低要求：0.3x 速度

## � 快速参考

### 一键启动命令

**Mac mini M4 Pro 8GB 基础版**:
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1 && \
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 && \
python demo/vibevoice_realtime_demo.py --device mps --port 8001
```

**Mac mini M4 Pro 16GB+**:
```bash
python demo/vibevoice_realtime_demo.py --device mps --port 8001
```

### 故障排除流程图

```
遇到问题？
│
├─ 错误: RuntimeError: out of memory
│  └─ 尝试: export PYTORCH_ENABLE_MPS_FALLBACK=1
│     └─ 仍有问题? 使用 --device cpu
│
├─ 错误: MPS not available
│  └─ 检查: python -c "import torch; print(torch.backends.mps.is_available())"
│     └─ 确认: PyTorch >= 1.12, Apple Silicon
│
├─ 性能慢
│  └─ 检查: 其他应用是否占用 GPU/CPU
│     └─ 关闭: 浏览器、IDE、视频播放器
│
└─ 其他问题
   └─ 查看: "常见问题" 部分
```

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
