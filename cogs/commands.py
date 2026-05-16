import discord
from discord.ext import commands
import datetime

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.start_time = datetime.datetime.utcnow()

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

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, role: discord.Role = None):
        if role is None:
            role = ctx.guild.default_role
        perms = ctx.channel.permissions_for(role)
        if not perms.send_messages:
            msg = await ctx.send("❌ Le salon est déjà lock.")
            await msg.delete(delay=3)
        else:
            await ctx.channel.set_permissions(role, send_messages=False)
            msg = await ctx.send("✅ Salon lock.")
            await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, role: discord.Role = None):
        if role is None:
            role = ctx.guild.default_role
        perms = ctx.channel.permissions_for(role)
        if not perms.send_messages:
            await ctx.channel.set_permissions(role, send_messages=True)
            msg = await ctx.send("✅ Salon unlock.")
            await msg.delete(delay=3)
        else:
            msg = await ctx.send("❌ Le salon n'est pas lock.")
            await msg.delete(delay=3)
            
    @commands.command()
    async def botstats(self, ctx):
        uptime = datetime.datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(title="📊 Stats du bot", color=discord.Color.blurple())
        embed.add_field(name="🏓 Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="🌍 Serveurs", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Utilisateurs", value=len(self.bot.users), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def report(self, ctx, membre: discord.Member, *, raison: str):
        salon = discord.utils.get(ctx.guild.channels, name="reports")
        if not salon:
            return await ctx.send("❌ Aucun salon `reports` trouvé.")
        
        embed = discord.Embed(title="🚨 Nouveau report", color=discord.Color.red())
        embed.add_field(name="Reporté", value=membre.mention, inline=True)
        embed.add_field(name="Reporté par", value=ctx.author.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=False)
        embed.add_field(name="Salon", value=ctx.channel.mention, inline=True)
        
        await salon.send(embed=embed)
        await ctx.message.delete()
        await ctx.send("✅ Report envoyé.", delete_after=3)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Les différentes commandes : ")
        embed.add_field(name="🛠️ Modération", value="`clear` `nuke` `lock` `unlock` `report`", inline=False)
        embed.add_field(name="🎨 Fun", value="`color` `avatar`", inline=False)
        embed.add_field(name="📊 Info", value="`botstats`", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandCog(bot))
