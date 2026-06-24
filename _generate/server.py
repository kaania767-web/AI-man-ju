"""ComfyUI 后端服务管理 — 启动/停止/API 交互封装。

用法:
    from server import start, stop, generate
    start()
    try:
        images = generate(workflow_json)
    finally:
        stop()
"""

import atexit
import http.client
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

COMFYUI_DIR = r"C:\ComfyUI"
COMFYUI_URL = "http://127.0.0.1:8188"
START_TIMEOUT = 120
GENERATE_TIMEOUT = 600
WARMUP_DELAY = 0.5

_server_proc = None


def start() -> bool:
    """启动 ComfyUI 服务，等待就绪后返回。

    Returns:
        True 表示服务已就绪，False 表示启动失败。
    """
    global _server_proc

    if _server_proc and _server_proc.poll() is None:
        print(f"ComfyUI 已在运行 (PID={_server_proc.pid})")
        return True

    env = os.environ.copy()
    env["PYTHONPATH"] = COMFYUI_DIR + os.pathsep + env.get("PYTHONPATH", "")

    _server_proc = subprocess.Popen(
        [sys.executable, "-u", "main.py", "--force-fp16", "--highvram", "--listen", "127.0.0.1"],
        cwd=COMFYUI_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for attempt in range(START_TIMEOUT):
        try:
            resp = urllib.request.urlopen(f"{COMFYUI_URL}/object_info", timeout=2)
            if resp.status == 200:
                print(f"ComfyUI 就绪 (PID={_server_proc.pid})")
                return True
        except (urllib.error.URLError, ConnectionResetError, OSError):
            pass

        if attempt > 0 and attempt % 10 == 0:
            print(f"  等待 ComfyUI 启动... ({attempt}s)")
        time.sleep(1)

    print(f"错误: ComfyUI 在 {START_TIMEOUT}s 内未启动")
    return False


def stop() -> None:
    """停止 ComfyUI 服务。"""
    global _server_proc
    if _server_proc and _server_proc.poll() is None:
        _server_proc.terminate()
        try:
            _server_proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            _server_proc.kill()
            _server_proc.wait(timeout=5)
        _server_proc = None
        print("ComfyUI 已停止")


atexit.register(stop)


def _queue_prompt(workflow_json: dict) -> str:
    """提交工作流，返回 prompt_id。"""
    body = json.dumps({"prompt": workflow_json}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"响应中没有 prompt_id: {result}")
    return prompt_id


def _wait_for_image(prompt_id: str, timeout: int = GENERATE_TIMEOUT) -> list[str]:
    """等待生成完成，返回输出图片路径列表。"""
    output_dir = pathlib.Path(COMFYUI_DIR) / "output"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            conn = http.client.HTTPConnection("127.0.0.1", 8188, timeout=30)
            conn.request("GET", f"/history/{prompt_id}")
            resp = conn.getresponse()
            data = json.loads(resp.read())
            conn.close()

            if prompt_id not in data:
                time.sleep(1)
                continue

            images: list[str] = []
            for node_out in data[prompt_id].get("outputs", {}).values():
                for imgs in node_out.values():
                    if not isinstance(imgs, list):
                        continue
                    for img in imgs:
                        if isinstance(img, dict) and "filename" in img:
                            img_path = output_dir / img["filename"]
                            if img_path.exists():
                                images.append(str(img_path))
            if images:
                return images
        except (ConnectionRefusedError, http.client.RemoteDisconnected, OSError):
            pass
        finally:
            if time.time() + 0.1 < deadline:
                time.sleep(WARMUP_DELAY)

    raise TimeoutError(f"生成超时 ({timeout}s)")


def generate(workflow_json: dict, timeout: int = GENERATE_TIMEOUT) -> list[str]:
    """完整管线：提交工作流 → 等待完成 → 返回图片路径。"""
    prompt_id = _queue_prompt(workflow_json)
    print(f"  已提交: {prompt_id[:8]}...")
    images = _wait_for_image(prompt_id, timeout)
    print(f"  完成: {len(images)} 张图片")
    return images


if __name__ == "__main__":
    if start():
        print("服务运行中，按 Ctrl+C 停止")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            stop()
