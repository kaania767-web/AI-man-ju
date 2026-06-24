"""
漫剧视频合成管线《浪漫主义流浪家》
将 28 张分镜图合成为完整漫剧视频：
  - Ken Burns 效果（缓推/平移）
  - 对话气泡 + 旁白字幕
  - 场景间交叉淡入淡出
  - 输出 1920×1080 @ 24fps MP4
"""

import os
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageSequenceClip

# ── 路径 ──
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE, "output")
VIDEO_OUTPUT = os.path.join(BASE, "output", "浪漫主义流浪家_漫剧.mp4")

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/yahei.ttf",
]
FONT_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
]

# ── 渲染参数 ──
TARGET_W, TARGET_H = 1920, 1080
FPS = 24
CROSSFADE_SEC = 0.5
SCENE_LABEL_DURATION = 3.5
TEXT_FADE_SEC = 0.15
KB_PAN_SCALE = 0.3

# ── 文字布局常量 ──
NARRATION_Y = 0.65       # 旁白垂直位置（相对于画面高度比例）
DIALOGUE_BOTTOM = 60     # 对话气泡距底边像素
TITLE_Y_OFFSET = 40      # 标题垂直居中偏移
SUBTITLE_Y = 0.55        # 副标题位置
CREDIT_Y = 0.6           # 片尾字幕位置

# ── 字体加载 ──
_FONT_CACHE = {}

def _get_font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        candidates = FONT_BOLD_CANDIDATES if bold else FONT_CANDIDATES
        path = None
        for p in candidates:
            if os.path.exists(p):
                path = p
                break
        if not path:
            raise RuntimeError("未找到中文字体，请安装微软雅黑")
        _FONT_CACHE[key] = ImageFont.truetype(path, size)
    return _FONT_CACHE[key]


# ═══════════════════════════════════════════
#  文字渲染
# ═══════════════════════════════════════════

def _wrap_text(text, font, max_width, padding_x):
    """将文本按最大宽度换行，返回行列表。"""
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for ch in paragraph:
            test = current + ch
            w = font.getbbox(test)[2] - font.getbbox(test)[0]
            if w > max_width - padding_x * 2 and current:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
    return lines


def _make_text_image(text, font_size=38, text_color=(255, 255, 255),
                     bg_color=(0, 0, 0, 160), padding=(24, 12),
                     max_width=1600, speaker=None):
    """渲染带半透明背景的文字条，返回 PIL RGBA Image。"""
    font = _get_font(font_size)
    lines = _wrap_text(text, font, max_width, padding[0])

    # 若行数过多缩小字号
    if len(lines) > 4:
        font = _get_font(int(font_size * 0.82))
        lines = _wrap_text(text, font, max_width, padding[0])

    line_data = []
    total_text_h = 0
    max_line_w = 0
    for line in lines:
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_data.append((line, lw, lh))
        total_text_h += lh
        max_line_w = max(max_line_w, lw)

    line_gap = 6
    total_text_h += line_gap * (len(lines) - 1)

    label_h = 0
    if speaker:
        label_font = _get_font(max(int(font_size * 0.65), 18), bold=True)
        label_h = (label_font.getbbox(speaker)[3] - label_font.getbbox(speaker)[1]) + 4

    pad_l, pad_r = padding[0], padding[0]
    pad_t, pad_b = padding[1], padding[1]

    img_w = max_line_w + pad_l + pad_r
    total_h = total_text_h + pad_t + pad_b + label_h + (4 if label_h else 0)

    img = Image.new("RGBA", (img_w, total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(2, 0), (img_w - 2, total_h)], radius=8, fill=bg_color)

    y = pad_t
    if speaker:
        label_font = _get_font(max(int(font_size * 0.65), 18), bold=True)
        draw.text((pad_l + 4, y), speaker, font=label_font, fill=(232, 160, 64, 255))
        y += (label_font.getbbox(speaker)[3] - label_font.getbbox(speaker)[1]) + 4

    for line, lw, lh in line_data:
        x = (img_w - lw) // 2
        draw.text((x, y), line, font=font, fill=text_color + (255,))
        y += lh + line_gap

    return img


