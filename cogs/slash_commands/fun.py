from asyncio import sleep
from io import BytesIO
from typing import Literal
from random import randint, choices
from string import punctuation
from typing import Literal
from threading import Thread

import disnake
from disnake.ext import commands
import blurplefier

from Tools.exceptions import CustomError
from Tools.images import ship_image
from services import waifu_pics

OVERLAY_DESCRIPTIONS = {
    'jail': '`{0}` За шо сидим?',
    'wasted': 'R.I.P. `{0}` погиб(-ла) смертью храбрых :D',
    'gay': '🤭',
    'triggered': 'ВЫАЫВОАЫАОЫВАЫВАРЫРАВЫРАЛО'
}


class FunSlashCommands(commands.Cog, name="развлечения", description="Всякие там развлекающие команды, да."):

    COG_EMOJI = "⚽"

    def __init__(self, bot) -> None:
        self.bot = bot


    def word_game_validator(self, message: disnake.Message, author: disnake.Member):
        check = lambda x: ''.join([i for i in x if i not in ' '.join(punctuation).split()])
        return check(message.replace('ъ', '').replace('ь', '').replace(' ', '')), author


    @commands.slash_command(description="Случайное число от a до b")
    async def random(self, inter: disnake.ApplicationCommandInteraction, a: int = commands.Param(description="Первое число"), b: int = commands.Param(description="Второе число")):
        if b < a or a == b:
            raise CustomError('Второе число не должно быть равно первому либо быть меньше чем оно owo')

        await inter.send(f'Выпавшее число: {randint(a, b)}')

    @commands.slash_command(
        options=[
            disnake.Option(
                'overlay', 'выберите наложение', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['wasted', 'jail', 'comrade', 'gay', 'glass', 'passed', 'triggered', 'blurple']
            ),
            disnake.Option('user', 'Выберите пользователя', type=disnake.OptionType.user, required=False)
        ],
        name='avatar-overlay',
        description="Накладывает разные эффекты на аватар."
    )
    async def overlay_image(self, inter: disnake.ApplicationCommandInteraction, overlay: str, user: disnake.User = commands.Param(lambda inter: inter.author)):
        if overlay == 'blurple':
            input_bytes = await user.display_avatar.read()
            extension, blurplefied_bytes = blurplefier.convert_image(
                input_bytes, blurplefier.Methods.CLASSIC
            )
            avatar_bytes = BytesIO(blurplefied_bytes)

            await inter.send(file=disnake.File(avatar_bytes, filename=f'blurplefied_file.{extension}'))
        else:
            async with inter.bot.session.get(f'https://some-random-api.ml/canvas/{overlay}?avatar={user.display_avatar.url.replace("gif", "png")}') as response:
                data = await response.read()
                image_bytes = BytesIO(data)
                image_filename = f'overlay.{"png" if overlay != "triggered" else "gif"}'
                embed = await inter.bot.embeds.simple(title=OVERLAY_DESCRIPTIONS.get(overlay).format(user) if overlay in OVERLAY_DESCRIPTIONS else disnake.embeds.EmptyEmbed, image=f'attachment://{image_filename}')
                await inter.send(embed=embed, file=disnake.File(image_bytes, filename=image_filename))

    @commands.slash_command(
        options=[
            disnake.Option(
                'choice', 'Выберите девАтЬку owo', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['megumin', 'shinobu', 'awoo', 'neko', 'poke']
            )
        ],
        name='anime-girl',
        description="Аниме тянки"
    )
    async def anime_girl(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        embed = await inter.bot.embeds.simple(title=f'{choice.title()} OwO', image=await waifu_pics.get_image('sfw', choice.lower()))
        return await inter.send(embed=embed)

    @commands.slash_command(name="ship", description="Создание шип-картинки")
    async def ship_not_ship(
        self, 
        inter, 
        user_one: disnake.User,
        second_user: disnake.User
    ):
        await inter.response.defer()
        percentage = randint(1, 100)
        get_image = ship_image(percentage, user_one, second_user)
        file = disnake.File(get_image.image_bytes, 'ship_img.png')

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title=f'*Толкнула {user_one.name} на {second_user.name}* <:awww:878155710796550145>' if percentage > 30 else 'Хрусь 💔',
                image='attachment://ship_img.png'
            ), file=file
        )

    @commands.slash_command(
        name="russian-roulette",
        description="Мой хозяин научил меня пользоваться револьвером"
    )
    async def fun_russian_roulette(self, inter, join_or_start_game: Literal['Начать', 'Присоединиться']):
        user_choice = {
            'Начать': 1,
            'Присоединиться': 2
        }
        db = inter.bot.config.DB.russian_roulette

        if user_choice[join_or_start_game] == 1:
            if await db.count_documents({"_id": inter.guild.id, "status": 0}) == 0: # "status": 0 = набор игроков, игра не началась. "status": 1 = игра началась
                await db.insert_one({"_id": inter.guild.id, "status": 0, "users": [], "queue": [inter.author.id], "host": inter.author.id})
                await inter.send(
                    embed=await inter.bot.embeds.simple(
                        title='Русская рулетка',
                        description="Новая игра начата! Ждём людей. Есть минута на подключение, если не будет хотя бы одного игрока - игра будет отменена"
                    )
                )
                await sleep(60)

                data = await db.find_one({"_id": inter.guild.id})

                if len(data['users']) > 0:
                    await inter.send(f'Игра началась! {inter.author.mention} ваш ход! (Игра будет длиться 600 секунд (10 минут))\nНужно ввести `выстрел`, чтоб сделать ход.')
                    await sleep(600)
                    await db.delete_one({"_id": inter.guild.id})
                else:
                    await inter.send("Игра была отменена. Недостаточно участников.")
                    await db.delete_one({"_id": inter.guild.id})
            else:
                game_status = await db.find_one({"_id": inter.author.id})

                if game_status['status'] == 0:
                    await inter.send(
                        embed=await inter.bot.embeds.simple(
                            title='Русская рулетка', 
                            description="На сервере уже есть действующее лобби, вы можете подключиться к нему!"
                        )
                    )
                else:
                    await inter.send(
                        embed=await inter.bot.embeds.simple(
                            title='Русская рулетка', 
                            description="На сервере уже есть действующее лобби, дождитесь окончания игры!"
                        )
                    )
        else:
            if await db.count_documents({"_id": inter.guild.id, "status": 0}) == 0:
                await inter.send('На сервере нет действующих лобби, вы можете попробовать создать новое!')
            else:
                data = await db.find_one({"_id": inter.guild.id})

                if data['host'] == inter.author.id:
                    await inter.send("Вы - хостер игры. Просто ожидайте чьего-нибудь подключения.")
                else:
                    await inter.send("Поздравляю! Вы вступили в игру, ожидайте.")
                    await db.update_one({"_id": inter.guild.id}, {"$push": {"users": inter.author.id}})

    @commands.slash_command(
        name="rps",
        description="Классическая для многих игра: камень, ножницы, бумага",
    )
    async def fun_rps(self, inter, user_choice: Literal['камень', 'ножницы', 'бумага']):
        variants = {'ножницы': 'бумага', 'камень': 'ножницы', 'бумага': 'камень'}
        bot_choice = ''.join(choices(list(variants.keys()), weights=[50, 30, 35], k=1))

        if user_choice == variants[bot_choice]:
            await inter.send(f'Я победила u-u! Мой выбор был: `{bot_choice}`')
        else:
            await inter.send(f'Ты победил(-а) (. Мой выбор был: `{bot_choice}`' if bot_choice != user_choice else f'Ничья, никто не победил 😅\n ||{user_choice} - {bot_choice}||')

    @commands.Cog.listener('on_message')
    async def russian_roulette_event(self, message):
        db = self.bot.config.DB.russian_roulette

        if await db.count_documents({"_id": message.guild.id}) == 0:
            return

        data = await db.find_one({"_id": message.guild.id})
        n = randint(1, 2) # 1 - выжил, 2 - нет

        if message.author.id in data['users'] or message.author.id in data['queue']:
            if data['queue'][0] == message.author.id:
                if message.content.lower() == "выстрел":
                    get_last_user_id = data['users'][-1]
                    if n == 1:
                        await message.channel.send(f'{message.author.mention} тебе повезло. Следующий! {message.guild.get_member(get_last_user_id).mention}')
                        await db.update_one({"_id": message.guild.id}, {"$pull": {'queue': message.author.id}})
                        await db.update_one({"_id": message.guild.id}, {"$push": {'queue': get_last_user_id}})
                        await db.update_one({"_id": message.guild.id}, {"$pull": {'users': get_last_user_id}})
                        await db.update_one({"_id": message.guild.id}, {"$push": {'users': message.author.id}})
                    else:
                        await db.update_one({"_id": message.guild.id}, {"$pull": {'queue': message.author.id}})
                        await db.update_one({"_id": message.guild.id}, {"$push": {'queue': get_last_user_id}})
                        await db.update_one({"_id": message.guild.id}, {"$pull": {'users': get_last_user_id}})

                        updated_data = await db.find_one({"_id": message.guild.id})

                        if len(updated_data['users']) + len(updated_data['queue']) == 1:
                            await message.channel.send(f'Игра окончена! Победитель: {message.guild.get_member(updated_data["queue"][0]).mention}')
                            await db.delete_one({"_id": message.guild.id})
                        else:
                            await message.channel.send(f'Застрелился(-ась) {message.author.mention}. Помянем. Следующий! {message.guild.get_member(get_last_user_id).mention}')

    @commands.Cog.listener('on_message')
    async def word_game_event(self, message):
        db = self.bot.config.DB.word_game

        if await db.count_documents({"_id": message.guild.id}) == 0:
            return

        data = db.find_one({'_id': message.guild.id})

        if message.channel.id == dict(await data)['channel']:
            if len([i async for i in message.channel.history()]) == 0:
                return
            
            if len([i async for i in message.channel.history()]) == 1:
                return
            
            last_message = [i async for i in message.channel.history()][1]
            msg = self.word_game_validator(last_message.content, last_message.author)

            if len(message.attachments) > 0:
                Thread(target=await message.delete()).run()

            if message.content[0].lower() != msg[0][-1].lower() or message.author.id == msg[-1].id:
                Thread(target=await message.delete()).run()


def setup(bot):
    bot.add_cog(FunSlashCommands(bot))
