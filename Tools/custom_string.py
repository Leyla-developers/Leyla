from string import Template
from update_changer import updated_username


class MyTemplate(Template):
    delimiter = '['
    pattern = r'''\[(?:(?P<escaped>\[) | (?P<named>[_a-z][_a-z0-9]*)\] | (?P<braced>[_a-z][_a-z0-9]*)\] | (?P<invalid>))'''


def welcome_function(member, message):
    variables = {
        'memberMention': member.mention,
        'guildMembers': str(len(member.guild.members)),
        'guild': member.guild.name,
        'member': updated_username(member)
    }

    return MyTemplate(message).safe_substitute(variables)


async def level_string(bot, member):
    data = await bot.config.DB.levels.find_one({"guild": member.guild.id, "member": member.id})
    message = await bot.config.DB.levels.find_one({"_id": member.guild.id})
    variables = {
        'memberMention': member.mention,
        'member': updated_username(member),
        'lvl': str(data['lvl']),
        'xp': str(5*(data['lvl']**2)+50*data['lvl']+100)
    }

    return MyTemplate(message['message']).safe_substitute(variables)
