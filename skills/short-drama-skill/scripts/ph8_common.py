"""
普华 ph8 CLI 共用逻辑：可选加载项目根目录 .env、校验 API Key。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_repo_env() -> None:
    """
    从项目根目录读取 .env（若存在），不覆盖已在环境中的变量。
    无需安装 python-dotenv。
    """
    env_path = repo_root() / ".env"
    if not env_path.is_file():
        return
    try:
        text = env_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if "=" not in raw:
            continue
        key, _, value = raw.partition("=")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def print_missing_api_key_help(*, tool_name: str = "生图 / 生视频") -> None:
    root = repo_root()
    print(
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️  未配置 API 密钥，无法调用普华 ph8 接口（"
        + tool_name
        + "）\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "请按任选一种方式配置密钥后再试：\n"
        "\n"
        "  【推荐】在项目根目录创建 .env 文件：\n"
        f"      cp {root / '.env.example'} {root / '.env'}\n"
        "      编辑 .env，填写： PH8_API_KEY=你的密钥\n"
        "\n"
        "  【或】当前终端临时导出（关闭终端后失效）：\n"
        "      export PH8_API_KEY='你的密钥'\n"
        "\n"
        "  也支持使用环境变量 OPENAI_API_KEY（与部分工具链兼容）。\n"
        "  可选：OPENAI_BASE_URL（默认 https://ph8.co/openai/v1）\n"
        "\n"
        "说明：不要将密钥写入剧本、Markdown 或提交到 Git（.env 已在 .gitignore）。\n",
        file=sys.stderr,
    )


def require_api_key(*, tool_name: str = "生图 / 生视频") -> str:
    load_repo_env()
    key = os.environ.get("PH8_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key or not str(key).strip():
        print_missing_api_key_help(tool_name=tool_name)
        sys.exit(1)
    return str(key).strip()
