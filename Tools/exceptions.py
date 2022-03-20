from disnake.ext import commands


class CustomError(commands.CommandError):

    def __init__(self, args):
        self.args = args
        super().__init__(args)
