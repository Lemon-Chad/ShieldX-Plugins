import discord
from discord.ext import commands
from time import sleep
import asyncio
import json
from random import randint, choice
from math import ceil, floor
import os
import sys, traceback



allPl = []

try:
  with open('botdata.json','r') as f:
    bot = json.load(f)
except:
  with open('botdata.json','w+') as f:
    bot = {}
    json.dump(bot, f)
  with open('botdata.json','r') as f:
    bot = json.load(f)

with open('token.txt','r') as f:
  tk = f.read()

loadedPlugins = []

client = commands.Bot(command_prefix = 'sx.')
client.remove_command('help')

def remove_char(str, n):
  first_part = str[:n]
  last_part=str[n+1:]
  return first_part + last_part

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity = discord.Game('sx.help | Join the discord with sx.joinDiscord'))
  print('yo wassup')
  print(discord.__version__)


@client.event
async def on_message(message):

  with open('botdata.json','w') as f:
    json.dump(bot,f)
    
  author = message.author
  content = message.content
  channel = message.channel
  guild = message.guild
  
  try:
    bot[str(guild.id)]
  except:
    bot[str(guild.id)] = {'loadedPlugins':{'ids':[]},'achievements':{'ids':[]},'shop':{"categories":[],"ids":[]},'teams':{},'teamids':[],'pointemoji':':cyclone:','bitemoji':':beginner:'}
  try:
    bot[str(guild.id)]['loadedPlugins']
  except:
    bot[str(guild.id)]['loadedPlugins'] = {'ids':[]}
  try:
    receiver = bot[str(guild.id)][str(author.id)]
  except:
    bot[str(guild.id)][str(author.id)] = {}
    receiver = bot[str(guild.id)][str(author.id)]  
  try:
      receiver['xp']
  except:
      receiver['xp'] = 0
      receiver['level'] = 1
      receiver['bits'] = 0
  try:
      receiver['team']
  except:
      receiver['team'] = 'None'
  try:
    receiver['inventory']
  except:
    receiver['inventory'] = {'consumables':{},'items':{},'ids':[]}
  try:
    receiver['aids']
  except:
    receiver['aids'] = []
    receiver['achievements']={}
  for i in range(len(receiver['aids'])):
    if receiver['aids'][i] not in bot[str(guild.id)]['achievements']['ids']:
      aid = receiver['aids'][i]
      del receiver['achievements'][aid]
      receiver['aids'].remove(aid)
  for i in range(len(bot[str(guild.id)]['achievements']['ids'])):
    aid=bot[str(guild.id)]['achievements']['ids'][i]
    aidd=bot[str(guild.id)]['achievements'][aid]
    if bot[str(guild.id)]['achievements']['ids'][i] not in receiver['aids']:
      receiver['aids'].append(aid)
      receiver['achievements'][aid] = {'goal':aidd['goal'],'progress':0}
  for i in range(len(receiver['aids'])):
    aid=bot[str(guild.id)]['achievements']['ids'][i]
    aidd=bot[str(guild.id)]['achievements'][aid]
    if aidd['action'] == 'sendMessages':
      receiver['achievements'][aid]['progress'] += 1
    if aidd['action'] == 'sendCustomMessage' and content == aidd['subaction']:
      receiver['achievements'][aid]['progress'] += 1
  
  #V  Achievement Reward  V
  
  for i in range(len(receiver['aids'])):
    aid=bot[str(guild.id)]['achievements']['ids'][i]
    aidd=bot[str(guild.id)]['achievements'][aid]
    if receiver['achievements'][aid]['progress'] == receiver['achievements'][aid]['goal']:
      if aidd['reward'] != "dummy":
        await channel.send("You completed the achievement, \""+aid+"!\"")
      else:
        for x in range(len(receiver['aids'])):
          aidb = bot[str(guild.id)]['achievements']['ids'][x]
          aiddb = bot[str(guild.id)]['achievements'][aidb]
          if aiddb['action'] == 'achievements' and aiddb['subaction'] == aidd['title']:
            receiver['achievements'][aidb]['progress'] += 1
      if aidd['reward'] == "bits":
        receiver["bits"] += aidd['rewardcount']
        await channel.send('You earned '+bot[str(guild.id)]['bitemoji']+str(aidd['rewardcount'])+'!')
      elif aidd['reward'] == "points":
        team =receiver['team']
        bot[str(guild.id)]['teams'][team]['points']+= aidd['rewardcount']
        await channel.send('You earned '+bot[str(guild.id)]['pointemoji']+str(aidd['rewardcount'])+' for your team! ('+receiver['team']+')')
      elif aidd['reward'] == "item":
        item = aidd['title']
        try:
          if isinstance(receiver['inventory']['items'][item],int):
            receiver['inventory']['items'][item] += aidd['rewardcount']
          else:
            receiver['inventory']['items'][item]["count"] += aidd['rewardcount']
        except:
          receiver['inventory']['items'][item] = {"count":aidd['rewardcount'],"category":"none"}
          receiver['inventory']['ids'].append(item)
        if aidd['rewardcount'] == 1:
          await channel.send('You received '+str(aidd['rewardcount'])+' '+aidd['title']+'.')
        elif aidd['rewardcount'] > 1:
          await channel.send('You received '+str(aidd['rewardcount'])+' '+aidd['title']+'s.')
      elif aidd['reward'] == "role":
        item = aidd['title']
        try:
          if isinstance(receiver['inventory']['items'][item],int):
            receiver['inventory']['items'][item] += aidd['rewardcount']
          else:
            receiver['inventory']['items'][item]["count"] += aidd['rewardcount']
        except:
          receiver['inventory']['items'][item] = {"count":aidd['rewardcount'],"category":"none"}
          receiver['inventory']['ids'].append(item)
          receiver['inventory']['consumables'][item] = 'role'
        await channel.send('You received the role '+aidd['title']+', check your inventory.')
      receiver['achievements'][aid]['progress']+=1
        
      
  try:
    receiver['team']
    try:
      receiver['xp'] += randint(2,5)
      lvl_limit = (receiver['level']-1)*50+100
      if receiver['xp'] >= lvl_limit:
        receiver['level'] += 1
        receiver['xp'] -= lvl_limit
        if receiver['team'] != 'None':
          team = receiver['team']
          bot[str(guild.id)]['teams'][team]['points'] += 1
          await channel.send('You generated '+bot[str(guild.id)]['pointemoji']+'1 for your team! ('+receiver['team']+')')
          bitrate = 20*bot[str(guild.id)]['teams'][team]['points']
          receiver['bits'] += bitrate
          await channel.send('You earned '+bot[str(guild.id)]['bitemoji']+str(bitrate)+' from your team!')
        else:
          receiver['bits'] += 5
          await channel.send('You earned '+bot[str(guild.id)]['bitemoji']+'5!')
    except:
      receiver['xp'] = randint(2,5)
      receiver['level'] = 1
      receiver['team'] = 'None'
      receiver['bits'] = 0
      receiver['inventory'] = {'items':{},'ids':[]}
  except:
    ...
  
  for i in range(len(receiver['inventory']['ids'])):
    itemid = receiver["inventory"]["ids"][i]
    item = receiver["inventory"]['items'][itemid]
    if isinstance(item,int):
      if item < 1:
        receiver['inventory']["ids"].remove(itemid)
        del receiver['inventory'][itemid]
        if itemid in receiver['inventory']['consumables']:
          del receiver['consumables'][itemid]
    else:
      if item["count"] < 1:
        receiver['inventory']["ids"].remove(itemid)
        del receiver['inventory'][itemid]
        if itemid in receiver['inventory']['consumables']:
          del receiver['consumables'][itemid]
  
  with open('botdata.json','w') as f:
    json.dump(bot,f)
  
  await client.process_commands(message)

