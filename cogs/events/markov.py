import random

import disnake
from disnake.ext import commands


class Markov(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def generate(self, words):
        for i in range(len(words) - 1):
            yield (words[i], words[i + 1])

    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.bot.config.DB.markov.count_documents({"_id": message.guild.id}) == 0:
            return
        else:
            if message.author.bot:
                return

            if dict(await self.bot.config.DB.markov.find_one({"_id": message.guild.id}))['channel'] != message.channel.id:
                return

            words = [i.content async for i in random.choice(message.guild.text_channels).history() if not i.author.bot and self.bot.uptime.timestamp() < message.created_at.timestamp()]
            data = await self.bot.config.DB.markov.find_one({"_id": message.guild.id})

            word_dict = {}
            for word_1, word_2 in self.generate(words):
                if word_1 in word_dict.keys():
                    word_dict[word_1].append(word_2)
                else:
                    word_dict[word_1] = [word_2]

            first_word = random.choice(words)
            n_words = 30
            chain = [first_word]

            for _ in range(n_words):
                if len(''.join(chain)) <= 200:
                    chain.append(random.choice(word_dict[chain[-1]]))

            await self.bot.get_channel(data['channel']).send(' '.join(chain))

def setup(bot):
    bot.add_cog(Markov(bot))
