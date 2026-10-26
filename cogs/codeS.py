
import discord
from discord.ext import commands

import json
import os
import random

DATA_FILE = "code_secret_data.json"


class CodeSecret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parties = {}

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)

    @commands.command(name="code")
    async def code(self, ctx):
        if ctx.author.id in self.parties:
            await ctx.send("Tu as déjà une partie en cours enflure !!")
            return

        code_secret = "".join(random.sample("0123456789", 3))
        self.parties[ctx.author.id] = True

        await ctx.send(
            "🔐 **Code secret de Mhyst**\n"
            "Trouve le code à 3 chiffres !\n"
            "Tu as 8 tentatives. Envoie ton code dans le salon."
        )

        for tentative in range(8):
            try:
                message = await self.bot.wait_for(
                    "message",
                    timeout=60,
                    check=lambda m: m.author == ctx.author
                    and m.channel == ctx.channel
                )
            except TimeoutError:
                await ctx.send(f"Temps écoulé ! Le code était {code_secret}.")
                self.parties.pop(ctx.author.id, None)
                return

            proposition = message.content.strip()

            if len(proposition) != 3 or not proposition.isdigit():
                await ctx.send("Entre un nombre de 3 chiffres enflure !")
                continue

            if proposition == code_secret:
                await ctx.send(
                    f"Bravo ! Tu as trouvé le code en {tentative + 1} tentative(s) !"
                )
                self.parties.pop(ctx.author.id, None)
                return

            bien_places = 0

            for i in range(3):
                if proposition[i] == code_secret[i]:
                    bien_places += 1

            mal_places = len(set(proposition) & set(code_secret)) - bien_places

            await ctx.send(
                f"Tentative {tentative + 1}/8\n"
                f"Bien placés : {bien_places}\n"
                f"Mal placés : {mal_places}"
            )

        await ctx.send(f"Perdu ! Le code était {code_secret}.")
        self.parties.pop(ctx.author.id, None)

    @commands.command(name="profil")
    async def profil(self, ctx):
        await ctx.send(
            f"👤 Profil de **{ctx.author.display_name}**\n"
            "Les statistiques arrivent bientôt !"
        )

    @commands.command(name="classement")
    async def classement(self, ctx):
        await ctx.send(
            "🏆 **Classement du Code secret**\n"
            "Le classement arrive bientôt !"
        )


async def setup(bot):
    await bot.add_cog(CodeSecret(bot))
