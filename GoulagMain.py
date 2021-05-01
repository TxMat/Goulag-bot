import discord
import asyncio
# from keep_live import keep_live
from time import sleep, time
from json import load as json_load
from discord.utils import get
from random import randrange
print(discord.__version__)

with open("config.json") as f:
    CONFIG = json_load(f)

OPTIONS = {}
DEFAULT = {"prefix": "&", "emoji": "👌", "role": "modifier"}
global mute
global chat
global ids
global idmute
global me
no = '❌'
me = 0
ids = 0
idmute = 0
mute = False
idbck = 0
meid = 0
memid = 0

client = discord.Client()
CHANNELS = {}


async def option(message, var, value, *args):
    OPTIONS[message.guild.id][var] = type(
        OPTIONS[message.guild.id][var])(value)
    await message.add_reaction("👌")


async def change_presence(message, *args):
    await client.change_presence(
        activity=discord.Activity(
            name=" ".join(args), type=discord.ActivityType.playing))
    log = "desc change to :", " ".join(args)
    print(str(log))




async def mutee(message, *args):
    global idmute
    idmute = int(args[0])
    if idmute == 259676097652719616:
        await message.add_reaction("🤫")
        await message.author.create_dm()
        await message.author.dm_channel.send(message.content + "\n\n mdr non")
        return
    if idmute in muted:
        await message.add_reaction("❔")
        await message.author.create_dm()
        await message.author.dm_channel.send(
            str(idmute) + "is already muted", delete_after=100)
        log = idmute, "already muted"
        print(log)
    if idmute not in muted:
        muted.append(idmute)
        await message.add_reaction("🟢")
        log = idmute, "is now muted"
        print(log)
        return


async def unmutee(message, *args):
    
    global muted
    await client.get_user(259676097652719616).dm_channel.send(muted)
    idmute = args[0]
    try:
        idmute = int(args[0])
    except:
        if idmute == 'all':
            muted = []
            return
        await message.add_reaction("👌")
    finally:
        if idmute not in muted:
            await message.add_reaction("❔")
            return
        if idmute in muted:
            muted.remove(idmute)
            await message.add_reaction("👌")
            return


async def sayy(message, *args):
    
    ch = int(args[0])
    mss = " ".join(args[1:])
    channel = client.get_channel(ch)
    await channel.send(mss)
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
    return


async def helpp(message, *args):
    mem = message.author
    await mem.create_dm()
    await mem.dm_channel.send(
        "xd"
    )
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])

async def createe(message, *args):
    if args[0] not in custom_cmd:
        custom_cmd.append(args[0])
        print(args[0] + " ajouté a la liste des commandes")
        CustomStrings[args[0]] = []
        print(custom_cmd)
        await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
    else:
        await message.add_reaction(no)
#    mss = " ".join(args[1:])
#    if mss != "":
#        await addd(message)

async def addd(message, *args):
    if args[0] not in custom_cmd:
        return
    CustomStrings[args[0]].append(" ".join(args[1:]))
    print(CustomStrings)
    print(CustomStrings[args[0]])
    return

async def custom(message, *args):
    print(args)
    if args[0] not in custom_cmd:
        return
    tot = len(CustomStrings[args[0]])
    rand = randrange(tot)
    await message.channel.send((CustomStrings[args[0]][rand]))

async def removee(message, *args):
    if args[0] in custom_cmd:
        await message.channel.send(args[0] + " Supprimée :c")
    else:
        await message.add_reaction(no)
actions = {
    "option": option,
    "desc": change_presence,
    "help": helpp,
    "mute": mutee,
    "say": sayy,
    "unmute": unmutee,
    "create" : createe,
    "add" : addd
}

perm_actions = ["option", "mute", "unmute"]
admin_actions = ["desc", "say"]
badwords = [
    "tg", "ntm","pd", "fdp","suce", "ftg"
]
muted = []
custom_cmd = []
CustomStrings = {}


@client.event
async def on_message(message):
    if type(message.channel) != discord.TextChannel:
        if message.author.id == 697343120433741947:
            return
        '''
        if len(message.content) and message.content[0] == "&":
            a = message.content[1:].split(" ")
            if a[0] not in actions:
                log = "wrong command:", message.content, "by :", message.author
                print(log)
                await message.add_reaction("❔")
                return
            if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
                log = "wrong permission to use command:", message.content, "by :", message.author
                print(log)
                await message.add_reaction("❌")
                return
            log = "executing command:", message.content, "by :", message.author
            print(log)
            await actions[a[0]](message, *a[1:])
        '''
        if message.content.lower() in badwords:
            if message.author.id == 328521363180748801:
                log = "insult in dm :", message.content
                print(log)
                log = "by :", message.author
                print(log)
                return
            await message.author.dm_channel.send(">:(")
            log = "insult in dm :", message.content
            print(log)
            log = "get trolled :", message.author
            print(log)
            return
        log = "dm ressage recived :", message.content
        print(log)
        log = "by :", message.author
        print(log)
        return
    if message.author.id in muted:
        await message.delete()
        return
    if len(message.content) and message.content[0] == OPTIONS[message.guild.id]["prefix"]:
        a = message.content[1:].split(" ")
        print(a[0])
        if a[0] not in actions and a[0] not in custom_cmd:
            log = "wrong command:", message.content, "by :", message.author
            print(log)
            await message.add_reaction("❔")
            return
        if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
            log = "wrong permission to use command:", message.content, "by :", message.author
            print(log)
            await message.add_reaction("❌")
            return
        if a[0] in perm_actions and (
                message.author.guild_permissions.manage_guild == False
                and OPTIONS[message.channel.guild.id]["role"] not in list(
                    map(lambda x: x.name, message.author.roles))):
            log = "no perms nice try ", message.author
            print(log)
            await message.add_reaction("❌")
            await client.get_user(259676097652719616).dm_channel.send(
                message.author.roles)
            return
        if a[0] in custom_cmd:
            await custom(message, *a[0:])
        else:
            await actions[a[0]](message, *a[1:])
        log = "executing command:", message.content, "by :", message.author
        print(log)


@client.event
async def on_ready():
    mute = False
    await change_presence(None, '&help | online and ready >:3')
    for server in client.guilds:
        OPTIONS[server.id] = dict(DEFAULT)
    print("**RESTART**")
    print('{} is online and ready'.format(client.user))


@client.event
async def on_guild_join(guild):
    OPTIONS[guild.id] = dict(DEFAULT)

# keep_live()
client.run(CONFIG["token"])
