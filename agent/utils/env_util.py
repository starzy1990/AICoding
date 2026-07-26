import os
from datetime import timedelta
from pathlib import Path
from typing import Optional

from opensandbox.config import ConnectionConfig
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)



def get_opensandbox_connection_config() -> Optional[ConnectionConfig]:
    domain = get_env_var("OPENSANDBOX_DOMAIN")
    api_key = get_env_var("OPENSANDBOX_API_KEY")

    if domain and api_key:
        return ConnectionConfig(domain=domain, api_key=api_key)

    return None


def get_opensandbox_image() -> str:
    return get_env_var(
        "OPENSANDBOX_IMAGE",
        "sandbox-registry.cn-zhangjiakou.cr.aliyuncs.com/opensandbox/code-interpreter:v1.0.2",
    )


def get_opensandbox_timeout() -> timedelta:
    timeout_seconds = get_env_var("OPENSANDBOX_TIMEOUT", "600")
    try:
        return timedelta(seconds=int(timeout_seconds))
    except ValueError:
        return timedelta(minutes=10)

