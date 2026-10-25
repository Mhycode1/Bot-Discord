import sqlite3
import random

import discord
from discord.ext import commands


class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.db = sqlite3.connect("combats.db")

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS combat_stats (
                user_id INTEGER PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0
            )
        """)

        self.db.commit()

    def get_stats(self, user_id):
        self.db.execute(
            "INSERT OR IGNORE INTO combat_stats (user_id) VALUES (?)",
            (user_id,)
        )
        self.db.commit()

        cursor = self.db.execute(
            "SELECT wins, losses, draws FROM combat_stats WHERE user_id = ?",
            (user_id,)
        )

        return cursor.fetchone()

    def update_stats(self, winner_id, loser_id):
        self.get_stats(winner_id)
        self.get_stats(loser_id)

        self.db.execute(
            "UPDATE combat_stats SET wins = wins + 1 WHERE user_id = ?",
            (winner_id,)
        )

        self.db.execute(
            "UPDATE combat_stats SET losses = losses + 1 WHERE user_id = ?",
            (loser_id,)
        )

        self.db.commit()

    @commands.command(name="stats_combat")
    async def stats_combat(
        self,
        ctx,
        membre: discord.Member = None
    ):
        membre = membre or ctx.author

        wins, losses, draws = self.get_stats(membre.id)
        total = wins + losses + draws

        taux = wins / total * 100 if total > 0 else 0

        embed = discord.Embed(
            title=f"⚔️ Combats de {membre.display_name}",
            color=discord.Color.purple()
        )

        embed.set_thumbnail(url=membre.display_avatar.url)
        embed.add_field(name="🏆 Victoires", value=str(wins))
        embed.add_field(name="💀 Défaites", value=str(losses))
        embed.add_field(name="🤝 Égalités", value=str(draws))
        embed.add_field(name="⚔️ Combats", value=str(total))
        embed.add_field(
            name="📊 Taux de victoire",
            value=f"{taux:.1f}%"
        )

        await ctx.send(embed=embed)

    @commands.command(name="duel")
    async def duel(self, ctx, membre: discord.Member = None):

        if membre is None:
            await ctx.send("❌ Tu dois mentionner un joueur !")
            return

        if membre.id == ctx.author.id:
            await ctx.send("❌ Tu ne peux pas te défier toi-même !")
            return

        if membre.bot:
            await ctx.send("❌ Tu ne peux pas défier un bot !")
            return

        duel = self

        class DuelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(
                label="Accepter",
                style=discord.ButtonStyle.success
            )
            async def accepter(
                self,
                interaction: discord.Interaction,
                button: discord.ui.Button
            ):
                if interaction.user.id != membre.id:
                    await interaction.response.send_message(
                        "Ce défi ne t'est pas destiné !",
                        ephemeral=True
                    )
                    return

                for item in self.children:
                    item.disabled = True

                await interaction.response.edit_message(
                    content=f"⚔️ {membre.mention} accepte le duel !",
                    view=self
                )

                joueurs = [ctx.author, membre]
                gagnant = random.choice(joueurs)
                perdant = (
                    membre if gagnant.id == ctx.author.id
                    else ctx.author
                )

                duel.update_stats(gagnant.id, perdant.id)

                await ctx.send(
                    f"⚔️ **Résultat du duel !**\n\n"
                    f"🏆 {gagnant.mention} remporte la victoire !\n"
                    f"💀 {perdant.mention} perd le combat."
                )

                self.stop()

            @discord.ui.button(
                label="Refuser",
                style=discord.ButtonStyle.danger
            )
            async def refuser(
                self,
                interaction: discord.Interaction,
                button: discord.ui.Button
            ):
                if interaction.user.id != membre.id:
                    await interaction.response.send_message(
                        "Ce défi ne t'est pas destiné !",
                        ephemeral=True
                    )
                    return

                for item in self.children:
                    item.disabled = True

                await interaction.response.edit_message(
                    content=f"❌ {membre.mention} refuse le duel.",
                    view=self
                )

                self.stop()

            async def on_timeout(self):
                for item in self.children:
                    item.disabled = True

        view = DuelView()

        await ctx.send(
            f"⚔️ {membre.mention}, tu es défié par "
            f"{ctx.author.mention} !\n"
            "Tu as 60 secondes pour accepter ou refuser.",
            view=view
        )

    def cog_unload(self):
        self.db.close()


async def setup(bot):
    await bot.add_cog(Duel(bot))