@client.command()
async def joinDiscord(ctx):
  await ctx.send("https://discord.gg/vknnSUw")

@client.command()
async def help(ctx):
  embed=discord.Embed(title="Help", color=0xf06000)
  embed.add_field(name="Teams", value="**join** - Joins specified team. If team doesn't exist, specified team will be created.\n\n**teams** - Lists all the teams and their points\n\n**stats** *<team-name\>* - Shows stats of the specified team.", inline=False)
  embed.add_field(name="Player", value="**stats** - Shows you your current stats.\n\n**inventory** - Shows you your current inventory.\n\n**use** *<id\>* - Use the object specified (If it has a usable ability).\n\n**reset** - Resets your data on the server.", inline=False)
  embed.add_field(name="Shop", value="**shop** - Shows you the current shop\n\n**shop** *<item-name\>* - Buys item specified.", inline=False)
  embed.add_field(name="How to get Points and Bits", value="Points are given to your team every time you level up. You gain xp from chatting. Whenever you level up, you will also be given bits. If you are not part of a team, you will be given 5 bits. If you are part of a team, you will get a boost based on how many points your team has! 1 Point = 20 Bits",inline=False)
  embed.set_footer(text="Prefix is sx. Admin commands are sx.adminHelp")
  await ctx.send(embed=embed)

