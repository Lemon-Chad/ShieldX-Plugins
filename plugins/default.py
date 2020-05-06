import discord
from discord.ext import commands

from achbot import bot
from sxPDK import *

class Test(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("default loaded")
  
  @commands.command()
  @pluginLoaded('default', bot)
  async def ping(self, ctx):
    await ctx.send("pong")


def setup(client):
  client.add_cog(Test(client))