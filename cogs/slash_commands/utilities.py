import re
import json
import random
import typing
import asyncio
import calendar as cld
from io import BytesIO
from os import environ
from typing import Literal
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta

import aiohttp
from PIL import Image
from textwrap3 import wrap
from humanize import naturaldelta

import disnake
import wikipedia
import emoji as emj
from bs4 import BeautifulSoup
from disnake.ext import commands
from disnake import SelectOption
from google.translator import GoogleTranslator

from Tools.decoders import Decoder
from Tools.paginator import Paginator
from Tools.links import emoji_converter
from Tools.exceptions import CustomError
from Tools.buttons import CurrencyButton
from Tools.update_changer import updated_username


class WikiDropdown(disnake.ui.Select):
    def __init__(self, author: disnake.Member, wiki_options: list):
        self.author = author

        options = wiki_options
        super().__init__(
            placeholder="Выберите статью",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="wiki_dropdown"
        )

    async def callback(self, inter):
        await inter.response.defer()

        if inter.author.id == self.author.id:
            data = wikipedia.page(title=wikipedia.search(self.values[0])[0])
            embeds = [await inter.bot.embeds.simple(title=data.title, url=data.url, description=i) for i in wrap(data.content, 1998)]
            await inter.edit_original_message(embed=embeds[0], view=Paginator(pages=embeds, author=inter.author))
        else:
            await inter.send('Не ты вызывал команду!', ephemeral=True)


