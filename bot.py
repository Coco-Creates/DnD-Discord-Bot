# bot.py
import os
import discord
from discord import DMChannel
import dddatabase
import ddparser
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

rpsValues = {
    1: ':rock:',
    2: ':newspaper:',
    3: ':scissors:'
}
rpsDict = {}

@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guilds:'
    )

    for guild in client.guilds:
        print(
            f'{guild.name}(id: {guild.id})'
        )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.split(" ")

    if len(content) == 1:
        if content[0] == '!f' or content[0] == '!flip':
            ast = ddparser.parse(message.author, '1d2')
            result = ddparser.compute(ast)
            if result == 1:
                await message.channel.send(':heads:')
            else:
                await message.channel.send(':tails:')
        if content[0] == '!rps' and type(message.channel) is not DMChannel:
            if message.channel.guild.id in rpsDict:
                ast = ddparser.parse(message.author, '1d3')
                result1 = ddparser.compute(ast)
                result2 = ddparser.compute(ast)
                output = rpsDict[message.channel.guild.id] + ' ' + rpsValues[result1] + ' vs '
                output += rpsValues[result2] + ' ' + message.author.name
                await message.channel.send(output)
                rpsDict.pop(message.channel.guild.id)
            else:
                rpsDict[message.channel.guild.id] = message.author.name

    if len(content) < 2:
        return

    output = ''

    if content[0] == '!r' or content[0] == '!roll':
        for x in range(1, len(content)):
            ast = ddparser.parse(message.author, content[x])
            result = ddparser.compute(ast)
            output += content[x] + ':' + str(result) + "  "
        await message.channel.send(output)

    if len(content) != 7:
        return

    if content[0] == '!s' or content[0] == '!stats':
        result = dddatabase.insert_character(message.author.id, content)
        if result == 0:
            await message.channel.send('Stats Saved')
        else:
            await message.channel.send('Stats Format Incorrect')

client.run(TOKEN)