@client.command(pass_context=True)
async def use(ctx, *args):
  selecteditem = ''
  for word in args:
    selecteditem+=word
    selecteditem+=' '
  selecteditem = selecteditem[:-1]
  user = ctx.message.author
  receiver = bot[str(ctx.guild.id)][str(user.id)]
  if selecteditem in receiver['inventory']['ids']:
    item = receiver['inventory']['items'][selecteditem]
    if selecteditem in receiver['inventory']['consumables']:
      if receiver['inventory']['consumables'][selecteditem] == 'role':
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name=selecteditem)
        await user.add_roles(role)
      if isinstance(receiver['inventory']['items'][selecteditem],int):
        receiver['inventory']['items'][selecteditem] -= 1
        await ctx.send("Used "+selecteditem+". You have "+str(receiver['inventory']['items'][selecteditem])+" left.")
      else:
        receiver['inventory']['items'][selecteditem]["count"] -= 1
        await ctx.send("Used "+selecteditem+". You have "+str(receiver['inventory']['items'][selecteditem]["count"])+" left.")

@client.command()
@commands.has_permissions(administrator=True)
async def loadPlugin(ctx, extension):
  if extension in allPl:
    await ctx.send(f"Loaded {extension}!")
    bot[str(ctx.guild.id)]['loadedPlugins']["ids"].append(extension)
  else:
    await ctx.send("Invalid plugin")

@client.command()
@commands.has_permissions(administrator=True)
async def unloadPlugin(ctx, extension):
  if extension in bot[str(ctx.guild.id)]['loadedPlugins']["ids"]:
    await ctx.send(f"Unloaded {extension}!")
    bot[str(ctx.guild.id)]['loadedPlugins']["ids"].remove(extension)
    del bot[str(ctx.guild.id)]['loadedPlugins'][extension]
  else:
    await ctx.send("Plugin not loaded")

for filename in os.listdir('./plugins'):
  if filename.endswith('.py'):
    client.load_extension(f'plugins.{filename[:-3]}')
    allPl.append(f'{filename[:-3]}')

@client.command(pass_context=True)
async def plugins(ctx):
  user = ctx.message.author
  receiver = bot[str(ctx.guild.id)][str(user.id)]
  lis = ''
  for i in range(len(bot[str(ctx.guild.id)]['loadedPlugins']["ids"])):
      pl = bot[str(ctx.guild.id)]['loadedPlugins']["ids"][i]
      lis += "- **"+pl+'**\n\n'
  listpl = discord.Embed(
      title = '**Plugins**',
      descriptiom = '',
      colour=0xfa9d21
  )
  if lis != '':
        listpl.add_field(name='** **',value=str(lis),inline=True)
        await ctx.send(embed=listpl)
  else:
      listpl.add_field(name='** **',value='There are no plugins :spider_web:',inline=True)
      await ctx.send(embed=listpl)


