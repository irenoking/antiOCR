import time
import io
import random
import math
import numpy as np
from PIL import Image, ImageGrab, ImageDraw, ImageFont
import win32clipboard


def multi_water_ripple_anti_ocr(image):
    """
    核心算法：多重流体水波纹干涉
    通过 3 层不同周期、不同振幅的正余弦波相互叠加，形成复杂的流体折射场。
    对小字和大字实施无差别局部梯度破坏，而人眼能利用流体视觉补偿轻松阅读。
    """
    img = image.convert("RGB")
    width, height = img.size
    
    out_img = Image.new("RGB", (width, height))
    pixels_in = img.load()
    pixels_out = out_img.load()
    
    # === 预计算多重水波纹的复合干涉矩阵 ===
    # 随机生成微幅相位差，防止每次截图的变形规律被 AI 固化识别
    phase1 = random.uniform(0, math.pi)
    phase2 = random.uniform(0, math.pi)
    phase3 = random.uniform(0, math.pi)
    
    # 1. 预计算 X 方向的复合偏移（由3个不同频段的波叠加而成）
    offset_x = []
    for y in range(height):
        # 第一重波：宏观大波纹（大周期，用于推歪整体字体行检测框）
        w1 = 3.5 * math.sin(y / 14.0 + phase1)
        # 第二重波：中观水波纹（中周期，扭曲字形骨架）
        w2 = 2.0 * math.cos(y / 6.0 + phase2)
        # 第三重波：微观纳米级毛刺波（极小周期，专门针对小字的局部边缘检测）
        w3 = 1.2 * math.sin(y * 1.62 + phase3)
        
        offset_x.append(int(w1 + w2 + w3))
        
    # 2. 预计算 Y 方向的复合偏移（提供纵向的拉扯扭曲）
    offset_y = []
    for x in range(width):
        w1 = 3.0 * math.cos(x / 16.0 + phase2)
        w2 = 1.8 * math.sin(x / 7.0 + phase3)
        w3 = 1.0 * math.cos(x * 1.85 + phase1)
        
        offset_y.append(int(w1 + w2 + w3))
        
    # === 执行二维非线性逆向流体映射 (Backward Mapping) ===
    # 逆向映射能够完美保证处理后的图像没有黑点和多余的空洞
    for y in range(height):
        for x in range(width):
            # 计算受多重水波纹干扰后的原始像素坐标
            orig_x = x + offset_x[y]
            orig_y = y + offset_y[x]
            
            # 边界安全拦截（防止溢出画布边界）
            orig_x = max(0, min(width - 1, orig_x))
            orig_y = max(0, min(height - 1, orig_y))
            
            pixels_out[x, y] = pixels_in[orig_x, orig_y]
            
    # === 微幅长宽比弹性微调 ===
    # 每次随机微调 1% 左右的尺寸，强制改变图像的全局拉伸特征
    scale_w = random.choice([0.99, 1.01])
    if scale_w != 1.0:
        out_img = out_img.resize((int(width * scale_w), height), Image.BILINEAR)
            
    return out_img

def get_random_char():
    """生成随机特殊干扰字符，用来污染 AI 的 Token 提取器"""
    chars = "一二三四五六七八九十★▲■●◆0123456789X#"
    return random.choice(chars)