def _render_text_on_frame(base_img, text_data, t_sec):
    """在帧上叠加一条文字（对话/旁白/标题）。"""
    ttype = text_data.get("type", "dialogue")
    text = text_data.get("text", "")
    start = text_data.get("start", 0)
    end = text_data.get("end", 0)

    if t_sec < start or t_sec > end:
        return base_img

    # 淡入淡出
    alpha = 1.0
    if t_sec - start < TEXT_FADE_SEC:
        alpha = (t_sec - start) / TEXT_FADE_SEC
    elif end - t_sec < TEXT_FADE_SEC:
        alpha = (end - t_sec) / TEXT_FADE_SEC
    if alpha <= 0:
        return base_img

    font_size = text_data.get("font_size", 34)

    if ttype == "narration":
        text_color = (200, 195, 185)
        bg_color = (0, 0, 0, int(140 * alpha))
        max_w = int(TARGET_W * 0.7)
        text_pil = _make_text_image(
            text, font_size=font_size, text_color=text_color,
            bg_color=bg_color, padding=(28, 16), max_width=max_w,
        )
        pos_y = int(TARGET_H * NARRATION_Y)
    elif ttype in ("title", "subtitle", "credit"):
        color_map = {"title": (240, 238, 230), "subtitle": (200, 195, 185), "credit": (200, 195, 185)}
        text_color = color_map.get(ttype, (255, 255, 255))
        bg_color = (0, 0, 0, int(100 * alpha))
        max_w = TARGET_W - 200
        text_pil = _make_text_image(
            text, font_size=font_size, text_color=text_color,
            bg_color=bg_color, padding=(40, 20), max_width=max_w,
        )
        y_map = {"title": TARGET_H // 2 - text_pil.size[1] // 2 - TITLE_Y_OFFSET,
                 "subtitle": int(TARGET_H * SUBTITLE_Y),
                 "credit": int(TARGET_H * CREDIT_Y)}
        pos_y = y_map.get(ttype, int(TARGET_H * 0.6))
    else:  # dialogue
        text_color = (255, 255, 255)
        bg_color = (0, 0, 0, int(160 * alpha))
        max_w = int(TARGET_W * 0.8)
        text_pil = _make_text_image(
            text, font_size=font_size, text_color=text_color,
            bg_color=bg_color, padding=(24, 12), max_width=max_w,
            speaker=text_data.get("speaker"),
        )
        pos_y = TARGET_H - text_pil.size[1] - DIALOGUE_BOTTOM

    # 缩放适配
    tw, th = text_pil.size
    scale = min(TARGET_W * 0.85 / tw, 1.0)
    if scale < 1:
        text_pil = text_pil.resize((int(tw * scale), int(th * scale)), Image.LANCZOS)

    pos_x = (TARGET_W - text_pil.size[0]) // 2
    result = base_img.copy()
    if text_pil.mode == "RGBA":
        result.paste(text_pil, (pos_x, pos_y), text_pil)
    else:
        result.paste(text_pil, (pos_x, pos_y))
    return result


# ═══════════════════════════════════════════
#  Ken Burns
# ═══════════════════════════════════════════