class Utilities(commands.Cog, name="слэш-утилиты", description="Вроде некоторые команды полезны, хд."):

    COG_EMOJI = "🔧"

    @commands.slash_command(
        description="Вывод аватара участника"
    )
    async def avatar(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        formats = [
            f"[PNG]({user.display_avatar.replace(format='png', size=1024).url}) | ",
            f"[JPG]({user.display_avatar.replace(format='jpg', size=1024).url})",
            f" | [GIF]({user.display_avatar.replace(format='gif', size=1024).url})" if user.display_avatar.is_animated() else ""
        ]
        embed = await inter.bot.embeds.simple(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            description=''.join(formats),
            image=user.display_avatar.url
        )
        await inter.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def crypter(self, inter, decoder: typing.Literal['Морзе', 'Шифр Цезаря'],
                      variant: typing.Literal['crypt', 'decrypt'], text):
        if decoder == "Морзе":            
            if variant == 'crypt':
                morse = Decoder().to_morse(text)
            elif variant == 'decrypt':
                morse = Decoder().from_morse(text)

            embed = await inter.bot.embeds.simple(
                title='Decoder/Encoder морзе.',
                description=morse
            )

        elif decoder == "Шифр Цезаря":
            if variant == 'crypt':
                cezar = ''.join([chr(ord(i) + 3) for i in text])

            elif variant == 'decrypt':
                cezar = ''.join([chr(ord(i) - 3) for i in text])

            embed = await inter.bot.embeds.simple(
                title='Decoder/Encoder шифра Цезаря (3).',
                description=' '.join([i for i in cezar.split()])
            )

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, inter: disnake.ApplicationCommandInteraction, guild: disnake.Guild = commands.Param(lambda inter: inter.guild)):
        channel_ids = sorted(list(i.id for i in guild.channels if not isinstance(i, disnake.CategoryChannel)))
        role_ids = sorted(list(i.id for i in guild.roles if i.id != guild.default_role.id and not i.is_integration()))
        member_ids = sorted(list(i.id for i in guild.members if not i.bot))
        last_joined = list(i.mention + ' | ' + f'<t:{round(i.joined_at.timestamp())}:R>' for i in guild.members if i.joined_at == sorted(list(map(lambda x: x.joined_at, list(filter(lambda x: x.id != guild.owner_id, guild.members)))))[-1])
        first_joined = list(i.mention + ' | ' + f'<t:{round(i.joined_at.timestamp())}:R>' for i in guild.members if i.joined_at == sorted(list(map(lambda x: x.joined_at, list(filter(lambda x: x.id != guild.owner_id, guild.members)))))[0]) # Колбаски ^--------------^

        members = (
            f'Ботов: **{len(list(i.id for i in guild.members if i.bot))}**',
            f'Участников (не считая ботов): **{len(list(i.id for i in guild.members if not i.bot))}**',
            f'Участников <:leyla_online:980318029764251679> (считая ботов): **{len(list(filter(lambda x: x.status == disnake.Status.online, guild.members)))}**',
            f'Участников <:leyla_dnd:980318029860704317>: **{len(list(filter(lambda x: x.status == disnake.Status.dnd, guild.members)))}**',
            f'Участников <:leyla_idle:980318419859685457>: **{len(list(filter(lambda x: x.status == disnake.Status.idle, guild.members)))}**',
            f'Участников <:leyla_offline:980318029877502003>: **{len(list(filter(lambda x: x.status == disnake.Status.offline, guild.members)))}**',
        )
        dates = (
            f'Дата создания сервера: <t:{round(guild.created_at.timestamp())}:R>',
            f'Самый старый канал: {guild.get_channel(channel_ids[0]).mention} | <t:{round(guild.get_channel(channel_ids[0]).created_at.timestamp())}:R>',
            f'Самый молодой канал: {guild.get_channel(channel_ids[-1]).mention} | <t:{round(guild.get_channel(channel_ids[-1]).created_at.timestamp())}:R>',
            f'Самая старая роль: {guild.get_role(role_ids[0]).mention} | <t:{round(guild.get_role(role_ids[0]).created_at.timestamp())}:R>',
            f'Самая молодая роль: {guild.get_role(role_ids[-1]).mention} | <t:{round(guild.get_role(role_ids[-1]).created_at.timestamp())}:R>',
            f'Самый старый участник: {guild.get_member(member_ids[0]).mention} | <t:{round(guild.get_member(member_ids[0]).created_at.timestamp())}:R>',
            f'Самый молодой участник: {guild.get_member(member_ids[-1]).mention} | <t:{round(guild.get_member(member_ids[-1]).created_at.timestamp())}:R>',
            f'Первый зашедший участник: {"".join(first_joined)}',
            f'Последний зашедший участник: {"".join(last_joined)}'
        )
        boosts = (
            f'Включен ли прогресс бустов: **{"Да" if guild.premium_progress_bar_enabled else "Нет"}**',
            f'Бустеров: **{len(guild.premium_subscribers)}**',
            f'Уровень буста: **{guild.premium_tier}**'
        )
        channels = (
            f'Всего каналов: **{len(guild.channels)}**',
            f'Голосовых: **{len(guild.voice_channels)}**',
            f'Текстовых: **{len(guild.text_channels)}**',
            f'Веток: **{len(guild.threads)}**',
            f'Канал правил: {guild.rules_channel.mention if guild.rules_channel else "Отсутствует"}',
            f'Системный канал (чат, куда приходят о том, что кто-то зашёл, бустах и пр.): {guild.system_channel.mention if guild.system_channel else "Отсутствует"}',
        )
        other = (
            f'Стикеров: **{len(guild.stickers)}**',
            f'Эмодзи: **{len(guild.emojis)}**',
            f'Сплэш: Отсутствует' if not guild.splash else f'Сплэш: [ссылка здесь]({guild.splash})',
            f'Владелец: {guild.owner.name}',
            f'Максимальное количество участников: **{guild.max_members}**',
            f'Айди шарда: **{guild.shard_id}**',
        )
        roles = (
            f'Количество ролей: **{len(guild.roles)}**',
            f'Ваша высшая роль: {inter.author.top_role.mention if inter.author in guild.members else "Вам нет на этом сервере("}',
            f'Роль бустеров: {guild.premium_subscriber_role.mention if bool(guild.premium_subscriber_role) else "На сервере нет роли бустеров"}',
        )

        fields = [
            {'name': '> Участники', 'value': '\n'.join(members)},
            {'name': '> Даты', 'value': '\n'.join(dates)},
            {'name': '> Бусты', 'value': '\n'.join(boosts)},
            {'name': '> Каналы', 'value': '\n'.join(channels)},
            {'name': '> Роли', 'value': '\n'.join(roles)},
            {'name': '> Прочее', 'value': '\n'.join(other)},
        ]
        embed = await inter.bot.embeds.simple(
            title=f'Информация о {guild.name}', 
            description='У сервера нет описания :(' if not guild.description else guild.description, 
            fields=fields,
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о юзере"
    )
    async def user(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        statuses = {
            disnake.Status.online: '<:leyla_online:980318029764251679>',
            disnake.Status.dnd: '<:leyla_dnd:980318029860704317>',
            disnake.Status.idle: '<:leyla_idle:980318419859685457>',
            disnake.Status.offline: '<:leyla_offline:980318029877502003>'
        }
        embed = await inter.bot.embeds.simple(title=f'Информация о {"боте" if user.bot else "пользователе"} {user.name}')
        user = await inter.bot.fetch_user(user.id)

        if user.banner:
            embed.set_image(url=user.banner.url)

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")

        main_information = [
            f"Зарегистрировался: **<t:{round(user.created_at.timestamp())}:R>** | {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней",
            f"Полный никнейм: **{updated_username(user)}**",
        ]

        embeds = [embed]

        if user in inter.guild.members:
            user_to_member = inter.guild.get_member(user.id)
            bool_to_symbol = {True: '+', False: '-'}

            embed.title = f'Информация о {"боте" if user.bot else "пользователе"} {user.name} {"📱" if user_to_member.is_on_mobile() else "🖥️"}'

            permissions_embed = inter.bot.embed(
                title=f'Права {user_to_member}',
                description='```' + 'diff\n' + '\n'.join([f'{bool_to_symbol[i[-1]]} {i[0].replace("_", " ").capitalize()}' for i in user_to_member.guild_permissions]) + '```'
            ).start()
            embeds.append(permissions_embed)

            spotify = list(filter(lambda x: isinstance(x, disnake.activity.Spotify), user_to_member.activities))
            second_information = [
                f"Зашёл(-ла) на сервер: **<t:{round(user_to_member.joined_at.timestamp())}:R> | {(datetime.utcnow() - user_to_member.joined_at.replace(tzinfo=None)).days} дней**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
                f"Статус: {statuses[user_to_member.status]}"
            ]

            if len(spotify):
                data = spotify[0]
                timestamps = (str(data._timestamps['end'])[:10], str(data._timestamps['start'])[:10])

                embed.add_field(
                    name="Информация про трек спотифай", 
                    value=f"Песня: [{data.title} | {', '.join(data.artists)}]({data.track_url})\n" \
                        f"Альбом: [{data.album}]({data.album_cover_url})\n" \
                        f"Длительность песни: {naturaldelta(data.duration.total_seconds())} | <t:{timestamps[0]}:R> - <t:{timestamps[-1]}:R>"
                )

            if len(user_to_member.activities) > 0:
                activities_embed = inter.bot.embed(
                    title=f"Активности {user_to_member}",
                    description='\n'.join([f'{i.name} | <t:{round(i.created_at.timestamp())}:R>' for i in user_to_member.activities])
                ).start()
                embeds.append(activities_embed)

        embed.description = "\n".join(main_information) + "\n" + "\n".join(second_information) if user in inter.guild.members else "\n".join(main_information)
        
        if len(embeds) > 1:
            view = Paginator(embeds, inter.author)
        else:
            view = None

        await inter.send(embed=embeds[0], view=view) if view is not None else await inter.send(embed=embeds[0])


    @commands.slash_command(
        description="Получить эмодзик"
    )
    async def emoji(self, inter, emoji):
        if emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH:
            await inter.send(emoji)
        else:
            get_emoji_id = int(''.join(re.findall(r'[0-9]', emoji)))
            url = f"https://cdn.discordapp.com/emojis/{get_emoji_id}.gif?size=480&quality=lossless"
            embed = await inter.bot.embeds.simple(
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
            "serverMembersOnlineCount": len(list(filter(lambda x: not x.status == disnake.Status.offline, inter.guild.members))),
            "serverOwnerID": str(inter.guild.owner_id),
            "serverOwnerTag": str(inter.guild.owner),
            "upUserId": str(inter.author.id),
            "upChannelID": str(inter.channel.id),
            "upChannelName": inter.channel.name
        }

        async with inter.bot.session.post(
            'https://api.boticord.top/v2/server',
            headers={'Authorization': 'Bot ' + environ['BCORD']},
            json=data
        ) as response:
            data = await response.json()
            embed = await inter.bot.embeds.simple(
                title='Перейти на BotiCord!',
                description="У меня нет доступа к API методу(\nЗайдите на [сервер поддержки](https://discord.gg/43zapTjgvm) для дальнейшей помощи" if "error" in data else data["message"],
                url=f"https://boticord.top/add/server" if "error" in data else f"https://boticord.top/server/{inter.guild.id}"
            )

            await inter.send(
                'Благодарю за поддержку сервера! <3' if 'успешно' in data['message'] else None,
                embed=embed
            )

    @commands.is_nsfw()
    @commands.slash_command(name='emoji-random', description="Я найду тебе рандомный эмодзик :3")
    async def random_emoji(self, inter):
        emoji = random.choice(inter.bot.emojis)
        await inter.send(embed=await inter.bot.embeds.simple(description="Эмодзяяяяяяяя", image=emoji.url, fields=[
            {'name': 'Скачать эмодзик', 'value': f'[ТЫКТЫКТЫК]({emoji.url})'}]))

    @commands.slash_command(
        name="random-anime",
        description="Вы же любите аниме? Я да, а вот тут я могу порекомендовать вам аниме!",
        guild_ids=[864367089102749726]
    )
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
        await inter.send(
            embed=await inter.bot.embeds.simple(
                description=f'**[{name}]({url})**\n**Описание**\n> {desc}',
                thumbnail=re.sub('media/cache/thumbs_\d{3}x\d{3}', '', img)
            )
        )

    @commands.slash_command(name="currency", description="Подскажу вам курс той или иной валюты :) (В рублях!)")
    async def currency_converter(self, inter, currency, how_many: float = 0):
        async with inter.bot.session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
            cb_data = await response.text()

        json_cb_data = json.loads(cb_data)
        get_currency = {i: j['Name'] for i, j in json_cb_data['Valute'].items()}
        data = json_cb_data["Valute"]
        view = CurrencyButton()

        if currency.upper() in data:
            upper_currency = currency.upper()

            await inter.send(
                embed=await inter.bot.embeds.simple(
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
                            "value": round(how_many * (data[upper_currency]['Value'] / data[upper_currency]['Nominal']),
                                           2),
                        },
                    ],
                    footer={"text": 'Вся информация взята с официального API ЦБ РФ.',
                            'icon_url': 'https://cdn.discordapp.com/attachments/894108349367484446/951452412714045460/unknown.png?width=493&height=491'}
                ), view=view
            )
        else:
            await inter.send(
                embed=await inter.bot.embeds.simple(
                    title='Курс... Так, стоп',
                    description="Такой валюты не существует! Попробуйте выбрать любую из валют (Кнопка ниже)"
                ), view=view
            )

    @commands.slash_command(description="Переведу тебе всё, что можно!")
    async def translate(self, inter, text, to_language, from_language='auto'):
        google = GoogleTranslator()
        data = await google.translate_async(text, to_language, from_language)

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='Лейла-переводчик',
                description=data,
                fields=[{"name": "Оригинальный текст", "value": text}],
                footer={
                    "text": f'Переводено с {from_language} на {to_language}',
                    'icon_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/1200px-Google_Translate_logo.svg.png'
                }
            )
        )

    @commands.slash_command(description="Помогу решить почти любой пример!")
    async def calculator(self, inter, expression: str):
        async with inter.bot.session.get(f'http://api.mathjs.org/v4/?expr={quote(expression)}') as response:
            data = await response.text()

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='Калькулятор',
                fields=[{"name": "Введённый пример", "value": expression, 'inline': True},
                        {'name': "Результат", "value": data, 'inline': True}]
            )
        )

    @commands.slash_command(name="bcinfo", description="Вывод информации о сервере с BotiCord")
    async def boticord_info_cmd(self, inter):
        ...

    @boticord_info_cmd.sub_command(name='server', description="Вывод информации о сервере с BotiCord'a!")
    async def boticord_server_info(self, inter, guild=None):
        async with inter.bot.session.get(
                f'https://api.boticord.top/v1/server/{inter.bot.get_guild(guild).id if inter.bot.get_guild(guild) in inter.bot.guilds else inter.guild.id if guild is None else guild}') as response:
            request = await response.json()

        if 'information' in request.keys():
            links_array = [
                f"Инвайт: {request['information']['links']['invite']}" if request['information']['links'][
                    'invite'] else None,
                f"Твич: {request['information']['links']['twitch']}" if request['information']['links'][
                    'twitch'] else None,
                f"Стим: {request['information']['links']['steam']}" if request['information']['links'][
                    'steam'] else None,
                f"ВК: {request['information']['links']['vk']}" if request['information']['links']['vk'] else None,
                f"Сайт: {request['information']['links']['site']}" if request['information']['links']['site'] else None,
                f"Ютуб: {request['information']['links']['youtube']}" if request['information']['links'][
                    'youtube'] else None,
            ]
            md = cld.monthrange(datetime.now().year, datetime.now().month)[-1]
            embed = await inter.bot.embeds.simple(
                title=request['information']['name'],
                description=f'**Владелец:** {guild.owner.name if guild else inter.guild.owner.name}\n' +
                            BeautifulSoup(request['information']['longDescription'], 'lxml').text if guild in inter.bot.guilds else '' + BeautifulSoup(request[
                    'information']['longDescription']).text,
                url=f"https://boticord.top/server/{inter.bot.get_guild(guild).id if inter.bot.get_guild(guild) in inter.bot.guilds else inter.guild.id if guild is None else guild}",
                footer={"text": request['information']['shortDescription'],
                        'icon_url': inter.author.display_avatar.url},
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
                        "value": ', '.join(request['information']['tags']) if len(
                            request['information']['tags']) > 0 else "У этого сервера нет тэгов.",
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

    @boticord_info_cmd.sub_command(name='bot', description="Вывод информации о боте с BotiCord'a!")
    async def boticord_bot_info(self, inter, bot=None):
        async with inter.bot.session.get(f'https://api.boticord.top/v1/bot/{bot}') as response:
            request = await response.json()

        if 'information' in request:
            fetch_developers = [await inter.bot.fetch_user(i) for i in request["information"]["developers"]]
            fields = [
                {
                    "name": "Статистика", "value": f'Серверов: {request["information"]["stats"]["servers"]}\n' + \
                                                   f'Пользователей: {request["information"]["stats"]["users"]}\n' + \
                                                   f'Шардов: {request["information"]["stats"]["shards"]}\n', "inline": True
                }, 
                {"name": "Тэги", "value": ', '.join(request['information']['tags']), "inline": True},
                {
                    "name": "BCord статистика", "value": f'Оценок: {request["information"]["bumps"]}\n' + \
                                                         f'Добавлен раз: {request["information"]["added"]}\n' + \
                                                         f'Префикс: {request["information"]["prefix"]}\n', "inline": True
                },
                {"name": "Разработчики", "value": f'Разработчики: {", ".join([str(i) for i in fetch_developers])}\n', "inline": True}
            ]

            embed = await inter.bot.embeds.simple(
                title=f'Информация о {bot}', 
                description=BeautifulSoup(request['information']['longDescription'], 'lxml').text, 
                footer={'text': request['information']['shortDescription'], 'icon_url': inter.author.display_avatar.url},
                fields=fields
            )
            await inter.send(embed=embed)
        else:
            raise CustomError("Я не нашла ничего по такому запросу!")

    async def giveaway_check(self, interaction, time):
        await asyncio.sleep(time)

        async for i in interaction.bot.config.DB.giveaway.find({"time": {"$lte": datetime.now()}}):
            if interaction.bot.get_guild(i['guild']) in interaction.bot.guilds:
                message = await interaction.bot.get_channel(i['channel']).fetch_message(i['message_id'])
                embed = await interaction.bot.embeds.simple(
                    title='> Розыгрыш окончен!', 
                    description=f"**Приз:** {i['prize']}\n**Победитель:** {''.join(random.choices([i.mention async for i in message.reactions[0].users()], k=i['count']))}",
                )
                await message.edit(embed=embed)
        
            await interaction.bot.config.DB.giveaway.delete_one({"guild": i['guild'], 'prize': i['prize']})


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
                'Дней': datetime.now() + timedelta(days=time),
            }

            embed = await inter.bot.embeds.simple(
                title='> Розыгрыш!',
                description=f"**Приз:** {prize}",
                footer={"text": f'До окончания: {time} {unit.lower()}', 'icon_url': inter.author.display_avatar.url}
            )
            message = await giveaway_channel.send(embed=embed)
            await message.add_reaction('👍')
            await inter.bot.config.DB.giveaway.insert_one(
                {"guild": inter.guild.id, "count": prizes_count, "prize": prize, "time": time_convert[unit],
                 "channel": giveaway_channel.id,
                 "message_id": message.id}
            )
            asyncio.create_task(self.giveaway_check(inter, time_convert[unit]))

    @commands.slash_command(name='role-info', description="Выдам информацию о любой роли на сервере")
    async def utilities_role_info(self, inter, role: disnake.Role):
        role_info_array = [
            f'Цвет роли: **{hex(role.color.value)}**',
            f'Интеграция: **{"Да" if role.is_integration() else "Нет"}**',
            f'Участников на этой роли: **{len(role.members)}**',
            f'ID роли: **{role.id}**',
            f'Упоминание роли: {role.mention}',
            f'Позиция: **{role.position}**',
            f'Роль создана: <t:{round(role.created_at.timestamp())}:D>'
        ]
        embed = await inter.bot.embeds.simple(
            title=f"Информация о {role.name}",
            description='\n'.join(role_info_array),
        )

        if role.icon:
            embed.set_thumbnail(url=role.icon.url)

        await inter.send(embed=embed)

    @commands.slash_command(
        name='wikipedia',
        description="Найдётся всё!"
    )
    async def utilities_wiki(self, inter, query: str) -> str:
        wikipedia.set_lang(prefix='ru')
        wiki_view = disnake.ui.View()

        if len(wikipedia.search(query)):
            wiki_view.add_item(
                WikiDropdown(
                    wiki_options=[SelectOption(label=i) for i in wikipedia.search(query)],
                    bot=inter.bot,
                    author=inter.author
                )
            )
        else:
            wiki_view.add_item(disnake.ui.Button(label='Ничего не найдено :(', disabled=True))

        await inter.send(view=wiki_view)


    @commands.slash_command(
        name="reminder",
        description='Напоминалка'
    )
    async def utilities_reminder(self, inter):
        ...

    async def reminder_task(self, inter):
        await asyncio.sleep(1)
        db = inter.bot.config.DB.reminder
        reminders = db.find({'time': {'$lte': datetime.now()}})

        async for reminder in reminders:
            ids = reminder['member']
            member = await inter.bot.fetch_user(ids)
            channel = await inter.bot.fetch_channel(reminder['channel'])
            embed = await inter.bot.embeds.simple(
                title='Вы ничего не забыли?',
                description='Вы просили меня, напомнить Вас о чём-то важном, наверное',
                fields=[{'name': 'Напоминание', 'value': reminder['text'] if len(reminder['text']) < 1024 else reminder['text'][:1023]+'...'}]
            )

            await channel.send(content=member.mention, embed=embed)
            return await db.delete_one(reminder)

    @utilities_reminder.sub_command(
        name="set",
        description='Установка напоминания',
    )
    async def reminder_set(self, inter, text: str, duration: int, unit: Literal['Секунд', 'Минут', 'Часов', 'Дней']):
        time_convert = {
            'Секунд': datetime.now() + timedelta(seconds=duration),
            'Минут': datetime.now() + timedelta(minutes=duration),
            'Часов': datetime.now() + timedelta(hours=duration),
            'Дней': datetime.now() + timedelta(days=duration)
        }
        db = inter.bot.config.DB.reminder

        if not re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', text):
            if duration <= 0:
                raise CustomError("Э! Ниже нуля нельзя! Продолжительность укажите, пожалуйста, корректную \🥺")
            else:
                await db.insert_one({"guild": inter.guild.id, "member": inter.author.id, "text": text, 'time': time_convert[unit], 'channel': inter.channel.id})
                await inter.send(
                    embed=await inter.bot.embeds.simple(
                        title="Напоминалка установлена!",
                        fields=[
                            {'name': 'Сообщение', 'value': text[:1023]},
                            {'name': 'Время', 'value': f'{duration} {unit.lower()}'}
                        ]
                    )
                )
                await asyncio.create_task(self.reminder_task())
        else:
            await inter.send('Нельзя добавлять ссылки, увы :(')
    
    @commands.slash_command(
        name="invites",
        description="Показывает топ приглашений"
    )
    async def invites_top_info(self, inter):
        data = enumerate(sorted([(i.uses, str(i.inviter), i.url) for i in await inter.guild.invites()], key=lambda x: x[0], reverse=True))
        invite_data = list(data)
        yield_invite_data = lambda _: (f'{i[0]+1}. "{i[-1][-1].split("/")[-1]}" -> {i[1][0]} | {i[1][1]}' for i in invite_data if i[0]+1 <= 15)

        await inter.send(
            embed=inter.bot.embed(
                title="Топ тех, кто приглашал", 
                description='```py\n' + '\n'.join(list(yield_invite_data(invite_data))) + '```'
            ).start()
        )


def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
