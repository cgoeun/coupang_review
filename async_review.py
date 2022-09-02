import asyncio
import json
import lxml.html
from datetime import datetime, timedelta
import itertools
import aiohttp

GET_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36"
}

class API:
    