def ultimate_physical_noise(image):
    """
    终极物理干扰算法：
    1. 截图文字和背景整体变色，大幅度降低对比度。
    2. 产生随机的高对比度彩色干扰线与多边形图案（直接从物理空间遮挡笔画，使 AI 去噪算法失效）。
    3. 密集添加中等大小的彩色干扰文字和图案（强行注入语义，让 AI 识别出的全都是乱码）。
    """
    # 强制转换为带有透明通道的图形，方便图层叠加
    img = image.convert("RGBA")
    width, height = img.size
    
    # 阶段 1：文字变色与明度干预（给原图上一层淡淡的彩色滤镜，缩小文字与背景的灰度差）
    # 制造一个暗金色调/暗蓝调（根据截屏背景自动平衡，这里使用高隐蔽暖色调）
    filter_layer = Image.new("RGBA", (width, height), (200, 160, 100, 40))
    img = Image.alpha_composite(img, filter_layer)
    
    # 创建专门的干扰层
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 阶段 2：注入彩色随机粗线条（穿透池化层，直击大模型骨架检测）
    # 使用中等粗度（3-5像素），这在 AI 进行下采样时无法被丢弃，但人类可以通过颜色区分自动过滤
    num_lines = random.randint(15, 25)
    for _ in range(num_lines):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        # 随机鲜艳彩色
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255), 100)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=random.choice([3, 4, 5]))
        
    # 阶段 3：添加随机背景几何图案（圆形/矩形）
    num_shapes = random.randint(8, 15)
    for _ in range(num_shapes):
        x1 = random.randint(0, width - 40)
        y1 = random.randint(0, height - 40)
        x2 = x1 + random.randint(20, 50)
        y2 = y1 + random.randint(20, 50)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 60)
        if random.random() < 0.5:
            draw.ellipse([x1, y1, x2, y2], fill=color)
        else:
            draw.rectangle([x1, y1, x2, y2], fill=color)

    # 阶段 4：添加高频高对比度干扰点
    for _ in range(1500):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        color = (random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255]), 140)
        draw.point((x, y), fill=color)

    # 阶段 5：注入实体干扰文字（字号设大，16-20像素，直接黏贴在原文字身上）
    try:
        font = ImageFont.truetype("msyh.ttc", 16)
    except IOError:
        font = ImageFont.load_default()
        
    num_chars = random.randint(25, 40)
    for _ in range(num_chars):
        x = random.randint(0, width - 20)
        y = random.randint(0, height - 20)
        color = (random.randint(30, 180), random.randint(30, 180), random.randint(30, 180), 120)
        draw.text((x, y), get_random_char(), fill=color, font=font)
        
    # 最终合并
    final_rgba = Image.alpha_composite(img, overlay)
    
    # 阶段 6：轻微拉伸，防止 Windows 剪贴板触发完全一致的缓存
    final_img = final_rgba.convert("RGB")
    scale_w = random.choice([0.99, 1.01])
    final_img = final_img.resize((int(width * scale_w), height), Image.BILINEAR)
    
    return final_img

def get_clipboard_image_safe():
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            return img
    except:
        pass
    return None

def send_image_to_clipboard_safe(image):
    output = io.BytesIO()
    image.save(output, format="BMP")
    data = output.getvalue()[14:]
    output.close()
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        return True
    except:
        try: win32clipboard.CloseClipboard()
        except: pass
        return False

def main():
    print("🎨 终极物理加噪版工具已启动...")
    print("当前策略：整体变色降对比 + 3-5px 彩色线条 + 几何斑块 + 实体汉字污染")
    print("文字不会被打碎，肉眼极易识别！正在死磕微信 OCR 预处理机制...\n")
    
    last_processed_fingerprint = None
    
    while True:
        try:
            img = get_clipboard_image_safe()
            if img:
                img_data = img.tobytes()[:100] if hasattr(img, 'tobytes') else b""
                current_fingerprint = (img.size, img_data) 
                
                if current_fingerprint != last_processed_fingerprint:
                    print(f"📸 捕获截图 {img.size}，正在注入强效物理混合噪声层...")
                    
                    protected_img = ultimate_physical_noise(multi_water_ripple_anti_ocr(ultimate_physical_noise(multi_water_ripple_anti_ocr(img))))
                    
                    protected_data = protected_img.tobytes()[:100] if hasattr(protected_img, 'tobytes') else b""
                    last_processed_fingerprint = (protected_img.size, protected_data)
                    
                    if send_image_to_clipboard_safe(protected_img):
                        print("✅ 魔改完成！去噪层已建立，请在微信中粘贴验证。")
            else:
                last_processed_fingerprint = None
                
        except Exception as e:
            print(f"运行异常: {e}")
            
        time.sleep(0.4)

if __name__ == "__main__":
    main()
