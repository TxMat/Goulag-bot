import discord
import asyncio
from keep_live import keep_live
from time import sleep, time
from json import load as json_load
from random import randrange
from random import randint
import time

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
log = False
me = 0
ids = 0
idmute = 0
mute = False
idbck = 0
meid = 0
memid = 0
waitrep = False

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
    idmute = args[0]
    try:
        idmute = int(args[0])
    except:
        if idmute == 'all':
            muted = []
            return
        await message.add_reaction("👌")
    finally:
        if idmute not in muted and idmute != 'all':
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


def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
        else:
          return True
    return inner_check


async def helpp(message, *args):
    mem = message.author
    await mem.create_dm()
    await mem.dm_channel.send(
        "__**command list:**__ \n\n**option prefix :** permet de changer le préfix du bot (& par défaut)\n\n**help :** envoie ce message à l'utilisateur qui effectue la commande\n\n**option emoji :** l'emoji avec le quel le bot réagit quand une personne fait <préfix>help (par défaut : :ok_hand:)\n\n**create :** va creer une commande (le nom doit etre contenu en un mot &create vive hitler ne va pas marcher utilisez create vive_hitler a la place)\n\n**add :** ajoute un phrase qui sera choisie aleatoirement a chaque appel de la commande custom (utilisation &add <name> <phrase>)\n\n**option role :** nom du role qu'un membre doit posséder pour modifier les differents parametres (`modifier` par défaut)\n\n**remove :** supprime une commande sans confirmation (ouais je vais changer ca tkt)\n\n**list :** envoie la liste des toutes les commandes custom (recommandé pour les sauvegarder)\n\n**clear :** supprime toutes les commandes custom du serveur\n\n ```note : il vous faut la permission `gerer le serveur` ou le role defini par <role> pour parametrer le bot (mais pas pour ajouter des commandes ouais c'est pt je vais changer tkt)```\n\n`Une question/sugestion? contactez mon devloppeur : `<@259676097652719616>` :)`\n\n*Ver : BETA0.7*"
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
        await message.add_reaction(no)
        return
    CustomStrings[args[0]].append(" ".join(args[1:]))
    print(CustomStrings)
    print(CustomStrings[args[0]])
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
    return


async def listt(message, *args):
    mss = ""
    for i in CustomStrings.keys():
        mss = mss + "**" + i + " :" + "**" + "\n\n"
        for j in CustomStrings[i]:
            print(j)
            mss = mss + " - " + j + "\n"
        mss = mss + "\n\n" + "------------------------------------------------" + "\n\n"
    await message.author.create_dm()
    await message.author.dm_channel.send(mss)
    return


async def custom(message, *args):
    print(args)
    if args[0] not in custom_cmd:
        return
    tot = len(CustomStrings[args[0]])
    rand = randrange(tot)
    await message.channel.send((CustomStrings[args[0]][rand]))


async def clearr(message, *args):
  global custom_cmd
  global CustomStrings
  await message.channel.send("ATTENTION CETTE COMMANDE VA SUPPRIMER **TOUTES** VOS COMMANDES CUSTOMS")
  await message.channel.send("tape 'tkt je gère' pour effectuer la commande")
  await message.channel.send("(ps : t'a 10 sec pour te decider)")
  msg = await client.wait_for('message', check=check(message.author), timeout=10)
  if msg.content == "tkt je gère":
    custom_cmd = []
    CustomStrings = {}
    await message.channel.send("Reset effectué")
  else:
    await message.channel.send("Annulé")



async def removee(message, *args):
    if args[0] in custom_cmd:
        await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
        await message.channel.send(args[0] + " Supprimé(e) :c")
    else:
        await message.add_reaction(no)


actions = {
    "option": option,
    "desc": change_presence,
    "help": helpp,
    "mute": mutee,
    "say": sayy,
    "unmute": unmutee,
    "create": createe,
    "add": addd,
    "delete": removee,
    "list": listt,
    "clear" : clearr
}

perm_actions = ["option", "mute", "unmute"]
admin_actions = ["desc", "say"]

badwords = [
    "tg", "ntm", "pd", "fdp", "suce", "ftg", "salope", "encule", "enculé", "connard", "pute"
]

reponses = [
  "tu veux quoi enculé ?", "il y a un probleme fils de pute ?", "redis ca encore une fois je baise ta mere", "et ta soeur fdp ?", "nique tes morts non ?", "je te retoune le compliment fdp", "t'a pas autre chose a faire qu'insulter un bot en mp qui te reponds avec des reponses pré-enregistrés ?", "1v1 gare du nord enculé", "no u", "toi je note ton nom fait gaffe a ton cul la prochaine fois que tu join un voc", "parle mieux pd"
]

react = [
  "wtf", "omg", "wow", "mdr", "xd", "hahaha", "😂", "😂😂", "😂😂😂"
]

rep2 = [
  "on fait moins le malin mtn hein ?", "alors ca t'a calmé ?", "je prefere cette ambiance", "ouais ouais mefie toi je t'ai a l'oeil"
]

quoi = ["quoi", "quoi?", "quoi ?"]

muted = []
custom_cmd = []
CustomStrings = {}


@client.event
async def on_message(message):
    if message.author.id == 408785106942164992 or  message.author.id == 259676097652719616:
      a = message.content[0:].split(" ")
      if a[0] == "**⚠️":
        print(a)
        user = await client.fetch_user(259676097652719616)
        await client.wait_until_ready()
        await user.create_dm()
        for i in range (10):
          await message.channel.send(user.mention)
          await user.dm_channel.send("OWO CAPTCHA EMERGENCY")
    if type(message.channel) != discord.TextChannel:
        global waitrep
        if message.author.id == 838037358854012938:
            return
        if waitrep:
          if message.content.lower() in react:
            nb = randint(0, len(rep2))
            await message.author.dm_channel.send(rep2[nb])
          waitrep = False
        if message.content.lower() in badwords:
            if message.author.id == 328521363180748801:
                log = "insult in dm :", message.content
                print(log)
                log = "by :", message.author
                print(log)
                return
            nb = randint(0, len(reponses)-1)
            await message.author.dm_channel.send(reponses[nb])
            waitrep = True
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
            return
        if a[0] in custom_cmd:
            await custom(message, *a[0:])
        else:
            await actions[a[0]](message, *a[1:])
        log = "executing command:", message.content, "by :", message.author
        print(log)
    if message.content.lower() in quoi:
      await message.channel.send("https://cdn.discordapp.com/attachments/691609589036220486/871044378691530793/FEUR.mp4")
      return


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


keep_live()
client.run(CONFIG["token"])
