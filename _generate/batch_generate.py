"""
AI漫剧 批量生成管线

启动 ComfyUI → 遍历全部分镜 prompt → 生成图片 → 保存到 output/

用法:
    python batch_generate.py
"""

import os
import sys
import time
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import start, stop, generate
from workflow import build_workflow

OUTPUT_DIR = r"C:\Users\唐文浚\Documents\AI漫剧\output"
NEGATIVE = (
    "nsfw, ugly, deformed, bad anatomy, blurry, low quality, "
    "worst quality, bad proportions, monochrome, text, watermark, "
    "extra limbs, mutated, deformed, bad hands, missing fingers"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


PROMPTS = {
    # ---- 角色定妆 ----
    "00a_郑新定妆": (
        "(masterpiece, best quality), portrait of a 30-year-old Chinese man, slim, "
        "tanned skin, messy short hair, slight curls, slight stubble, beige linen shirt, "
        "beach, backlight, golden hour, sunset rim light, gentle smile, windblown hair, "
        "cinematic lighting, shallow depth of field, warm tones, photorealistic",
        42
    ),
    "00b_我定妆": (
        "(masterpiece, best quality), portrait of a 30-year-old Chinese man, friendly face, "
        "fair skin, short hair, light blue shirt, balcony, lounge chair, morning sunlight, "
        "warm lighting, calm expression, slight smile, soft tones, photorealistic, cinematic",
        43
    ),
    # ---- Scene 1 平潭海边·重逢 ----
    "01-1_落日海面全景": (
        "(masterpiece, best quality), wide angle, vast sea surface, sunset golden hour, "
        "sparkling water, warm orange to purple sky gradient, small silhouette of a person "
        "facing the sea, peaceful atmosphere, cinematic, photorealistic, 16:9",
        100
    ),
    "01-2_郑新出现": (
        "(masterpiece, best quality), medium shot, 30-year-old Chinese man, slim, "
        "tanned skin, messy short hair, standing on beach, turning to camera, warm relieved "
        "smile, sunset golden backlight, windblown hair, cinematic, warm tones",
        101
    ),
    "01-3_郑新释然一笑": (
        "(masterpiece, best quality), close-up, 30-year-old Chinese man, tanned skin, "
        "messy hair, relieved warm smile, eyes crinkling, beach background, golden hour, "
        "backlight creating rim light, windblown hair, cinematic portrait, emotional, warm tones",
        102
    ),
    "01-4_我认出他": (
        "(masterpiece, best quality), medium shot, two Chinese men, 30 years old, "
        "one with fair skin and short hair, one tanned with messy hair, on beach, "
        "friendly shoulder punch, sunset lighting, warm atmosphere, cinematic",
        103
    ),
    "01-5_对话蒙太奇": (
        "(masterpiece, best quality), close-up two shot, two Chinese men talking on beach, "
        "sunset golden hour, warm expressions, shallow depth of field, cinematic, warm tones, "
        "photorealistic",
        104
    ),
    # ---- Scene 2 石头上·落日 ----
    "02-1_岩石剪影": (
        "(masterpiece, best quality), wide shot, silhouette of two men sitting on seaside rock, "
        "facing setting sun, orange to purple-blue sky gradient, sea waves, sparkling water, "
        "peaceful melancholic atmosphere, cinematic lighting, 16:9",
        200
    ),
    "02-2_郑新侧脸": (
        "(masterpiece, best quality), close-up profile, 30-year-old Chinese man, tanned skin, "
        "messy hair, side view, sitting on rock, sunset glow on face, thoughtful expression, "
        "cinematic lighting, shallow depth of field, warm tones",
        201
    ),
    "02-3_闪回母亲车祸": (
        "(masterpiece, best quality), cinematic flashback, car accident scene, blurred edges, "
        "desaturated cool tones, broken glass, emergency lights, emotional, film grain, "
        "nostalgic filter, 16:9",
        202
    ),
    "02-4_高中郑新黯然": (
        "(masterpiece, best quality), portrait, teenage Chinese boy, sad eyes, school uniform, "
        "classroom background, dim lighting, melancholic atmosphere, nostalgic warm filter, "
        "cinematic, shallow depth of field",
        203
    ),
    # ---- Scene 3 回忆·高三·便利贴 ----
    "03-1_教室全景": (
        "(masterpiece, best quality), wide shot, high school classroom, teacher at podium, "
        "students at desks, warm fluorescent lighting, nostalgic atmosphere, cinematic, "
        "film grain, 16:9",
        300
    ),
    "03-2_便利贴特写": (
        "(masterpiece, best quality), close-up, colorful sticky notes on bulletin board, "
        "hand placing a note, focus on Chinese text \u6d41\u6d6a in black ink, classroom background "
        "blur, warm nostalgic filter, film grain, cinematic, shallow depth of field",
        301
    ),
    "03-3_回到现在": (
        "(masterpiece, best quality), medium shot, two Chinese men on beach at dusk, "
        "one looking at the other with questioning expression, warm evening light, "
        "cinematic, storytelling mood",
        302
    ),
    # ---- Scene 4 男儿志在四方 ----
    "04-1_男儿志在四方": (
        "(masterpiece, best quality), cinematic, Chinese man standing on rock, arms raised "
        "to sky, heroic mid-air pose, sunset backlight, dramatic silhouette, long shadow on "
        "rock, laughing expression, vast colorful sky, youthful energy, cinematic lighting",
        400
    ),
    "04-2_我的怅然": (
        "(masterpiece, best quality), close-up, Chinese man, fair skin, short hair, "
        "sitting on rock, watching, wistful expression, sunset glow, quiet moment, "
        "cinematic, emotional, warm tones",
        401
    ),
    # ---- Scene 5 夜幕降临·告别 ----
    "05-1_夜幕降临": (
        "(masterpiece, best quality), wide landscape, beach at twilight, sky transitioning "
        "from orange to deep blue, calm sea, peaceful atmosphere, cinematic, photorealistic, 16:9",
        500
    ),
    "05-2_交换联系方式": (
        "(masterpiece, best quality), medium shot, two men exchanging phones on beach at dusk, "
        "warm artificial light from phone screens, deep blue background, quiet farewell "
        "atmosphere, cinematic",
        501
    ),
    # ---- Scene 6 深夜·燥热 ----
    "06-1_辗转难眠": (
        "(masterpiece, best quality), interior night scene, bedroom, person lying in bed "
        "unable to sleep, phone screen glowing, warm dim lamplight, restless atmosphere, "
        "cinematic, intimate",
        600
    ),
    "06-2_手机特写": (
        "(masterpiece, best quality), close-up of phone screen, WeChat chat interface, "
        "Chinese text visible, blurred background of dark room, phone screen illuminating "
        "face slightly, cinematic, intimate night atmosphere",
        601
    ),
    # ---- Scene 7 公园·深夜咖啡 ----
    "07-1_深夜公园": (
        "(masterpiece, best quality), night scene, quiet park, warm lamplight, tree shadows, "
        "two men at small table with coffee, deep blue night tones, warm light accents, "
        "summer night atmosphere, peaceful, cinematic storytelling",
        700
    ),
    "07-2_聊天蒙太奇": (
        "(masterpiece, best quality), cinematic montage, two men talking at park cafe table "
        "at night, warm lamplight, coffee cups, expressive hand gestures, intimate "
        "conversation, filmic, warm night tones",
        701
    ),
    "07-3_咖啡杯特写": (
        "(masterpiece, best quality), close-up, two coffee cups on wooden table, warm "
        "lamplight, steam rising, blurred park background, quiet intimate moment, cinematic "
        "still life, warm tones",
        702
    ),
    # ---- Scene 8 浪漫主义流浪家 ----
    "08-1_浪漫主义流浪家": (
        "(masterpiece, best quality), cinematic, park at night, one man standing looking down "
        "at seated man, warm lamplight, gentle smile, sincere expression, quiet emotional "
        "moment, warm tones, shallow depth of field",
        800
    ),
    # ---- Scene 9 大理之约 ----
    "09-1_大理之约": (
        "(masterpiece, best quality), cinematic wide shot, two men under park lamppost saying "
        "goodbye, starry sky, path extending into distance, warm expectant atmosphere, "
        "night scene, cinematic colors",
        900
    ),
    # ---- Scene 10 次日清晨 ----
    "10-1_阳台日出": (
        "(masterpiece, best quality), wide shot, balcony view, sunrise over city, warm golden "
        "light, peaceful morning atmosphere, cinematic, photorealistic, 16:9",
        1000
    ),
    "10-2_手机消息": (
        "(masterpiece, best quality), close-up, hand holding phone, WeChat chat screen with "
        "Chinese text, background balcony morning light blur, cup of tea, warm soft lighting, "
        "quiet meaningful atmosphere, cinematic",
        1001
    ),
    # ---- Scene 11 尾声·天空 ----
    "11-1_天空意境": (
        "(masterpiece, best quality), wide shot, sky view from balcony, blue sky with soft "
        "clouds, warm gentle tones, clean composition, serene, cinematic closing shot, "
        "peaceful atmosphere",
        1100
    ),
}


# ═══════════════════════════════════════════
#  生成函数
# ═══════════════════════════════════════════

def generate_batch(prompts_dict, model_name="DreamShaperXL_Turbo_v2.safetensors",
                   width=1024, height=576, steps=6, cfg=2.0):
    """批量生成图片。"""
    results = []
    total = len(prompts_dict)

    for i, (name, (prompt, seed)) in enumerate(prompts_dict.items(), 1):
        print(f"\n[{i}/{total}] 生成: {name}")
        print(f"  Seed: {seed}")

        wf = build_workflow(
            model_name=model_name,
            positive_prompt=prompt,
            negative_prompt=NEGATIVE,
            width=width, height=height,
            steps=steps, cfg=cfg,
            seed=seed,
            filename_prefix=name,
        )

        try:
            image_paths = generate(wf)
            if image_paths:
                src = image_paths[0]
                dst = os.path.join(OUTPUT_DIR, f"{name}.png")
                shutil.copy2(src, dst)
                print(f"  -> 已保存: {dst}")
                results.append((name, dst))
            else:
                print(f"  -> 失败: 无返回图片")
                results.append((name, None))
        except Exception as exc:
            print(f"  -> 错误: {exc}")
            results.append((name, None))

        time.sleep(0.5)

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("AI漫剧《浪漫主义流浪家》— 全自动分镜生成管线")
    print("=" * 60)

    print("\n[1/3] 启动 ComfyUI...")
    if not start():
        print("致命错误: ComfyUI 启动失败")
        sys.exit(1)

    try:
        print("\n[2/3] 生成角色定妆照...")
        char_prompts = {k: v for k, v in PROMPTS.items() if k.startswith("00")}
        char_results = generate_batch(char_prompts)

        print("\n[3/3] 生成全部分镜...")
        shot_prompts = {k: v for k, v in PROMPTS.items() if not k.startswith("00")}
        shot_results = generate_batch(shot_prompts)

        success = sum(1 for _, p in char_results + shot_results if p)
        total = len(char_results) + len(shot_results)
        print(f"\n生成完成: {success}/{total} 成功")
        for name, path in char_results + shot_results:
            status = "OK" if path else "FAIL"
            print(f"  [{status}] {name}")

    finally:
        stop()
        print("\nComfyUI 已停止")
