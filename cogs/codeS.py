import discord
from discord.ext import commands
from discord import app_commands

import json
import random
import os

DATA_FILE = "code_secret_data.json"

class CodeSecret(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.parties = {}

    if not os.path.exists(DATA_FILE):
      with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump({}, f)
  
  @commands.command(name="code")
  async def code(self, bot):
    self.bot = bot

  @commands.command(name="profil")
  async def profil(self, ctx):
    await ctx send(f"👤 Profil de **{ctx.author.display_name}**\n" "Les statistiques arrivent bientôt !!")

  @commands.command(name=classement)
  asynd def classement(self, ctx):
    await ctx send("🏆 **Classement du Code secret**\n" "Le classement arrive bientôt !!!")

async def setup(bot):
  await bot.add_cog(CodeSecret(bot))
