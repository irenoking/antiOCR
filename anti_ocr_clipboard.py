import time
import io
import random
import math
import numpy as np
from PIL import Image, ImageGrab, ImageDraw, ImageFont
import win32clipboard

def get_random_noise_char():
    chars = "一二三四五六七八九十abcdefgABCDEFG!@#$%^&*"
    return random.choice(chars)

def get_random_char():
    chars = "一二三四五六七八九十abcdefgABCDEFG!@#$%^&*"
    return random.choice(chars)

def get_random_chinese_char():
    val = random.randint(0x4e00, 0x9fa5)
    return chr(val)

def advanced_semantic_mask(image):
    img = image.convert("RGBA")
    width, height = img.size
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("msyh.ttc", 16)
    except IOError:
        font = ImageFont.load_default()
        
    for y in range(4, height, 14):
        for x in range(2, width, 12):
            if random.random() < 0.7:
                draw.text((x, y), get_random_noise_char(), fill=(120, 120, 120, 90), font=font)
                
    for i in range(0, height, 24):
        y_base = i + random.randint(-3, 3)
        for x in range(0, width, 15):
            if random.random() < 0.8:
                draw.line([(x, y_base), (x + 8, y_base + random.randint(-1, 1))], 
                          fill=(130, 130, 130, 110), width=1)
    img_masked = Image.alpha_composite(img, overlay).convert("RGB")
    skew_factor = random.choice([-0.015, 0.015])
    img_skewed = img_masked.transform((width, height), Image.AFFINE, (1, skew_factor, 0, 0, 1, 0), resample=Image.BILINEAR, fillcolor=(255, 255, 255))
    return img_skewed

def ultimate_physical_noise(image):
    img = image.convert("RGBA")
    width, height = img.size
    filter_layer = Image.new("RGBA", (width, height), (200, 160, 100, 40))
    img = Image.alpha_composite(img, filter_layer)
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    num_lines = random.randint(15, 25)
    for _ in range(num_lines):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255), 100)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=random.choice([3, 4, 5]))
        
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

    for _ in range(1500):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        color = (random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255]), 140)
        draw.point((x, y), fill=color)

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
        
    final_rgba = Image.alpha_composite(img, overlay)
    return final_rgba.convert("RGB")

def multi_water_ripple_anti_ocr(image):
    img = image.convert("RGB")
    width, height = img.size
    out_img = Image.new("RGB", (width, height))
    pixels_in = img.load()
    pixels_out = out_img.load()
    
    phase1 = random.uniform(0, math.pi)
    phase2 = random.uniform(0, math.pi)
    phase3 = random.uniform(0, math.pi)
    
    offset_x = []
    for y in range(height):
        w1 = 3.5 * math.sin(y / 14.0 + phase1)
        w2 = 2.0 * math.cos(y / 6.0 + phase2)
        w3 = 1.2 * math.sin(y * 1.62 + phase3)
        offset_x.append(int(w1 + w2 + w3))
        
    offset_y = []
    for x in range(width):
        w1 = 3.0 * math.cos(x / 16.0 + phase2)
        w2 = 1.8 * math.sin(x / 7.0 + phase3)
        w3 = 1.0 * math.cos(x * 1.85 + phase1)
        offset_y.append(int(w1 + w2 + w3))
        
    for y in range(height):
        for x in range(width):
            orig_x = max(0, min(width - 1, x + offset_x[y]))
            orig_y = max(0, min(height - 1, y + offset_y[x]))
            pixels_out[x, y] = pixels_in[orig_x, orig_y]
            
    scale_w = random.choice([0.99, 1.01])
    if scale_w != 1.0:
        out_img = out_img.resize((int(width * scale_w), height), Image.BILINEAR)
    return out_img

def get_clipboard_image_safe():
    """安全读取剪贴板图片（兼容截屏数据与复制的图像文件）"""
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
    data = output.getvalue()[14:]  # 剥离 BMP 文件头取得 DIB 数据
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

def generate_image_fingerprint(img):
    """
    升级版图像指纹生成器：
    不仅记录尺寸，同时抽取图像头部、中部和尾部的像素片段进行哈希指纹绑定。
    能完美区分大小一致、但内容不同的普通复制图片。
    """
    if not img:
        return None
    try:
        raw_bytes = img.tobytes()
        length = len(raw_bytes)
        # 抽取头部、中部、尾部三个定位点的字节片段，避免判定碰撞
        if length > 300:
            fingerprint_data = raw_bytes[:100] + raw_bytes[length//2:length//2+100] + raw_bytes[-100:]
        else:
            fingerprint_data = raw_bytes
        return (img.size, fingerprint_data)
    except:
        return (img.size, img.mode)

def main():
    print("🎨 终极剪贴板/截屏全向防护工具已启动...")
    print("当前策略：多重水波纹 + 物理噪层 + 语义伪装（三重混合防御）")
    print("支持场景：[Win+Shift+S系统截屏] 以及 [网页/任意软件中直接复制图片]\n")
    
    last_processed_fingerprint = None
    
    while True:
        try:
            img = get_clipboard_image_safe()
            if img:
                # 生成高灵敏度的图像唯一指纹
                current_fingerprint = generate_image_fingerprint(img)
                
                # 如果当前剪贴板里的图和上次处理完的图指纹不同，说明有“新图”进来了（不论是截屏还是复制）
                if current_fingerprint != last_processed_fingerprint:
                    print(f"📸 检测到剪贴板新图像进入 (尺寸: {img.size})，正在执行抗 OCR 魔改...")
                    
                    # 依次运行你的复合对抗算法链
                    protected_img = advanced_semantic_mask(ultimate_physical_noise(multi_water_ripple_anti_ocr(img)))
                    
                    # 提前保存魔改后的新图指纹，防止重新写入剪贴板时二次触发自身
                    last_processed_fingerprint = generate_image_fingerprint(protected_img)
                    
                    # 将魔改后的图片送回剪贴板覆盖
                    if send_image_to_clipboard_safe(protected_img):
                        print("✅ 防御层注入成功！已覆盖剪贴板，可直接粘贴发送。\n")
            else:
                # 剪贴板中不是图片（如复制了文字或清空），重置指纹缓存
                last_processed_fingerprint = None
                
        except Exception as e:
            print(f"监听运行异常: {e}")
            
        time.sleep(0.4) # 保持超轻量轮询

if __name__ == "__main__":
    main()
