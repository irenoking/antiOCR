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
git clone [https://github.com/irenoking/anti-ocr-clipboard-shield.git](https://github.com/irenoking/anti-ocr-clipboard-shield.git)
cd anti-ocr-clipboard-shield

```

### 2. 安装依赖库

打开命令行（CMD 或 PowerShell），运行以下命令安装专门处理图像和 Windows 剪贴板的依赖：

```bash
pip install pillow pywin32

```

---

## 🚀 使用方法

### 基础运行

在项目根目录下，直接运行脚本：

```bash
python anti_ocr_clipboard.py

```

保持命令行窗口开启。此时，您可以正常使用 `Win + Shift + S` 或 `PrtScn` 截屏。截屏完成后，控制台会刷出：

> 📸 捕获新截图 [800x600]，正在注入复合水波纹干涉场...
> ✅ 处理完成！已完美送回剪贴板，请去微信粘贴发送测试。

此时直接在微信、钉钉或任何社交软件中粘贴发送即可。

### 🤫 进阶：后台完全隐形运行

如果您不想开着黑色的控制台窗口，可以将脚本文件的后缀名从 `.py` 改为 **`.pyw`**（例如 `anti_ocr_clipboard.pyw`）。

在 Windows 中，`.pyw` 格式会由后台的 `pythonw.exe` 静默启动，没有任何窗口。

* **开机自启**：按下 `Win + R` 输入 `shell:startup` 打开系统启动文件夹，将该 `.pyw` 文件的快捷方式拖入其中即可。
* **彻底关闭**：若想停止服务，只需打开 Windows 任务管理器，结束名为 `pythonw.exe` 的进程。

---

## ⚠️ 免责声明与技术边界

1. **猫鼠游戏提示**：本工具针对的是 2026 年主流多模态模型（如微信自带 OCR 等云端大模型）的视觉检测特性。由于深度学习模型具有强大的泛化性，不能保证对所有未来的闭源或特定领域的专用 OCR 引擎达到 100% 混淆效果。
2. **场景适用**：对于对比度极高的大字，AI 的纠错能力极强。建议在截取包含大段敏感文本、小字段落、网页表格等场景下使用本工具，防抓取效果最佳。

---

## 📄 开源协议

本项目基于 **MIT License** 协议开源，详情请参阅 [LICENSE](https://www.google.com/search?q=LICENSE) 文件。

