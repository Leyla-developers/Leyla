from justify.cog import JustifyCog


class LeylaJustify(JustifyCog):

    hidden = True
    ...

def setup(bot):
    bot.add_cog(LeylaJustify(bot))
