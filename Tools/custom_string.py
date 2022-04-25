from string import Template

class MyTemplate(Template):
    delimiter = '['
    pattern = r'''
    \[(?:
    (?P<escaped>\[) |
    (?P<named>[_a-z][_a-z0-9]*)\] |
    (?P<braced>[_a-z][_a-z0-9]*)\] |
    (?P<invalid>)
    )
    '''

def welcome_function(member, message):
    variables = {
        'memberMention': member.mention,
        'guildMembers': str(len(member.guild.members)),
        'guild': member.guild.name,
        'member': str(member)
    }

    return MyTemplate(message).safe_substitute(variables)
