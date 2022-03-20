from disnake.ext import commands


class CustomError(commands.CommandError):

    def __init__(self, args):
        self.args = args
        super().__init__(args)

class NotLoggedIn(commands.CommandError):
     
    def __init__(self):
        super().__init__()

class DataNotPublic(commands.CommandError):
     
    def __init__(self):
        super().__init__()