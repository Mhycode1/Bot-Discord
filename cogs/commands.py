import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nombre: int):
        await ctx.channel.purge(limit=nombre + 1)
        msg = await ctx.send(f"✅ {nombre} messages supprimés.")
        await msg.delete(delay=3)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        salon = ctx.channel
        nouveau = await salon.clone(reason="Nuke")
        await nouveau.move(after=salon)
        await salon.delete()
        msg = await nouveau.send("💥 Salon nuké !")
        await msg.delete(delay=3)

async def setup(bot):
    await bot.add_cog(CommandCog(bot))