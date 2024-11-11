import nest_asyncio
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from urllib.parse import unquote
from bot.logger import Logger
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
import asyncio

logger = Logger()




class Tapper:
    def __init__(self, tg_client: Client, logger: Logger):
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.logger = logger

    async def get_tg_web_data(self, proxy: str | None) -> str:
        # This is my referral id to join with if you don't have an account
        # This is the least way to support me
        # If you don't you can change it to yours or leave it blank
        ref_ = 'https://t.me/seed_coin_bot/app?startapp=1306499778'
        try:
            ref__ = ref_.split('=')[1]
        except IndexError:
            ref__ = "1306499778"

        actual = ref__

        # Set up proxy if provided
        if proxy:
            proxy_dict = {'scheme': 'http', 'hostname': proxy, 'port': 8080}
            self.tg_client.proxy = proxy_dict
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            # Connect the client only if not already connected
            if not self.tg_client.is_connected:
                await self.tg_client.connect()

            peer = await self.tg_client.resolve_peer('seed_coin_bot')

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=actual
            ))

            auth_url = web_view.url
            tg_web_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            return tg_web_data

        except Exception as e:
            logger.error({self.session_name}, f"Error fetching web data: {e}")
            return ''
