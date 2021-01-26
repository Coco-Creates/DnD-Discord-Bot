# bot.py
import os
import discord
import dddatabase
import ddparser
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


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