@client.command()
@commands.has_permissions(administrator=True)
async def adminHelp(ctx):
  embed=discord.Embed(title="Admin Help", color=0xf06000)
  embed.add_field(name="Admin Commands", value="**vibeCheck** - Tells if you are an admin or not\n\n**manageShop** *< add|remove|sort\> <item\> <category\> <cost\> <limited\> <count\> <description\>* - Adds an item with the specified name into a hidden category (Used for achievements). It will also cost as much as specified. Limited changes wether you can only but it once or not. The count is how much of the item you will get upon purchase. You can also remove an item with the specified name. Sort allows you to add items into more categories.\n\n**pointEmoji** *<emoji\>* - Changes the emoji for points to the one specified.\n\n", inline=False)
  embed.add_field(name="** **",value="**bitEmoji** *<emoji\>* - Changes the emoji for bits to the one specified.\n\n**manageAchievements** *<add|remove\> <id\> <buy|sendMessages|sendCustomMessage|achievements\> <subaction\> <goal\> <bits|item|role|dummy\> <title\> <count\> <description\>* - Adds an achievement with specified name and action chosen. Subaction is applied for actions that require more specification. For the action *buy* it's the item category. For the action *sendCustomMessage* it's the custom message. For the action *achievements* it's the achievement group. Next is the goal of how many times you want the action to be executed.",inline=False)
  embed.add_field(name="** **",value=" After that is the reward for the achievement. You can choose between rewarding bits, a custom role, or a custom item, and the title is the name of the custom role/item. If you set the reward to dummy, there will be no message for completing the achievement, and the title will be the achievement group. The count is the amount of the reward the player will get. You can also remove an achievement with the specified name.\n\n**displayNames** *<shop|achievements\> <id\> <displayName\>* - Allows you to change the name of an item or achievement to add spaces or just change the name in general.\n\n**serverReset** - Resets all server data\n\n**plugins** - lists all the enabled server plugins.\n\n**loadPlugin** *<plugin\>* - loads a plugin.\n\n**unloadPlugin** *<plugin\>* - unloads a loaded plugin.",inline=False)
  embed.set_footer(text="Prefix is sx. Normal commands are sx.help\n\n")
  await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def serverReset(ctx):
  del bot[str(ctx.guild.id)]
  await ctx.send(":soap: Server data wiped! :soap:")

@client.command(pass_context=True)
async def reset(ctx):
  user = ctx.message.author
  del bot[str(ctx.guild.id)][str(user.id)]
  await ctx.send(":soap: User data wiped! :soap:")

@client.command(pass_context=True)
async def join(ctx, team=''):
  user = ctx.message.author
  receiver = bot[str(ctx.guild.id)][str(user.id)]
  receiver['team'] = team
  try:
    bot[str(ctx.guild.id)]['teams'][team]
    await ctx.send('Joined, \"'+str(team)+'\"')
  except:
    bot[str(ctx.guild.id)]['teams'][team] = {'points':0}
    bot[str(ctx.guild.id)]['teamids'].append(team)
    await ctx.send('Created and joined, \"'+str(team)+'\"')

@client.command()
async def teams(ctx):
  
  lis = ''
  for i in range(len(bot[str(ctx.guild.id)]["teamids"])):
    ct = bot[str(ctx.guild.id)]["teamids"][i]
    lis += ct+' | Points: '+bot[str(ctx.guild.id)]['pointemoji']+str(bot[str(ctx.guild.id)]['teams'][ct]['points'])+'\n\n'
  tm = discord.Embed(
    title = '**Teams**',
    descriptiom = '',
    colour=0xfa9d21
  )
  tm.add_field(name='** **',value=str(lis),inline=True)
  await ctx.send(embed=tm)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=25):
  
  channel = ctx.message.channel
  await channel.purge(limit=amount)

@client.command(pass_context=True)
async def inventory(ctx):
  user = ctx.message.author
  r = bot[str(ctx.guild.id)][str(user.id)]
  try:
    r['inventory']
  except:
    r['inventory'] = {'items':{},'ids':[]}
  inv = r['inventory']
  lis = ''
  for i in range(len(inv["ids"])):
      itemid = inv["ids"][i]
      item = inv['items'][itemid]
      if itemid in r['inventory']['consumables']:
        if r['inventory']['consumables'][itemid] == 'role':
          consumetag = " | Use to earn a role!"
        else:
          consumetag = " | "+r['inventory']['consumables'][itemid]
      else:
        consumetag = ""
      if item == 1:
        lis += itemid+consumetag+'\n\n'
      else:
        if isinstance(item,int): 
          lis += itemid+consumetag+' | Count: '+str(item)+'\n\n'
        else:
          lis += itemid+consumetag+' | Count: '+str(item["count"])+'\n\n'
  inventory = discord.Embed(
      title = '**Inventory**',
      descriptiom = '',
      colour=0xfa9d21
  )
  if lis != '':
        inventory.add_field(name='** **',value=str(lis),inline=True)
        await ctx.send(embed=inventory)
  else:
      inventory.add_field(name='** **',value='Your inventory is empty :spider_web:',inline=True)
      await ctx.send(embed=inventory)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def getData(ctx,password=0):
  if password == 78295701923012488305934853040218520204593489537589628971908470349502043:
    with open('bot.json','w+') as f:
      json.dump(bot,f)
      await ctx.author.send(file=discord.File(open('botdata.json','r'),'botdata.json'))
    '''botmsg = str(bot)
    x = int(len(botmsg)/1999)
    if len(botmsg)/1999 > x:
      x+=1

    for i in range(x):
      await ctx.author.send(botmsg[:1999])
      botmsg = botmsg[1999:]'''

