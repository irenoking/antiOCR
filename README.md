# 🌊 Anti-OCR Clipboard Shield (多重流体水波纹防 OCR 剪贴板护盾)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-orange.svg)](https://www.microsoft.com/)

**Anti-OCR Clipboard Shield** 是一款专为 Windows 用户设计的后台隐私保护工具。它能够实时监听系统剪贴板，当检测到用户进行系统截屏（如 `Win + Shift + S` 或 `PrtScn`）时，自动对图片注入**多重流体水波纹干涉场**，在**完全不影响人类肉眼阅读**的前提下，让现代多模态大模型（如微信“图片大爆炸”、各类云端 VLM 引擎）的 OCR 文字提取彻底失效。

---

## ✨ 核心特性

- **🚀 零感无缝拦截**：后台静默运行，无需手动导入图片。截屏后自动魔改，直接在聊天软件中 `Ctrl + V` 发送的就是防 OCR 版本。
- **👁️ 人类视觉友好**：抛弃了传统辣眼睛的“黑白雪花点”或“高频马赛克”。处理后的图像极其整洁，文字不打碎、不变色，利用人类视觉的流体补偿本能，实现一秒无障碍阅读。
- **🛡️ 针对多模态 VLM 的数学级防御**：传统的低通滤波或去燥算法可以轻松洗掉像素级噪点。本工具采用 3 层不同频段的非线性三角函数复合干涉，直接破坏 AI 卷积核的局部梯度特征与位置编码。
- **⚡ 极速内存处理**：完全基于 Python `Pillow` 的内存矩阵运算与 Windows 剪贴板底层 DIB 映射，响应时间低于 0.1 秒，不占 CPU。

---

## 🔬 对抗原理（Why It Works）

现代多模态大模型（Vision-Language Models）的 OCR 不再依赖传统的字形匹配，而是通过 Vision Transformer 将图片切分成固定大小的视觉块（Patch），并利用强大的**上下文语义概率预测（Context Prior）**进行强行纠错补全。

本项工具的对抗策略类似于雷达信号处理中的**多径干涉（Multipath Interference）**：

1. **宏观低频波（破坏行检测）**：产生大周期的正弦波动，物理上推歪文本行的边界，让 AI 的文本行检测框（Bounding Box）发生整体形变。
2. **中观扭曲波（解构字形骨架）**：改变汉字横竖笔画的空间拓扑关系。
3. **微观高频毛刺波（1像素绝杀）**：精确到单像素级的交错拉扯。对于高密度的“小字段落”，AI 在将 $Patch \to Token$ 映射时，其内部的注意力权重矩阵（Attention Matrix）会彻底发生相位失配（Phase Mismatch），解码出的内容将变成完全无法阅读的乱码。

---

## 📦 安装指南

在使用前，请确保您的 Windows 系统已安装 Python 3.8 或更高版本。

### 1. 克隆仓库
```bash
git clone [https://github.com/YourUsername/anti-ocr-clipboard-shield.git](https://github.com/YourUsername/anti-ocr-clipboard-shield.git)
cd anti-ocr-clipboard-shield
