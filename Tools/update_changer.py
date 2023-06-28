import disnake
from disnake.ext import commands


def updated_username(user: disnake.User or disnake.Member):
    if user.discriminator == "0":
        return user.name
    else:
        return str(user)