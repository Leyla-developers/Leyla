from io import BytesIO
from PIL import Image
from random import randint, choice
from typing import Literal
import time
import datetime

import disnake
from disnake.ext import commands

from Tools.exceptions import CustomError
from Tools.images import ship_image
from services import waifu_pics


OVERLAY_DESCRIPTIONS = {
    'jail': '{user} За шо сидим?',
    'wasted': 'R.I.P. {user} погиб(-ла) смретью храбрых :D',
    'gay': '🤭',
    'triggered': 'ВЫАЫВОАЫАОЫВАЫВАРЫРАВЫРАЛО'
}


class FunSlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        options=[
            disnake.Option(name='a', type=disnake.OptionType.integer, description='Число от:'),
            disnake.Option(name='b', type=disnake.OptionType.integer, description='Число до:')
        ],
        description='Случайное число в заданном диапазоне'
    )
    async def random(self, inter: disnake.ApplicationCommandInteraction, a: int, b: int):
        if b < a or a == b:
            raise CustomError('Второе число не должно быть равно первому либо быть меньше чем оно owo')
        embed = await self.bot.embeds.simple(inter, title=f'Случайное число от `{a}` до `{b}`', thumbnail=inter.author.avatar.url)
        embed.add_field(name='Ваше число...', value=randint(a, b))
        return await inter.send(embed=embed)

    @commands.slash_command(
        options=[
            disnake.Option(
                'overlay', 'выберите наложение', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['wasted', 'jail', 'comrade', 'gay', 'glass', 'passed', 'triggered']
            ),
            disnake.Option('user', 'Выберите пользователя', type=disnake.OptionType.user, required=False)
        ],
        name='avatar-overlay',
        description="Накладывает разные эффекты на аватар."
    )
    async def jail_image(self, inter: disnake.ApplicationCommandInteraction, overlay: str, user: disnake.User = commands.Param(lambda inter: inter.author)):
        async with self.bot.session.get(f'https://some-random-api.ml/canvas/{overlay}?avatar={user.display_avatar.url}') as response:
            image_bytes = BytesIO(await response.read())
            image_filename = f'overlay.{"png" if overlay != "triggered" else "gif"}'
            embed = await self.bot.embeds.simple(inter, title=OVERLAY_DESCRIPTIONS.get(overlay, f'`{user}`'), image=f'attachment://{image_filename}')
            await inter.send(embed=embed, file=disnake.File(image_bytes, filename=image_filename))
            return await response.close()

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
        embed = await self.bot.embeds.simple(inter, title=f'{choice.title()} OwO', image=await waifu_pics.get_image('sfw', choice.lower()))
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
            embed=await self.bot.embeds.simple(
                title=f'*Толкнула {user_one.name} на {second_user.name}* <:awww:878155710796550145>' if percentage > 30 else 'Хрусь 💔',
                image='attachment://ship_img.png'
            ), file=file
        )

    @commands.slash_command(name='russian-roulette', description="Игра в русскую рулетку...)")
    async def fun_rr(self, inter, action: Literal['Войти', 'Начать игру']):
        if await self.bot.config.DB.russian_roulette.count_documents({"_id": inter.guild.id}) == 0:
            if action == "Начать игру":
                await self.bot.config.DB.russian_roulette.insert_one({"_id": inter.guild.id, "lobby": "rr", "step": [inter.author.id], "joined": [inter.author.id], "started_or_not": False, 'start_time': datetime.datetime.now().strftime("%H%M")})
                data = await self.bot.config.DB.russian_roulette.find_one({"_id": inter.guild.id})
                await inter.send("Лобби создано! Игра начнётся, когда будет >=3 игроков.")
                # if (int(msg.created_at.strftime('%H%M'))+5) - int(datetime.datetime.now().strftime('%H%M')) > data['start_time']:
            else:
                raise CustomError("Нет начатой игры!")

        else:
            if action == "Войти":
                data = await self.bot.config.DB.russian_roulette.find_one({"_id": inter.guild.id})

                if data['started_or_not']:
                    raise CustomError("Сейчас уже идёт игра, подождите, пока игра закончится!")
                else:
                    await self.bot.config.DB.russian_roulette.update_one({"_id": inter.guild.id}, {"$push": {"joined": inter.author.id}})
                    await inter.send("Я подключила вас к игре.")
                    new_data = await self.bot.config.DB.russian_roulette.find_one({"_id": inter.guild.id})

                    if len(new_data['joined']) >= 2:
                        await self.bot.config.DB.russian_roulette.update_one({"_id": inter.guild.id}, {"$set": {"started_or_not": True}})
                        await inter.send(f"Игра начата! Ходите, {inter.guild.get_member(int(new_data['joined'][0])).mention}. Чтобы сделать ход, пропишите 'Выстрел'")
            
            else:
                raise CustomError("Сейчас уже идёт игра, подождите, пока игра закончится!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.bot.config.DB.russian_roulette.count_documents({"_id": message.guild.id}) != 0:
            data = await self.bot.config.DB.russian_roulette.find_one({"_id": message.guild.id})
            if message.author.id in data['joined']:
                if message.author.id == data['step'][0]:
                    if data['started_or_not']:
                        if message.content.lower() == "выстрел":
                            rand = randint(1, 2)
                            for i in range(1, len(data['joined'])):
                                if len(data['joined']) > 1:
                                    await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$set": {"step": [data['joined'][i]]}})
                                    member = message.guild.get_member(int(data['joined'][i]))
                                else:
                                    await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$set": {"step": [data['joined'][0]]}})
                                    member = message.guild.get_member(int(data['joined'][0]))

                                if rand == 1:
                                    await message.channel.send(f'Тебе повезло :). Следующий: {member.mention}')
                                else:
                                    await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$pull": {"joined": message.author.id, "step": message.author.id}})
                                    await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$set": {"step": [data['joined'][1 if len(data['joined']) > 1 else 0]]}})
                                    if len(data['joined']) == 1:
                                        await message.channel.send(f"А {member.mention} везунчик.. Ты победил(-а)!")
                                        await self.bot.config.DB.russian_roulette.delete_one({"_id": message.guild.id})
                                    else:
                                        await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$pull": {"joined": message.author.id, "step": message.author.id}})
                                        await self.bot.config.DB.russian_roulette.update_one({"_id": message.guild.id}, {"$set": {"step": [data['joined'][1 if len(data['joined']) > 1 else 0]]}})
                                        await message.channel.send(f'Тебе не повезло, выбываешь. :(. Следующий: {member.mention}')

                        if int(data['start_time']) == int(datetime.datetime.now().strftime('%H%M'))+5:
                            await message.channel.send('Игра окончена. Время выбыло')
                            await self.bot.config.DB.russian_roulette.delete_one({"_id": message.guild.id})


def setup(bot):
    bot.add_cog(FunSlashCommands(bot))
