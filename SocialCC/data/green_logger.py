#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -------- Message Format -----------
import os, sys, logging, re

os.environ.setdefault("NO_COLOR", "1")

C_GREEN = "\033[32m"
C_RESET = "\033[0m"
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

class GreenFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        msg = ANSI_RE.sub('', msg)   
        return f"{C_GREEN}{msg}{C_RESET}"


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(GreenFormatter("%(message)s"))


root = logging.getLogger()
root.handlers.clear()
root.setLevel(logging.ERROR)


for name in ["autogen", "autogen.agentchat", "autogen.runtime_logging", "autogen.runtime", "autogen.logger"]:
    lg = logging.getLogger(name)
    lg.handlers.clear()
    lg.propagate = False        
    lg.setLevel(logging.INFO)  
    lg.addHandler(handler)


for noisy in ["httpx", "openai", "urllib3", "asyncio", "aiohttp"]:
    logging.getLogger(noisy).setLevel(logging.ERROR)

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)