@client.command(pass_context=True)
async def achievements(ctx):
  user = ctx.message.author
  receiver = bot[str(ctx.guild.id)][str(user.id)]
  lis = ''
  for i in range(len(bot[str(ctx.guild.id)]['achievements']["ids"])):
      aid = bot[str(ctx.guild.id)]['achievements']["ids"][i]
      aidd = bot[str(ctx.guild.id)]['achievements'][aid]
      if aidd['reward'] != "dummy":
        lis += "**"+aid+'**\n'+str(aidd['description'])+'\n\n'
  shop = discord.Embed(
      title = '**Achievements**',
      descriptiom = '',
      colour=0xfa9d21
  )
  if lis != '':
        shop.add_field(name='** **',value=str(lis),inline=True)
        await ctx.send(embed=shop)
  else:
      shop.add_field(name='** **',value='There are no achievements :spider_web:',inline=True)
      await ctx.send(embed=shop)

@client.command(pass_context=True)
async def shop(ctx, *args):
  user = ctx.message.author
  receiver = bot[str(ctx.guild.id)][str(user.id)]
  try:
    receiver['bits']
  except:
    receiver['bits'] = 0
  item = ''
  for word in args:
    item += word
    item += ' '
  item = item[:-1]
  if item=='':
    lis = ''
    for i in range(len(bot[str(ctx.guild.id)]['shop']["ids"])):
      itemid = bot[str(ctx.guild.id)]['shop']["ids"][i]
      item = bot[str(ctx.guild.id)]['shop'][itemid]
      lis += "**"+itemid+'** | Cost: '+bot[str(ctx.guild.id)]['bitemoji']+str(item['cost'])+'\n'+str(item['description'])+'\n\n'
    shop = discord.Embed(
      title = '**Shop**',
      descriptiom = '',
      colour=0xfa9d21
    )
    if lis != '':
        shop.add_field(name='** **',value=str(lis),inline=True)
        await ctx.send(embed=shop)
    else:
      shop.add_field(name='** **',value='The shop is empty :spider_web:',inline=True)
      await ctx.send(embed=shop)
  elif item in bot[str(ctx.guild.id)]["shop"]["ids"]:
    if receiver['bits'] >= bot[str(ctx.guild.id)]["shop"][item]["cost"]:
      if bot[str(ctx.guild.id)]["shop"][item]["limited"] == True and item in receiver["inventory"]["ids"]:
        await ctx.send('You cannot own anymore of this item!')
      else:
        receiver['bits'] -= bot[str(ctx.guild.id)]["shop"][item]["cost"]
        await ctx.send('Bought 1 '+item+'.')
        for i in range(len(bot[str(ctx.guild.id)]['shop'][item]['category'])):
          cat = bot[str(ctx.guild.id)]['shop'][item]['category'][i]
          for i in range(len(bot[str(ctx.guild.id)]['achievements']['ids'])):
            aid = bot[str(ctx.guild.id)]['achievements']['ids'][i]
            aidd = bot[str(ctx.guild.id)]['achievements'][aid]
            if aidd['action'] == 'buy' and cat in aidd['subaction']:
              receiver['achievements'][aid]['progress']+=1          
        try:
          if isinstance(receiver['inventory']['items'][item], int):
            receiver['inventory']['items'][item] += bot[str(ctx.guild.id)]["shop"][item]["count"]
          else:
            receiver['inventory']['items'][item]["count"] += bot[str(ctx.guild.id)]["shop"][item]["count"]
        except:
          receiver['inventory']['items'][item] = {"count":bot[str(ctx.guild.id)]["shop"][item]["count"],"category":bot[str(ctx.guild.id)]["shop"][item]["category"]}
          receiver['inventory']['ids'].append(item)
    else:
      await ctx.send('Insufficient funds.')

@client.command()
@commands.has_permissions(administrator=True)
async def vibeCheck(ctx):
  await ctx.send('Access verified!')

