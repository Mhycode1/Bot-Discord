import discord
from discord.ext import commands
from PIL import Image
import io

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def color(self, ctx, hex_color: str):
        hex_color = hex_color.strip("#")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        image = Image.new("RGB", (200, 200), (r, g, b))
        
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        embed = discord.Embed(title=f"🎨 #{hex_color.upper()}", color=int(hex_color, 16))
        embed.add_field(name="HEX", value=f"`#{hex_color.upper()}`", inline=True)
        embed.add_field(name="RGB", value=f"`{r}, {g}, {b}`", inline=True)
        embed.set_image(url="attachment://color.png")
        
        await ctx.send(embed=embed, file=discord.File(buffer, filename="color.png"))

async def setup(bot):
    await bot.add_cog(FunCog(bot))