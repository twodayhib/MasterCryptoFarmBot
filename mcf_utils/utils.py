# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

from datetime import datetime
from urllib.parse import urlparse
import requests
import re


def parseProxy(proxy_url):
    if not proxy_url or proxy_url is None or proxy_url == "":
        return None

    parsed = urlparse(proxy_url)

    if not parsed.hostname or not parsed.port:
        return None

    proxy_dict = {
        "scheme": "http",
        "hostname": parsed.hostname,
        "port": parsed.port,
    }

    if parsed.scheme:
        proxy_dict["scheme"] = parsed.scheme
    if parsed.username:
        proxy_dict["username"] = parsed.username
    if parsed.password:
        proxy_dict["password"] = parsed.password

    return proxy_dict


def getConfig(config, key, default=None):
    if key in config:
        return config[key]
    return default


def testProxy(proxy_url, retries=3):
    if not proxy_url:
        return True
    proxy_dict = {
        "http": proxy_url,
        "https": proxy_url,
    }
    for attempt in range(retries):
        try:
            resp = requests.get(
                "https://api.masterking32.com/ip.php?json=true",
                proxies=proxy_dict,
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json().get("ipAddress", False)
            return False
        except Exception as e:
            if attempt == retries - 1:
                return False


def HideIP(ip):
    if not ip:
        return None

    if ":" in ip:
        return ip[:6] + "****" + ip[-6:]
    parts = ip.split(".")
    return parts[0] + "." + parts[1] + ".***.***"


def RemoveConsoleColor(text):
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def ansi_to_html(text):
    ansi_to_html_map = {
        "\x1b[0m": "</span>",
        "\x1b[1m": '<span style="font-weight: bold;">',
        "\x1b[3m": '<span style="font-style: italic;">',
        "\x1b[4m": '<span style="text-decoration: underline;">',
        "\x1b[31m": '<span style="color: red;">',
        "\x1b[32m": '<span style="color: green;">',
        "\x1b[33m": '<span style="color: yellow;">',
        "\x1b[34m": '<span style="color: blue;">',
        "\x1b[35m": '<span style="color: magenta;">',
        "\x1b[36m": '<span style="color: cyan;">',
        "\x1b[37m": '<span style="color: white;">',
        "\n": "<br>",
        "\r": "",
        "<red>": '<span style="color: red;">',
        "<green>": '<span style="color: green;">',
        "<yellow>": '<span style="color: yellow;">',
        "<blue>": '<span style="color: blue;">',
        "<magenta>": '<span style="color: magenta;">',
        "<cyan>": '<span style="color: cyan;">',
        "<white>": '<span style="color: white;">',
        "</red>": "</span>",
        "</green>": "</span>",
        "</yellow>": "</span>",
        "</blue>": "</span>",
        "</magenta>": "</span>",
        "</cyan>": "</span>",
        "</white>": "</span>",
        "<r>": '<span style="color: red;">',
        "<g>": '<span style="color: green;">',
        "<y>": '<span style="color: yellow;">',
        "<b>": '<span style="color: blue;">',
        "<m>": '<span style="color: magenta;">',
        "<c>": '<span style="color: cyan;">',
        "<w>": '<span style="color: white;">',
        "</r>": "</span>",
        "</g>": "</span>",
        "</y>": "</span>",
        "</b>": "</span>",
        "</m>": "</span>",
        "</c>": "</span>",
        "</w>": "</span>",
    }

    for ansi_code, html_code in ansi_to_html_map.items():
        text = text.replace(ansi_code, html_code)

    lines = text.split("<br>")
    for i, line in enumerate(lines):
        open_tags = line.count("<span") - line.count("</span")
        if open_tags > 0:
            lines[i] += "</span>" * open_tags

    text = "<br>".join(lines)

    return text + "</span>"


def TimeAgo(time):
    if not time:
        return "Unknown"

    if isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    now = datetime.now()
    diff = (now - time).total_seconds()

    if diff < 60:
        return f"{int(diff)} seconds"
    if diff < 3600:
        return f"{int(diff // 60)} minutes"
    if diff < 86400:
        return f"{int(diff // 3600)} hours"
    return f"{int(diff // 86400)} days"


def hide_text(text, length=4):
    if not text:
        return None

    if len(text) <= length:
        return "*" * len(text)

    return text[:length] + "*" * (len(text) - length * 2) + text[-length:]