@client.command()
@commands.has_permissions(administrator=True)
async def infiniteBits(ctx):
  receiever = bot[str(ctx.guild.id)][str(ctx.message.author.id)]
  receiever["bits"] = 999999
  with open('botdata.json','w') as f:
    json.dump(bot,f)

@client.command()
@commands.has_permissions(administrator=True)
async def manageShop(ctx, arc, id, category='None', cost=100, lim=False, count=1, *args):
  if arc == 'add':
    if lim == True or lim == False:
      bot[str(ctx.guild.id)]['shop']["ids"].append(id)
      bot[str(ctx.guild.id)]['shop']['categories'].append(category)
      desc = ''
      for word in args:
        desc += word
        desc += ' '
      bot[str(ctx.guild.id)]['shop'][id] = {'cost':cost,'description':desc,'category':[],'limited':lim,'count':count}
      bot[str(ctx.guild.id)]['shop'][id]['category'].append(category)
      await ctx.send('Added item, \"'+id+'\"')
  elif arc == 'remove':
    del bot[str(ctx.guild.id)]['shop'][id]
    bot[str(ctx.guild.id)]['shop']["ids"].remove(id)
    await ctx.send('Removed item, \"'+id+'\"')
  elif arc == 'sort' and id in bot[str(ctx.guild.id)]['shop']['ids']:
    bot[str(ctx.guild.id)]['shop'][id]['category'].append(category)
    if category not in bot[str(ctx.guild.id)]['shop']['categories']:
      bot[str(ctx.guild.id)]['shop']['categories'].append(category)
    await ctx.send('Added item, \"'+id+',\" to category, \"'+category+'.\"')
  
@client.command()
@commands.has_permissions(administrator=True)
async def pointEmoji(ctx, emoji=':cyclone:'):
  if emoji != bot[str(ctx.guild.id)]['pointemoji']:
    bot[str(ctx.guild.id)]['pointemoji'] = emoji
    await ctx.send('Changed Points to '+emoji)
    
@client.command()
@commands.has_permissions(administrator=True)
async def bitEmoji(ctx, emoji=':beginner:'):
  if emoji != bot[str(ctx.guild.id)]['bitemoji']:
    bot[str(ctx.guild.id)]['bitemoji'] = emoji
    await ctx.send('Changed Bits to '+emoji)