def apply_ken_burns(img_pil, start_zoom, end_zoom, pan_x=0, pan_y=0, progress=0.0):
    """Ken Burns 运镜：smoothstep 缓动 + 缩放 + 平移。"""
    p = progress * progress * (3 - 2 * progress)  # smoothstep
    zoom = start_zoom + (end_zoom - start_zoom) * p
    src_w, src_h = img_pil.size

    crop_w = max(1, int(src_w / zoom))
    crop_h = max(1, int(src_h / zoom))
    px = int(pan_x * p * KB_PAN_SCALE)
    py = int(pan_y * p * KB_PAN_SCALE)

    left = max(0, min((src_w - crop_w) // 2 + px, src_w - crop_w))
    top = max(0, min((src_h - crop_h) // 2 + py, src_h - crop_h))

    cropped = img_pil.crop((left, top, left + crop_w, top + crop_h))
    return cropped.resize((TARGET_W, TARGET_H), Image.LANCZOS)


# ═══════════════════════════════════════════
#  场景标签
# ═══════════════════════════════════════════

def _make_scene_label_img(label_text):
    """生成金色场景标签图像。"""
    font = _get_font(22, bold=True)
    bbox = font.getbbox(label_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = (16, 8)
    img = Image.new("RGBA", (tw + pad[0] * 2, th + pad[1] * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (img.size[0] - 1, img.size[1] - 1)], radius=4,
                           fill=(232, 160, 64, 200))
    draw.text((pad[0], pad[1] - 2), label_text, font=font, fill=(13, 13, 26, 255))
    return img


# ═══════════════════════════════════════════
#  单镜头帧序列
# ═══════════════════════════════════════════

def render_shot(shot):
    """为一个镜头生成所有帧的 numpy 数组列表。"""
    shot_id = shot["id"]
    duration = shot["duration"]
    num_frames = max(1, int(duration * FPS))

    img_path = os.path.join(OUTPUT_DIR, shot["image"])
    if not os.path.exists(img_path):
        print(f"  WARNING: 找不到图片 {img_path}，使用占位图")
        src_img = Image.new("RGB", (1024, 576), (20, 20, 40))
    else:
        src_img = Image.open(img_path).convert("RGB")

    kb = shot.get("ken_burns", {})
    zoom_start = kb.get("zoom_start", 1.0)
    zoom_end = kb.get("zoom_end", 1.05)
    pan_x = kb.get("pan_x", 0)
    pan_y = kb.get("pan_y", 0)

    scene_label_img = None
    if shot.get("scene_label"):
        scene_label_img = _make_scene_label_img(shot["scene_label"])

    fade_in_dur = shot.get("fade_in", CROSSFADE_SEC)
    fade_out_dur = CROSSFADE_SEC

    frames = []
    for fi in range(num_frames):
        t = fi / FPS
        progress = fi / max(1, num_frames - 1) if num_frames > 1 else 0

        frame = apply_ken_burns(src_img, zoom_start, zoom_end, pan_x, pan_y, progress)

        alpha = 1.0
        if t < fade_in_dur and fade_in_dur > 0:
            alpha = min(1.0, t / fade_in_dur)
        elif duration - t < fade_out_dur and fade_out_dur > 0:
            alpha = max(0.0, (duration - t) / fade_out_dur)
        if alpha < 1.0:
            black = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
            frame = Image.blend(black, frame, alpha)

        if scene_label_img and t < SCENE_LABEL_DURATION:
            label_alpha = min(1.0, (SCENE_LABEL_DURATION - t) / 0.5) if t > SCENE_LABEL_DURATION - 0.5 else 1.0
            if label_alpha > 0:
                frame = frame.copy()
                if scene_label_img.mode == "RGBA":
                    frame.paste(scene_label_img, (20, 16), scene_label_img)

        for td in shot.get("texts", []):
            frame = _render_text_on_frame(frame, td, t)

        frames.append(np.array(frame))

    return frames


# ═══════════════════════════════════════════
#  交叉淡入淡出
# ═══════════════════════════════════════════

def crossfade_frames(frames_a, frames_b, fade_frames):
    if fade_frames <= 0:
        return frames_a + frames_b
    result = list(frames_a[:-fade_frames]) if len(frames_a) > fade_frames else []
    overlap = min(fade_frames, len(frames_a), len(frames_b))
    for i in range(overlap):
        a_idx = len(frames_a) - overlap + i
        b_idx = i
        alpha = (i + 1) / (overlap + 1)
        blended = (frames_a[a_idx].astype(np.float32) * (1 - alpha) +
                   frames_b[b_idx].astype(np.float32) * alpha)
        result.append(blended.astype(np.uint8))
    result.extend(frames_b[overlap:])
    return result


# ═══════════════════════════════════════════
#  主合成
# ═══════════════════════════════════════════

def render_video():
    from shots import SHOTS

    print("=" * 60)
    print("  漫剧视频合成  《浪漫主义流浪家》")
    print(f"  镜头数: {len(SHOTS)}")
    print(f"  分辨率: {TARGET_W}x{TARGET_H} @ {FPS}fps")
    print(f"  输出:   {VIDEO_OUTPUT}")
    print("=" * 60)

    t_start = time.time()
    all_frames = []
    total_dur = 0.0
    fade_frame_count = int(CROSSFADE_SEC * FPS)

    for i, shot in enumerate(SHOTS):
        shot_id = shot["id"]
        dur = shot["duration"]
        shot_t = time.time()
        print(f"[{i+1}/{len(SHOTS)}] {shot_id} ({dur:.0f}s) ... ", end="", flush=True)

        frames = render_shot(shot)
        elapsed = time.time() - shot_t
        remaining = len(SHOTS) - (i + 1)
        avg = (time.time() - t_start) / (i + 1)
        eta = avg * remaining
        print(f"{len(frames)} 帧 ({elapsed:.1f}s, ETA: {eta:.0f}s)")

        if i == 0:
            all_frames = frames
        else:
            all_frames = crossfade_frames(all_frames, frames, fade_frame_count)
        total_dur += dur

    print(f"\n帧渲染完成: {len(all_frames)} 帧, {total_dur:.0f}s")
    print("写入视频文件...")
    write_t = time.time()

    clip = ImageSequenceClip(all_frames, fps=FPS)
    clip.write_videofile(
        VIDEO_OUTPUT, fps=FPS, codec="libx264", audio_codec="aac",
        bitrate="8000k", preset="medium", threads=4, logger=None,
    )
    clip.close()

    total = time.time() - t_start
    print(f"\n{'=' * 60}")
    print(f"  合成完成！时长: {total_dur:.1f}s ({total_dur/60:.1f} min)")
    print(f"  帧数: {len(all_frames)}, 耗时: {total:.0f}s ({total/60:.1f} min)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    render_video()
