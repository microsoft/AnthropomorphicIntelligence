#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -------- Message Format -----------
import os, sys, logging, re

# 禁掉三方库自带上色
os.environ.setdefault("NO_COLOR", "1")

C_GREEN = "\033[32m"
C_RESET = "\033[0m"
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

class GreenFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        msg = ANSI_RE.sub('', msg)  # 去掉任何已有颜色
        return f"{C_GREEN}{msg}{C_RESET}"

# 仅给 autogen.* 配置 handler；root 静音
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(GreenFormatter("%(message)s"))

# 先把 root 调到 ERROR，避免其它库噪音
root = logging.getLogger()
root.handlers.clear()
root.setLevel(logging.ERROR)

# 限定只拦 autogen 的日志命名空间
for name in ["autogen", "autogen.agentchat", "autogen.runtime_logging", "autogen.runtime", "autogen.logger"]:
    lg = logging.getLogger(name)
    lg.handlers.clear()
    lg.propagate = False       # 防止冒泡到 root 造成重复
    lg.setLevel(logging.INFO)  # 只要 INFO 以上
    lg.addHandler(handler)

# 显式压低常见第三方库的噪音（可选）
for noisy in ["httpx", "openai", "urllib3", "asyncio", "aiohttp"]:
    logging.getLogger(noisy).setLevel(logging.ERROR)

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)