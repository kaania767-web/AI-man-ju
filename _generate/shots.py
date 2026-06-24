SHOTS = [
    # ========== 封面 ==========
    {
        "id": "cover",
        "image": "01-1_落日海面全景.png",
        "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.08, "pan_x": 0, "pan_y": -20},
        "texts": [
            {"type": "title", "text": "浪漫主义流浪家", "start": 1.0, "end": 4.5, "font_size": 72},
            {"type": "subtitle", "text": "一个关于相遇与告别的故事", "start": 2.0, "end": 4.5, "font_size": 32},
        ],
        "fade_in": 0.8,
    },
    # ========== 序幕 ==========
    {
        "id": "prologue",
        "image": "01-1_落日海面全景.png",
        "duration": 8.0,
        "ken_burns": {"zoom_start": 1.08, "zoom_end": 1.15, "pan_x": 0, "pan_y": -40},
        "texts": [
            {"type": "narration", "text": "那是我在平潭的最后一个傍晚。\n海风咸涩，落日熔金。我以为这不过是又一个安静的黄昏。",
             "start": 0.5, "end": 7.5, "font_size": 34},
        ],
    },
    # ========== Scene 1 ==========
    {
        "id": "01-1", "image": "01-1_落日海面全景.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 30, "pan_y": 0},
        "scene_label": "SCENE 01  海边·再会",
        "texts": [
            {"type": "dialogue", "text": "认识郑新那年，也是这样的夏天。",
             "speaker": "VO · 我", "start": 0.5, "end": 5.5},
        ],
    },
    {
        "id": "01-2", "image": "01-2_郑新出现.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 10},
        "texts": [
            {"type": "dialogue", "text": "嗨，好久不见。", "speaker": "郑新", "start": 0.5, "end": 4.5},
        ],
    },
    {
        "id": "01-3", "image": "01-3_郑新释然一笑.png", "duration": 8.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.08, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue",
             "text": "你知道吗，我在大理住过一个房间，\n只有空调外机没有空调内机。\n老板说——「意境到了就行」。",
             "speaker": "郑新", "start": 0.5, "end": 7.5},
        ],
    },
    {
        "id": "01-4", "image": "01-4_我认出他.png", "duration": 4.0,
        "ken_burns": {"zoom_start": 1.02, "zoom_end": 1.06, "pan_x": -10, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "你还是老样子。", "speaker": "我", "start": 0.5, "end": 3.5},
        ],
    },
    {
        "id": "01-5", "image": "01-5_对话蒙太奇.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.04, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "这些年跑哪去了？", "speaker": "我", "start": 0.5, "end": 2.5},
            {"type": "dialogue", "text": "瞎跑呗。新疆、西藏、大理……活着。", "speaker": "郑新", "start": 2.8, "end": 5.5},
            {"type": "dialogue", "text": "跟高中同学都没联系了？", "speaker": "我", "start": 5.8, "end": 7.5},
            {"type": "dialogue", "text": "嗯。你是我这几年遇到的第一个熟人。", "speaker": "郑新", "start": 7.8, "end": 9.5},
        ],
    },
    # ========== Scene 2 ==========
    {
        "id": "02-1", "image": "02-1_岩石剪影.png", "duration": 8.0,
        "ken_burns": {"zoom_start": 1.02, "zoom_end": 1.12, "pan_x": 20, "pan_y": -10},
        "scene_label": "SCENE 02  石上·落日",
        "texts": [
            {"type": "dialogue", "text": "我爸走的那天，我在新疆，信号都没有。\n等我知道，已经是一周后了。",
             "speaker": "VO · 郑新", "start": 1.0, "end": 7.5},
        ],
    },
    {
        "id": "02-2", "image": "02-2_郑新侧脸.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": -15, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "算一算，十多年没回过家了。", "speaker": "郑新", "start": 0.5, "end": 5.5},
        ],
    },
    {
        "id": "02-3", "image": "02-3_闪回母亲车祸.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "narration", "text": "高中那年，他母亲在接他放学的路上出了车祸。\n从那以后，郑新变了。",
             "start": 0.5, "end": 5.5},
        ],
    },
    {
        "id": "02-4", "image": "02-4_高中郑新黯然.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.02, "zoom_end": 1.08, "pan_x": 0, "pan_y": 0},
    },
    # ========== Scene 3 ==========
    {
        "id": "03-1", "image": "03-1_教室全景.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 10},
        "scene_label": "SCENE 03  回憶·高三·便利貼",
        "texts": [
            {"type": "narration", "text": "高三那年，老师让大家在便利贴上写自己的理想。", "start": 0.5, "end": 4.5},
        ],
    },
    {
        "id": "03-2", "image": "03-2_便利贴特写.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 0},
    },
    {
        "id": "03-3", "image": "03-3_回到现在.png", "duration": 7.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "你还记不记得你写的什么？", "speaker": "我", "start": 0.5, "end": 2.5},
            {"type": "dialogue", "text": "记得。\n我说我要去流浪。", "speaker": "郑新", "start": 3.0, "end": 6.5},
        ],
    },
    # ========== Scene 4 ==========
    {
        "id": "04-1", "image": "04-1_男儿志在四方.png", "duration": 7.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.08, "pan_x": 0, "pan_y": -15},
        "scene_label": "SCENE 04  男儿志在四方",
        "texts": [
            {"type": "dialogue", "text": "我可是要征服世界的男人！", "speaker": "郑新", "start": 0.5, "end": 6.5},
        ],
    },
    {
        "id": "04-2", "image": "04-2_我的怅然.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "narration", "text": "（看着他，忽然有点羡慕）", "start": 0.5, "end": 4.5},
        ],
    },
    # ========== Scene 5 ==========
    {
        "id": "05-1", "image": "05-1_夜幕降临.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 0},
        "scene_label": "SCENE 05  夜幕降临·告别",
    },
    {
        "id": "05-2", "image": "05-2_交换联系方式.png", "duration": 7.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "加个微信？", "speaker": "郑新", "start": 0.5, "end": 2.5},
            {"type": "dialogue", "text": "好。", "speaker": "我", "start": 3.0, "end": 4.5},
        ],
    },
    # ========== Scene 6 ==========
    {
        "id": "06-1", "image": "06-1_辗转难眠.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.04, "pan_x": 0, "pan_y": 0},
        "scene_label": "SCENE 06  深夜·燥热",
    },
    {
        "id": "06-2", "image": "06-2_手机特写.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "睡了吗？\n出来喝杯咖啡。", "speaker": "郑新", "start": 0.5, "end": 5.5},
        ],
    },
    {
        "id": "06-narration", "image": "06-1_辗转难眠.png", "duration": 5.0,
        "ken_burns": {"zoom_start": 1.04, "zoom_end": 1.08, "pan_x": -10, "pan_y": 0},
        "texts": [
            {"type": "narration", "text": "于是凌晨一点，我在民宿门口见到了拎着两杯咖啡的他。", "start": 0.5, "end": 4.5},
        ],
    },
    # ========== Scene 7 ==========
    {
        "id": "07-1", "image": "07-1_深夜公园.png", "duration": 8.0,
        "ken_burns": {"zoom_start": 1.02, "zoom_end": 1.1, "pan_x": -20, "pan_y": 0},
        "scene_label": "SCENE 07  公園·深夜咖啡",
        "texts": [
            {"type": "narration", "text": "蝉声如潮，路灯昏黄。\n这座岛上醒着的，大概只剩我们了。",
             "start": 1.0, "end": 7.5},
        ],
    },
    {
        "id": "07-2", "image": "07-2_聊天蒙太奇.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.05, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "你去过那么多地方，最喜欢哪里？", "speaker": "我", "start": 0.5, "end": 2.8},
            {"type": "dialogue", "text": "大理吧。在那里我住得最久。\n白天在古城闲逛，晚上去山上躺着看星星。", "speaker": "郑新", "start": 3.0, "end": 6.5},
            {"type": "dialogue", "text": "不孤独吗？", "speaker": "我", "start": 6.8, "end": 8.0},
            {"type": "dialogue", "text": "孤独啊。但孤独和自由是一回事的两面。", "speaker": "郑新", "start": 8.2, "end": 9.5},
        ],
    },
    {
        "id": "07-3", "image": "07-3_咖啡杯特写.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "narration", "text": "咖啡已经凉了，但谁也没说要走。", "start": 0.5, "end": 5.5},
        ],
    },
    # ========== Scene 8 ==========
    {
        "id": "08-1", "image": "08-1_浪漫主义流浪家.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": 0},
        "scene_label": "SCENE 08  浪漫主义流浪家",
        "texts": [
            {"type": "dialogue", "text": "你知道吗，我觉得你不是在流浪。", "speaker": "我", "start": 0.5, "end": 2.5},
            {"type": "dialogue", "text": "你是一个浪漫主义流浪家。\n——你流浪，是因为你把世界过成了诗。", "speaker": "我", "start": 3.0, "end": 7.0},
            {"type": "narration", "text": "郑新愣了两秒，然后笑了起来，笑得眼睛都眯成了一条缝。", "start": 7.5, "end": 9.5},
        ],
    },
    # ========== Scene 9 ==========
    {
        "id": "09-1", "image": "09-1_大理之约.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.08, "pan_x": 10, "pan_y": 0},
        "scene_label": "SCENE 09  大理之约",
        "texts": [
            {"type": "dialogue", "text": "等我安顿下来，你来大理找我。\n三年后吧——不见不散。", "speaker": "郑新", "start": 0.5, "end": 6.5},
            {"type": "dialogue", "text": "不见不散。", "speaker": "我", "start": 7.0, "end": 9.0},
        ],
    },
    # ========== Scene 10 ==========
    {
        "id": "10-1", "image": "10-1_阳台日出.png", "duration": 6.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0, "pan_y": -10},
        "scene_label": "SCENE 10  次日清晨",
    },
    {
        "id": "10-2", "image": "10-2_手机消息.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.04, "pan_x": 0, "pan_y": 0},
        "texts": [
            {"type": "dialogue", "text": "我到家了，你也早点休息。", "speaker": "郑新", "start": 0.5, "end": 2.5},
            {"type": "dialogue", "text": "有时候往天上一看，和17岁的没区别。\n于是一直看着天，不看这个世界。", "speaker": "郑新", "start": 3.0, "end": 9.5},
        ],
    },
    # ========== Scene 11 ==========
    {
        "id": "11-1", "image": "11-1_天空意境.png", "duration": 10.0,
        "ken_burns": {"zoom_start": 1.0, "zoom_end": 1.1, "pan_x": 0, "pan_y": -15},
        "scene_label": "SCENE 11  尾声·天空",
        "texts": [
            {"type": "narration", "text": "我放下手机，看向窗外。\n天亮了。云在走。\n和十七岁那年看到的，确实没什么区别。",
             "start": 0.5, "end": 8.0},
        ],
    },
    # ========== 片尾 ==========
    {
        "id": "ending", "image": "11-1_天空意境.png", "duration": 8.0,
        "ken_burns": {"zoom_start": 1.1, "zoom_end": 1.15, "pan_x": 0, "pan_y": -30},
        "texts": [
            {"type": "title", "text": "浪漫主义流浪家", "start": 1.0, "end": 7.0, "font_size": 60},
            {"type": "credit", "text": "原作 / 剧本 · 唐文浚\nAI 绘图 · ComfyUI + DreamShaperXL", "start": 3.0, "end": 7.5, "font_size": 28},
        ],
        "fade_in": 0.5,
    },
]
