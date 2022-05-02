import asyncio
import calendar as cld
import json
import random
import re
import typing
from datetime import datetime, timedelta
from io import BytesIO
from os import environ
from typing import Dict, List, Literal

import aiohttp
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

import disnake
import emoji as emj
from bs4 import BeautifulSoup
from core.classes import LeylaTasks
from disnake.ext import commands
from Tools.buttons import CurrencyButton
from Tools.decoders import Decoder
from Tools.exceptions import CustomError
from Tools.links import emoji_converter, emoji_formats, fotmat_links_for_avatar
from Tools.translator import Translator


class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description="Вывод аватара участника"
    )
    async def avatar(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        formats = [
            f"[PNG]({user.display_avatar.replace(format='png', size=1024).url}) | ",
            f"[JPG]({user.display_avatar.replace(format='jpg', size=1024).url})",
            f" | [GIF]({user.display_avatar.replace(format='gif', size=1024).url})" if user.display_avatar.is_animated() else ""
        ]
        embed = await self.bot.embeds.simple(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            description=''.join(formats),
            image=user.display_avatar.url
        )
        return await inter.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def crypter(self, inter, decoder: typing.Literal['Морзе', 'Шифр Цезаря'], variant: typing.Literal['crypt', 'decrypt'], *, text):
        if decoder == "Морзе":
            if variant == 'crypt':
                morse = Decoder().to_morse(text)
            elif variant == 'decrypt':
                morse = Decoder().from_morse(text)

            embed = await self.bot.embeds.simple(
                title='Decoder/Encoder морзе.',
                description=morse
            )

        elif decoder == "Шифр Цезаря":
            if variant == 'crypt':
                cezar = ''.join([chr(ord(i)-3) for i in text])

            elif variant == 'decrypt':
                cezar = ''.join([chr(ord(i)+3) for i in text])

            embed = await self.bot.embeds.simple(
                title='Decoder/Encoder шифра Цезаря (3).',
                description=' '.join([i for i in cezar.split()])
            )

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, inter: disnake.ApplicationCommandInteraction):
        information = (
            f'Участников: **{len(inter.guild.members)}**',
            f'Эмодзи: **{len(inter.guild.emojis)}**',
            f'Количество ролей: **{len(inter.guild.roles)}**',
            f'Ботов на сервере: **{len(list(filter(lambda user: user.bot, inter.guild.members)))}**'
        )
        embed = await self.bot.embeds.simple(
            title=f'Информация о гильдии {inter.guild.name}',
            description="\n".join(information)
        )

        if inter.guild.banner:
            embed.set_thumbnail(inter.guild.banner.url)

        if inter.guild.icon:
            embed.set_thumbnail(inter.guild.icon)

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о юзере"
    )
    async def user(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        embed = await self.bot.embeds.simple(title=f'Информация о {"боте" if user.bot else "пользователе"} {user.name}')
        user = await self.bot.fetch_user(user.id)
        color = Image.open(BytesIO(await user.display_avatar.read())).resize((720, 720)).convert('RGB')
        img = Image.new('RGBA', (500, 200), '#%02x%02x%02x' % color.getpixel((360, 360)))
        img.save('banner.png', 'png')
        file = disnake.File(BytesIO(open('banner.png', 'rb').read()), filename='banner.png')
        embed.set_image(url='attachment://banner.png')

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        
        main_information = [
            f"Зарегистрировался: **<t:{round(user.created_at.timestamp())}:R>** | {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней",
            f"Полный никнейм: **{str(user)}**",
            f"Бот?: **{'Да' if user.bot else 'Нет'}**"
        ]

        if user in inter.guild.members:
            user_to_member = inter.guild.get_member(user.id)
            second_information = [
                f"Зашёл(-ла) на сервер: **<t:{round(user_to_member.joined_at.timestamp())}:R> | {(datetime.utcnow() - user_to_member.joined_at.replace(tzinfo=None)).days} дней**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
            ]

        embed.description = "\n".join(main_information) + "\n" + "\n".join(second_information) if user in inter.guild.members else "\n".join(main_information)

        await inter.send(embed=embed, file=file)

    @commands.slash_command(
        description="Получить эмодзик"
    )
    async def emoji(self, inter, emoji):
        if emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH:
            await inter.send(emoji)
        else:
            get_emoji_id = int(''.join(re.findall(r'[0-9]', emoji)))
            url = f"https://cdn.discordapp.com/emojis/{get_emoji_id}.gif?size=480&quality=lossless"
            embed = await self.bot.embeds.simple(
                title=f"Эмодзи **{emoji}**",
                image=await emoji_converter('webp', url)
            )

            await inter.send(embed=embed)

    @commands.slash_command(description="Данная команда может поднять сервер в топе на boticord'e")
    async def up(self, inter: disnake.ApplicationCommandInteraction):
        data = {
            "serverID": str(inter.guild.id),
            "up": 1,
            "status": 1,
            "serverName": inter.guild.name,
            "serverAvatar": inter.guild.icon.url if inter.guild.icon else None,
            "serverMembersAllCount": len(inter.guild.members),
            "serverOwnerID": str(inter.guild.owner_id),
            "serverOwnerTag": str(inter.guild.owner),
        }

        async with self.bot.session.post(
            'https://api.boticord.top/v1/server', 
            headers={'Authorization': environ['BCORD']}, 
            json=data
        ) as response:
            data = await response.json()
        
            if not response.ok:
                return
            else:
                server = data["serverID"]
                embed = await self.bot.embeds.simple(
                    title='Перейти на BotiCord!',
                    description="У меня нет доступа к API методу(\nЗайдите на [сервер поддержки](https://discord.gg/43zapTjgvm) для дальнейшей помощи" if "error" in data else data["message"], 
                    url=f"https://boticord.top/add/server" if "error" in data else f"https://boticord.top/server/{server}"
                )

                await inter.send('Благодарю за поддержку сервера! <3' if 'успешно' in data['message'] else None, embed=embed)

    @commands.slash_command(name='emoji-random', description="Я найду тебе рандомный эмодзик :3")
    async def random_emoji(self, inter):
        emoji = random.choice(self.bot.emojis)
        await inter.send(embed=await self.bot.embeds.simple(description="Эмодзяяяяяяяя", image=emoji.url, fields=[{'name': 'Скачать эмодзик', 'value': f'[ТЫКТЫКТЫК]({emoji.url})'}]))

    @commands.slash_command(name="random-anime", description="Вы же любите аниме? Я да, а вот тут я могу порекомендовать вам аниме!")
    async def random_anime(self, inter):
        url = 'https://animego.org'

        async with aiohttp.ClientSession(
            headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.91',
                'cookie': environ['COOKIE']
            }) as session:
            async with session.get(f'{url}/anime/random') as res:
                soup = BeautifulSoup(await res.text(), 'html.parser')
                name = soup.select('.anime-title')[0].find('h1', class_=False).text
                img = soup.find('div', class_='anime-poster').find('img', class_=False).get('src')
                desc = soup.find('div', class_='description').text
                url = f'{url}{res.url._val.path}'
                await session.close()
        desc = re.sub('\n', '', desc, 1)
        await inter.send(embed=await self.bot.embeds.simple(
                description=f'**[{name}]({url})**\n**Описание**\n> {desc}',
                thumbnail=re.sub('media/cache/thumbs_\d{3}x\d{3}', '', img)
            )
        )

    @commands.slash_command(name="currency", description="Подскажу вам курс той или иной валюты :) (В рублях!)")
    async def currency_converter(self, inter, currency, how_many: float = 0):
        async with self.bot.session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
            cb_data = await response.text()

        json_cb_data = json.loads(cb_data)
        get_currency = {i:j['Name'] for i, j in json_cb_data['Valute'].items()}
        data = json_cb_data["Valute"]
        view = CurrencyButton()

        if currency.upper() in data:
            upper_currency = currency.upper()

            await inter.send(
                embed=await self.bot.embeds.simple(
                    title=f'Курс - {get_currency[upper_currency]} ({upper_currency})',
                    description=f'Один {get_currency[upper_currency]} на данный момент стоит **{round(data[upper_currency]["Value"], 2) / data[upper_currency]["Nominal"]}** рублей. ({round(data[upper_currency]["Value"] - data[upper_currency]["Previous"], 1)})',
                    fields=[
                        {
                            "name": "Абсолютная погрешность", 
                            "value": abs(data[upper_currency]["Value"] - round(data[upper_currency]["Value"])), 
                            'inline': True
                        }, 
                        {
                            "name": "Прошлая стоимость", 
                            "value": data[upper_currency]['Previous'] / data[upper_currency]['Nominal'], 
                            'inline': True
                        }, None if how_many == 0 else {
                            "name": f"Сколько **{how_many} {upper_currency}** в рублях", 
                            "value": round(how_many * (data[upper_currency]['Value'] / data[upper_currency]['Nominal']), 2),
                        },
                    ],
                    footer={"text": 'Вся информация взята с официального API ЦБ РФ.', 'icon_url': 'https://cdn.discordapp.com/attachments/894108349367484446/951452412714045460/unknown.png?width=493&height=491'}
                ), view=view
            )
        else:
            await inter.send(embed=await self.bot.embeds.simple(title='Курс... Так, стоп', description="Такой валюты не существует! Попробуйте выбрать любую из валют (Кнопка ниже)"), view=view)

    @commands.slash_command(description="Переведу тебе всё, что можно!")
    async def trasnlate(self, inter, text, to_language, from_language = 'ru'):
        data = await Translator().translate(text, to_language, from_language)

        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Лейла-переводчик',
                description=data,
                fields=[{"name": "Оригинальный текст", "value": text}],
                footer={"text": f'Переводено с {from_language} на {to_language}', 'icon_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/1200px-Google_Translate_logo.svg.png'}
            )
        )

    @commands.slash_command(description="Помогу решить почти любой пример!")
    async def calculator(self, inter, expression: str):
        async with self.bot.session.get(f'http://api.mathjs.org/v4/?expr={expression}') as response:
            data = await response.text()
        
        await inter.send(
            embed=await self.bot.embeds.simple(
                title='Калькулятор',
                fields=[{"name": "Введённый пример", "value": expression, 'inline': True}, {'name': "Результат", "value": data, 'inline': True}]
            )
        )

    @commands.slash_command(name="bcinfo", description="Вывод информации о сервере с BotiCord")
    async def boticord_info_cmd(self, inter, guild = None):
        async with self.bot.session.get(f'https://api.boticord.top/v1/server/{self.bot.get_guild(guild).id if self.bot.get_guild(guild) in self.bot.guilds else inter.guild.id if guild is None else guild}') as response:
            request = await response.json()

        if 'information' in request.keys():
            links_array = [
                f"Инвайт: {request['information']['links']['invite']}" if request['information']['links']['invite'] else None,
                f"Твич: {request['information']['links']['twitch']}" if request['information']['links']['twitch'] else None,
                f"Стим: {request['information']['links']['steam']}" if request['information']['links']['steam'] else None,
                f"ВК: {request['information']['links']['vk']}" if request['information']['links']['vk'] else None,
                f"Сайт: {request['information']['links']['site']}" if request['information']['links']['site'] else None,
                f"Ютуб: {request['information']['links']['youtube']}" if request['information']['links']['youtube'] else None,
            ]
            md = cld.monthrange(datetime.now().year, datetime.now().month)[-1]
            embed = await self.bot.embeds.simple(
                title=request['information']['name'],
                description=f'**Владелец:** {guild.owner.name if guild else inter.guild.owner.name}\n' + request['information']['longDescription'] if guild in self.bot.guilds else '' + request['information']['longDescription'],
                url=f"https://boticord.top/server/{self.bot.get_guild(guild).id if self.bot.get_guild(guild) in self.bot.guilds else inter.guild.id if guild is None else guild}",
                footer={"text": request['information']['shortDescription'], 'icon_url': inter.author.display_avatar.url},
                fields=[
                    {
                        "name": f"Количество бампов (оценок) | До сброса (дней)",
                        "value": str(request['information']['bumps']) + " | " + str(md - datetime.now().day),
                        "inline": True
                    },
                    {
                        "name": "Количество участников",
                        "value": request['information']['members'][0],
                        "inline": True
                    },
                    {
                        "name": "Тэги",
                        "value": ', '.join(request['information']['tags']) if len(request['information']['tags']) > 0 else "У этого сервера нет тэгов.",
                        "inline": True
                    },
                    {
                        "name": "Прочие ссылки",
                        "value": "\n".join([i for i in links_array if not i is None]),
                        "inline": True
                    }
                ],
            )

            if request['shortCode']:
                embed.add_field(name="Короткая ссылка", value=f'https://bcord.cc/s/{request["shortCode"]}', inline=True)

            if request['information']['avatar']:
                embed.set_thumbnail(url=request['information']['avatar'])
        else:
            raise CustomError("Сервера нет на ботикорд (или произошла какая-либо непредвиденная ошибка).")

        await inter.send(embed=embed)

    @commands.slash_command(name="afk", description="Встали в афк? Ну ладно, подождём.")
    async def utilities_afk_command(self, inter):
        if await self.bot.config.DB.afk.count_documents({"_id": inter.guild.id}) == 0:
            await self.bot.config.DB.afk.insert_one({"_id": inter.guild.id, "afk_members": [inter.author.id]})
        else:
            await self.bot.config.DB.afk.update_one({"_id": inter.guild.id}, {"$push": {"afk_members": inter.author.id}})

        await inter.send(embed=await self.bot.embeds.simple(description="Я поставила вас в список AFK, ждём вашего возвращения :relaxed:"))

    @commands.slash_command(name="giveaway", description="Можно всякие там розыгрыши делатц...")
    @commands.has_permissions(manage_roles=True)
    async def utilities_giveaway(
        self, inter, 
        giveaway_channel: disnake.TextChannel, prize: str,
        time: int, unit: Literal['Секунд', 'Минут', 'Часов', 'Дней'], prizes_count: int = 1
    ):
        if time <= 0:
            raise CustomError("Э! Ниже нуля нельзя! Время укажите, пожалуйста, корректное \🥺")
        else:
            time_convert = {
                'Секунд': datetime.now() + timedelta(seconds=time),
                'Минут': datetime.now() + timedelta(minutes=time),
                'Часов': datetime.now() + timedelta(hours=time),
                'Дней': datetime.now() + timedelta(days=time)
            }

            embed = await self.bot.embeds.simple(
                title='> Розыгрыш!', 
                description=f"**Приз:** {prize}", 
                footer={"text": f'До окончания: {time} {unit.lower()}', 'icon_url': inter.author.display_avatar.url}
            )
            message = await giveaway_channel.send(embed=embed)
            await message.add_reaction('👍')
            await self.bot.config.DB.giveaway.insert_one({"guild": inter.guild.id, "count": prizes_count, "prize": prize, "time": time_convert[unit], "channel": giveaway_channel.id if giveaway_channel is not None else inter.channel.id, "message_id": message.id})

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