@client.command(pass_context=True)
async def stats(ctx, team=''):
  user = ctx.message.author
  r = bot[str(ctx.guild.id)][str(user.id)]
  if team != '':
    try:
      pnts = bot[str(ctx.guild.id)]['teams'][team]['points']
      stats = discord.Embed(
      title = '**Stats**',
      descriptiom = '',
      colour=0xfa9d21
      )
      stats.add_field(name='Team',value=str(team),inline=True)
      stats.add_field(name='Points',value=bot[str(ctx.guild.id)]['pointemoji']+str(pnts),inline=True)
      await ctx.send(embed=stats)
    except:
      await ctx.send('Please enter a valid team name!')
  else:
    try:
      r['xp']
    except:
      r['xp'] = 0
      r['level'] = 1
      r['bits'] = 0
    try:
      r['team']
    except:
      r['team'] = 'None'
    lvl_limit = (r['level']-1)*50+100
    stats = discord.Embed(
      title = '**Stats**',
      descriptiom = '',
      colour=0xfa9d21
    )
    stats.add_field(name='Level',value=str(r['level']),inline=True)
    stats.add_field(name='XP',value=str(r['xp'])+'/'+str(lvl_limit),inline=True)
    stats.add_field(name='Team',value=str(r['team']),inline=True)
    stats.add_field(name='Bits',value=bot[str(ctx.guild.id)]['bitemoji']+str(r['bits']),inline=False)
    await ctx.send(embed=stats)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def manageAchievements(ctx, ar, id, action='', subaction='', goal=10, bi='bits', title='', count=10, *args):
  if ar == 'add' and action != '' and subaction != '':
    if action == 'buy' and subaction in bot[str(ctx.guild.id)]['shop']['categories']:
      if bi == 'role' or bi == 'item' or bi == 'bits' or bi == 'points' or bi == 'dummy':
        bot[str(ctx.guild.id)]['achievements']['ids'].append(id)
        desc = ''
        for word in args:
          desc += word
          desc += ' '
        bot[str(ctx.guild.id)]['achievements'][id] = {'action':action,'subaction':subaction,'goal':goal,'description':desc,'reward':bi,'title':title,'rewardcount':count}
        if bi == 'role':
          guild = ctx.guild
          await guild.create_role(name=title)
        await ctx.send('Created achievement, \"'+id+'.\"')
    elif action == 'sendCustomMessage':
      if bi == 'role' or bi == 'item' or bi == 'bits' or bi == 'points' or bi == 'dummy':
        bot[str(ctx.guild.id)]['achievements']['ids'].append(id)
        desc = ''
        for word in args:
          desc += word
          desc += ' '
        bot[str(ctx.guild.id)]['achievements'][id] = {'action':action,'subaction':subaction,'goal':goal,'description':desc,'reward':bi,'title':title,'rewardcount':count}
        if bi == 'role':
          guild = ctx.guild
          await guild.create_role(name=title)
        await ctx.send('Created achievement, \"'+id+'.\"')
    elif action == 'sendMessages':
      if bi == 'role' or bi == 'item' or bi == 'bits' or bi == 'points' or bi == 'dummy':
        bot[str(ctx.guild.id)]['achievements']['ids'].append(id)
        desc = ''
        for word in args:
          desc += word
          desc += ' '
        bot[str(ctx.guild.id)]['achievements'][id] = {'action':action,'subaction':subaction,'goal':goal,'description':desc,'reward':bi,'title':title,'rewardcount':count}
        if bi == 'role':
          guild = ctx.guild
          await guild.create_role(name=title)
        await ctx.send('Created achievement, \"'+id+'.\"')
    elif action == 'achievements':
      if bi == 'role' or bi == 'item' or bi == 'bits' or bi == 'points' or bi == 'dummy':
        bot[str(ctx.guild.id)]['achievements']['ids'].append(id)
        desc = ''
        for word in args:
          desc += word
          desc += ' '
        bot[str(ctx.guild.id)]['achievements'][id] = {'action':action,'subaction':subaction,'goal':goal,'description':desc,'reward':bi,'title':title,'rewardcount':count}
        if bi == 'role':
          guild = ctx.guild
          await guild.create_role(name=title)
        await ctx.send('Created achievement, \"'+id+'.\"')
    elif action == 'custom':
      if bi == 'role' or bi == 'item' or bi == 'bits' or bi == 'points' or bi == 'dummy':
        bot[str(ctx.guild.id)]['achievements']['ids'].append(id)
        desc = ''
        for word in args:
          desc += word
          desc += ' '
        bot[str(ctx.guild.id)]['achievements'][id] = {'action':action,'subaction':subaction,'goal':goal,'description':desc,'reward':bi,'title':title,'rewardcount':count}
        if bi == 'role':
          guild = ctx.guild
          await guild.create_role(name=title)
        await ctx.send('Created achievement, \"'+id+'.\"')
  elif ar == 'remove':
    if id in bot[str(ctx.guild.id)]['achievements']['ids']:
      title = bot[str(ctx.guild.id)]['achievements'][id]['title']
      user = ctx.message.author
      role = discord.utils.get(ctx.guild.roles, name=title)
      await role.delete()
      del bot[str(ctx.guild.id)]['achievements'][id]
      bot[str(ctx.guild.id)]['achievements']['ids'].remove(id)
      await ctx.send('Removed achievement, \"'+id+'.\"')

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def displayNames(ctx, sa, id, *args):
  name = ''
  for word in args:
      name += word
      name += ' '
  name = name[:-1]
  if sa == "achievements" and id in bot[str(ctx.guild.id)]['achievements']['ids']:
    bot[str(ctx.guild.id)]['achievements'][name] = bot[str(ctx.guild.id)]['achievements'][id]
    bot[str(ctx.guild.id)]['achievements']['ids'].append(name)
    del bot[str(ctx.guild.id)]['achievements'][id]
    bot[str(ctx.guild.id)]['achievements']['ids'].remove(id)
  elif sa == "shop" and id in bot[str(ctx.guild.id)]['shop']['ids']:
    bot[str(ctx.guild.id)]['shop'][name] = bot[str(ctx.guild.id)]['shop'][id]
    bot[str(ctx.guild.id)]['shop']['ids'].append(name)
    del bot[str(ctx.guild.id)]['shop'][id]
    bot[str(ctx.guild.id)]['shop']['ids'].remove(id)
  await ctx.send('Changed, \"'+id+',\" to, \"'+name+'.\"')

client.run(tk)
