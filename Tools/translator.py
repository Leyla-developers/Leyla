from this import d
from core.bot import Leyla
import html
import re


class Translator:
    
    def __init__(self, bot: Leyla):
        self.bot = bot

    def normal_data(self, text):
        return html.unescape(text)

    async def translate(self, text, to_lang, from_lang):
        async with self.bot.session.get(f'https://translate.google.com/m?tl={to_lang}&sl={from_lang}&q={text}') as response:
            data = await response.read()

        data = data.decode('utf-8')
        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', data)

        return self.normal_data(result[0])
