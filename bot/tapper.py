import nest_asyncio
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from urllib.parse import unquote
from bot.logger import Logger


logger = Logger()




class Tapper:
    def __init__(self, tg_client: Client, logger: Logger):
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.logger = logger

    async def get_tg_web_data(self, proxy: str | None) -> str:
        try:
            if proxy:
                proxy_dict = {'scheme': 'http', 'hostname': proxy, 'port': 8080}
                self.tg_client.proxy = proxy_dict
            else:
                self.tg_client.proxy = None

            if not self.tg_client.is_connected:
                await self.tg_client.connect()
                logger.info(self.session_name, f"Connected to Telegram client.")

            peer = await self.tg_client.resolve_peer('seed_coin_bot')

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
            ))

            auth_url = web_view.url
            tg_web_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            return tg_web_data
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error(self.session_name, "Error retrieving data.")
            return None