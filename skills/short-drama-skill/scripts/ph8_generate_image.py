#!/usr/bin/env python3
"""
普华 (ph8.co) OpenAI 兼容图像生成 — CLI，供 Agent / 本地脚本调用。

用途：角色设定图、分镜首帧/尾帧、风格参考图生图。

环境变量：
  PH8_API_KEY 或 OPENAI_API_KEY  — 必填
  OPENAI_BASE_URL                — 可选，默认 https://ph8.co/openai/v1

示例：
  python scripts/ph8_generate_image.py \\
    --prompt "短剧人设，25岁女性，职业装，半身，白底，电影光" \\
    --out assets/characters/heroine.png

  python scripts/ph8_generate_image.py \\
    --prompt "同一场景尾帧：女主转身离开，背影" \\
    --ref-uri "https://example.com/first.png" \\
    --out assets/frames/ep001/end.png
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any

from ph8_common import require_api_key


def _default_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://ph8.co/openai/v1")


def _mime_from_uri(uri: str) -> str:
    path_part = uri.split("?", 1)[0].lower()
    if path_part.endswith(".png"):
        return "image/png"
    if path_part.endswith(".webp"):
        return "image/webp"
    if path_part.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    return "image/jpeg"


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


def _build_reference_images(
    ref_uris: list[str],
    ref_files: list[Path],
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for u in ref_uris:
        u = u.strip()
        if not u:
            continue
        # 默认按 URL 推断 jpeg；无法推断时 jpeg 多数服务可接受
        refs.append({"file_uri": u, "mime_type": _mime_from_uri(u)})
    for p in ref_files:
        if not p.is_file():
            print(f"错误：参考图文件不存在 — {p}", file=sys.stderr)
            sys.exit(1)
        raw = p.read_bytes()
        b64 = base64.standard_b64encode(raw).decode("ascii")
        refs.append({"data": b64, "mime_type": _guess_mime(p)})
    return refs


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="调用 ph8 OpenAI 兼容接口生成图像（角色 / 首尾帧）",
    )
    p.add_argument("--prompt", required=True, help="图像描述提示词")
    p.add_argument(
        "--out",
        type=Path,
        help="保存路径（.png/.jpg）。多张图时自动加序号：name-1.png",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("PH8_IMAGE_MODEL", "Nano-Banana-Pro2"),
        help="模型名，默认 Nano-Banana-Pro2，可用环境变量 PH8_IMAGE_MODEL",
    )
    p.add_argument("--size", default="1024x1024", help='尺寸，如 1024x1024、16:9 等')
    p.add_argument("--n", type=int, default=1, help="生成张数，默认 1")
    p.add_argument(
        "--response-format",
        choices=("b64_json", "url"),
        default="b64_json",
        help="返回格式",
    )
    p.add_argument(
        "--ref-uri",
        action="append",
        default=[],
        help="参考图 URL，可重复传入多次",
    )
    p.add_argument(
        "--ref-file",
        type=Path,
        action="append",
        default=[],
        help="本地参考图路径，可重复传入多次",
    )
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top-p", type=float, default=0.95, dest="top_p")
    p.add_argument(
        "--output-mime-type",
        default="image/png",
        dest="output_mime_type",
        help="生成图 MIME，如 image/png / image/jpeg",
    )
    p.add_argument(
        "--json-meta",
        action="store_true",
        help="成功时在 stdout 打印一行 JSON（便于 Agent 解析）",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    api_key = require_api_key(tool_name="图像生成")
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：请先安装依赖：pip install -r scripts/requirements.txt", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(base_url=_default_base_url(), api_key=api_key)

    extra_body: dict[str, Any] = {
        "temperature": args.temperature,
        "top_p": args.top_p,
        "output_mime_type": args.output_mime_type,
    }
    refs = _build_reference_images(list(args.ref_uri), list(args.ref_file))
    if refs:
        extra_body["reference_images"] = refs

    result = client.images.generate(
        model=args.model,
        prompt=args.prompt,
        size=args.size,
        n=args.n,
        response_format=args.response_format,
        extra_body=extra_body,
    )

    saved: list[str] = []
    if args.response_format == "b64_json":
        if not args.out:
            print("错误：b64_json 模式下必须指定 --out", file=sys.stderr)
            sys.exit(1)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        stem = args.out.stem
        suffix = args.out.suffix or ".png"
        for i, item in enumerate(result.data):
            b64 = item.b64_json
            if not b64:
                print(f"错误：第 {i+1} 张未返回 b64_json", file=sys.stderr)
                sys.exit(1)
            raw = base64.b64decode(b64)
            if args.n == 1:
                path = args.out
            else:
                path = args.out.with_name(f"{stem}-{i + 1}{suffix}")
            path.write_bytes(raw)
            saved.append(str(path.resolve()))
    else:
        # url
        for i, item in enumerate(result.data):
            url = getattr(item, "url", None)
            if not url:
                print(f"错误：第 {i+1} 张未返回 url", file=sys.stderr)
                sys.exit(1)
            if args.out:
                print(
                    "提示：response_format=url 时未自动下载，请自行拉取 URL：",
                    url,
                    file=sys.stderr,
                )
            saved.append(url)

    if args.json_meta:
        line = json.dumps({"ok": True, "paths": saved, "n": len(saved)}, ensure_ascii=False)
        print(line)
    elif saved and args.out and args.response_format == "b64_json":
        for s in saved:
            print(s)

    sys.exit(0)


if __name__ == "__main__":
    main()
