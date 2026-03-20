#!/usr/bin/env python3
"""
普华 (ph8.co) OpenAI 兼容视频生成 — CLI，供 Agent / 本地脚本调用。

支持：文生视频、图生视频（简化 extra_body）、高级透传（首帧 / 尾帧 / 参考图）。

环境变量：
  PH8_API_KEY 或 OPENAI_API_KEY  — 必填
  OPENAI_BASE_URL                — 可选，默认 https://ph8.co/openai/v1
  PH8_VIDEO_MODEL                — 可选，覆盖默认模型

示例（文生视频·简化）：
  python scripts/ph8_generate_video.py \\
    --prompt "短剧镜头：女主角推门进入办公室，逆光" \\
    --out assets/video/ep001.mp4 --json-meta

示例（图生视频·简化，首帧为 URL）：
  python scripts/ph8_generate_video.py --mode simple \\
    --prompt "镜头缓慢推进" --image-url "https://..." \\
    --duration 5 --ratio "9:16" --out assets/video/clip.mp4 --json-meta

示例（首帧 + 尾帧·高级）：
  python scripts/ph8_generate_video.py --mode advanced \\
    --prompt "同一角色从坐姿站起，走向门口" \\
    --first-frame-url "https://.../start.png" \\
    --last-frame-url "https://.../end.png" \\
    --duration 5 --ratio "9:16" --seed 42 \\
    --out assets/video/ep001_transition.mp4 --json-meta
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

from ph8_common import require_api_key


def _default_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://ph8.co/openai/v1")


def _guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime:
        return mime
    suf = path.suffix.lower()
    if suf in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suf == ".webp":
        return "image/webp"
    return "image/png"


def _file_to_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    mime = _guess_mime(path)
    b64 = base64.standard_b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _url_to_data_uri(url: str) -> str:
    """下载 URL 为 data URI（简化模式部分服务只接受 base64）。"""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ph8_generate_video.py/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
        hdr = resp.headers.get("Content-Type", "image/png") or "image/png"
    mime = hdr.split(";", 1)[0].strip().lower()
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        mime = "image/png"
    b64 = base64.standard_b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _resolve_simple_image(
    image_url: str | None,
    image_file: Path | None,
    image_as_data_uri: bool,
) -> str | None:
    if image_url and image_file:
        print("错误：--image-url 与 --image-file 不能同时指定", file=sys.stderr)
        sys.exit(1)
    if image_file:
        if not image_file.is_file():
            print(f"错误：图片文件不存在 — {image_file}", file=sys.stderr)
            sys.exit(1)
        return _file_to_data_uri(image_file)
    if image_url:
        u = image_url.strip()
        if u.startswith("http://") or u.startswith("https://"):
            if image_as_data_uri:
                return _url_to_data_uri(u)
            return u
        print("错误：--image-url 必须是 http(s) URL", file=sys.stderr)
        sys.exit(1)
    return None


def _build_advanced_content_text(
    prompt: str,
    ratio: str | None,
    duration: int | None,
    seed: int | None,
    advanced_text: str | None,
) -> str:
    if advanced_text:
        return advanced_text
    parts = [prompt.strip()]
    if ratio:
        parts.append(f"--ratio {ratio}")
    if duration is not None:
        parts.append(f"--duration {duration}")
    if seed is not None:
        parts.append(f"--seed {seed}")
    return " ".join(parts)


def _poll_video(
    client: Any,
    video_id: str,
    *,
    poll_interval: float,
    show_progress: bool,
) -> Any:
    bar_length = 30
    while True:
        video = client.videos.retrieve(video_id)
        if video.status not in ("in_progress", "queued"):
            break
        progress = float(getattr(video, "progress", 0) or 0)
        if show_progress:
            filled = int((progress / 100.0) * bar_length)
            bar = "=" * filled + "-" * (bar_length - filled)
            status_text = "Queued" if video.status == "queued" else "Processing"
            sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
            sys.stdout.flush()
        time.sleep(poll_interval)
    if show_progress:
        sys.stdout.write("\n")
    return video


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="调用 ph8 OpenAI 兼容接口生成视频（文生 / 图生 / 首尾帧）",
    )
    p.add_argument("--prompt", required=True, help="视频内容描述（主提示词）")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("video.mp4"),
        help="输出 .mp4 路径，默认 video.mp4",
    )
    p.add_argument(
        "--model",
        default=os.environ.get(
            "PH8_VIDEO_MODEL",
            "doubao-seedance-1-5-pro-251215",
        ),
        help="视频模型名，可用 PH8_VIDEO_MODEL",
    )
    p.add_argument(
        "--mode",
        choices=("simple", "advanced"),
        default="simple",
        help="simple=扁平 extra_body；advanced=content 透传（支持首/尾帧）",
    )
    # simple i2v
    p.add_argument("--image-url", dest="image_url", default=None, help="图生视频：图片 URL")
    p.add_argument("--image-file", type=Path, default=None, help="图生视频：本地图片路径")
    p.add_argument(
        "--image-as-data-uri",
        action="store_true",
        help="简化模式下将 image-url 先下载并转为 data:...;base64,...",
    )
    p.add_argument("--duration", type=int, default=5, help="时长（秒），简化模式常用 4-12")
    p.add_argument("--resolution", default="1080p", help="720p / 1080p")
    p.add_argument(
        "--ratio",
        default="16:9",
        help='画幅，如 16:9, 9:16, 1:1, adaptive',
    )
    p.add_argument(
        "--camerafixed",
        action="store_true",
        help="简化模式：镜头固定（True=静态）",
    )
    p.add_argument("--seed", type=int, default=None, help="随机种子（可选）")
    p.add_argument("--watermark", action="store_true", help="是否加水印")
    # advanced
    p.add_argument(
        "--advanced-text",
        default=None,
        help="高级模式：content 里第一条 text 的完整字符串（若省略则由 prompt+ratio+duration+seed 拼装）",
    )
    p.add_argument("--first-frame-url", action="append", default=[], dest="first_frame_urls")
    p.add_argument("--last-frame-url", action="append", default=[], dest="last_frame_urls")
    p.add_argument(
        "--reference-image-url",
        action="append",
        default=[],
        dest="reference_image_urls",
    )
    p.add_argument("--service-tier", default="default", dest="service_tier")
    p.add_argument(
        "--generate-audio",
        action="store_true",
        dest="generate_audio",
        help="高级模式：是否生成音频",
    )
    p.add_argument(
        "--no-return-last-frame",
        action="store_true",
        dest="no_return_last_frame",
        help="高级模式：关闭 return_last_frame（默认开启）",
    )
    p.add_argument(
        "--execution-expires-after",
        type=int,
        default=3600,
        dest="execution_expires_after",
    )
    # run
    p.add_argument("--poll-interval", type=float, default=2.0, dest="poll_interval")
    p.add_argument(
        "--download-wait",
        type=float,
        default=10.0,
        dest="download_wait",
        help="完成后等待秒数再下载（部分任务需短暂就绪）",
    )
    p.add_argument("--no-progress", action="store_true", help="不打印进度条")
    p.add_argument(
        "--json-meta",
        action="store_true",
        help="成功时在 stdout 打印一行 JSON",
    )
    return p.parse_args()


def _validate_advanced(args: argparse.Namespace) -> None:
    if args.first_frame_urls and len(args.first_frame_urls) > 1:
        print("错误：当前仅支持 1 个 --first-frame-url", file=sys.stderr)
        sys.exit(1)
    if args.last_frame_urls and len(args.last_frame_urls) > 1:
        print("错误：当前仅支持 1 个 --last-frame-url", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = _parse_args()
    if args.mode == "advanced":
        _validate_advanced(args)

    api_key = require_api_key(tool_name="视频生成")
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：请先安装依赖：pip install -r scripts/requirements.txt", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(base_url=_default_base_url(), api_key=api_key)
    show_progress = not args.no_progress

    if args.mode == "simple":
        extra_body: dict[str, Any] = {
            "duration": args.duration,
            "resolution": args.resolution,
            "ratio": args.ratio,
            "camerafixed": args.camerafixed,
            "watermark": args.watermark,
        }
        if args.seed is not None:
            extra_body["seed"] = args.seed
        img = _resolve_simple_image(
            args.image_url,
            args.image_file,
            args.image_as_data_uri,
        )
        if img:
            extra_body["image"] = img
        video = client.videos.create(
            model=args.model,
            prompt=args.prompt,
            extra_body=extra_body,
        )
    else:
        content: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": _build_advanced_content_text(
                    args.prompt,
                    args.ratio,
                    args.duration,
                    args.seed,
                    args.advanced_text,
                ),
            }
        ]
        for u in args.first_frame_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": u.strip()},
                    "role": "first_frame",
                }
            )
        for u in args.last_frame_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": u.strip()},
                    "role": "last_frame",
                }
            )
        for u in args.reference_image_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": u.strip()},
                    "role": "reference_image",
                }
            )
        extra_body = {
            "content": content,
            "resolution": args.resolution,
            "service_tier": args.service_tier,
            "generate_audio": args.generate_audio,
            "return_last_frame": not args.no_return_last_frame,
            "execution_expires_after": args.execution_expires_after,
            "watermark": args.watermark,
        }
        video = client.videos.create(
            model=args.model,
            prompt=args.prompt,
            extra_body=extra_body,
        )

    vid = getattr(video, "id", None)
    if not vid:
        print(f"错误：创建任务失败，响应无 id：{video!r}", file=sys.stderr)
        sys.exit(1)

    if show_progress:
        print(f"Video task started: id={vid}", file=sys.stderr)

    video = _poll_video(client, vid, poll_interval=args.poll_interval, show_progress=show_progress)

    if video.status == "failed":
        err = getattr(video, "error", None)
        msg = getattr(err, "message", None) if err else None
        print(msg or "视频生成失败", file=sys.stderr)
        sys.exit(1)

    if show_progress:
        print("Downloading video content...", file=sys.stderr)
    time.sleep(max(0.0, args.download_wait))

    content_obj = client.videos.download_content(video.id, variant="video")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    content_obj.write_to_file(str(args.out))
    out_path = str(args.out.resolve())

    if args.json_meta:
        line = json.dumps(
            {
                "ok": True,
                "video_id": video.id,
                "path": out_path,
                "status": getattr(video, "status", None),
            },
            ensure_ascii=False,
        )
        print(line)
    elif show_progress:
        print(out_path)

    sys.exit(0)


if __name__ == "__main__":
    main()
