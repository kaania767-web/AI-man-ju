"""ComfyUI 工作流构建器 — 支持 txt2img + 可选 IP-Adapter 参考图。

用法:
    from workflow import build_workflow
    wf = build_workflow(model_name=..., positive_prompt=..., ...)
"""


def build_workflow(
    model_name="DreamShaperXL_Turbo_v2.safetensors",
    positive_prompt="",
    negative_prompt="",
    width=1024,
    height=576,
    steps=6,
    cfg=2.0,
    seed=42,
    sampler_name="dpmpp_2m",
    scheduler="karras",
    filename_prefix="comfy",
    ref_image_path=None,
    ipadapter_weight=0.6,
    ipadapter_preset="PLUS (high strength)",
    ipadapter_start=0.0,
    ipadapter_end=1.0,
    ipadapter_weight_type="standard",
):
    """Build a txt2img workflow JSON for the ComfyUI API.

    When *ref_image_path* is provided, the workflow chains an IP-Adapter
    reference node so the generated image follows the reference character's
    appearance.
    """
    import os

    workflow = {}
    nid = iter(range(1, 1000))

    def N():
        return str(next(nid))

    # Checkpoint
    ckpt = N()
    workflow[ckpt] = {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": model_name},
    }

    # Positive prompt
    pos = N()
    workflow[pos] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": positive_prompt, "clip": [ckpt, 1]},
    }

    # Negative prompt
    neg = N()
    workflow[neg] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": negative_prompt, "clip": [ckpt, 1]},
    }

    # Empty latent
    latent = N()
    workflow[latent] = {
        "class_type": "EmptyLatentImage",
        "inputs": {"width": width, "height": height, "batch_size": 1},
    }

    # Optional IP-Adapter reference
    if ref_image_path and os.path.exists(ref_image_path):
        load_img = N()
        workflow[load_img] = {
            "class_type": "LoadImage",
            "inputs": {"image": ref_image_path},
        }

        ipa_loader = N()
        workflow[ipa_loader] = {
            "class_type": "IPAdapterUnifiedLoader",
            "inputs": {"model": [ckpt, 0], "preset": ipadapter_preset},
        }

        ipa_apply = N()
        workflow[ipa_apply] = {
            "class_type": "IPAdapter",
            "inputs": {
                "model": [ipa_loader, 0],
                "ipadapter": [ipa_loader, 1],
                "image": [load_img, 0],
                "weight": ipadapter_weight,
                "start_at": ipadapter_start,
                "end_at": ipadapter_end,
                "weight_type": ipadapter_weight_type,
            },
        }
        model_ref = [ipa_apply, 0]
    else:
        model_ref = [ckpt, 0]

    # KSampler
    sampler = N()
    workflow[sampler] = {
        "class_type": "KSampler",
        "inputs": {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "denoise": 1.0,
            "model": model_ref,
            "positive": [pos, 0],
            "negative": [neg, 0],
            "latent_image": [latent, 0],
        },
    }

    # VAE Decode
    vae = N()
    workflow[vae] = {
        "class_type": "VAEDecode",
        "inputs": {"samples": [sampler, 0], "vae": [ckpt, 2]},
    }

    # Save Image
    save = N()
    workflow[save] = {
        "class_type": "SaveImage",
        "inputs": {"filename_prefix": filename_prefix, "images": [vae, 0]},
    }

    return workflow
