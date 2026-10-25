import sqlite3
import discord

from discord import app_commands
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
        self.db.execute(
            "INSERT OR IGNORE INTO combat_stats (user_id) VALUES (?)",
            (winner_id,)
        )
        self.db.execute(
            "INSERT OR IGNORE INTO combat_stats (user_id) VALUES (?)",
            (loser_id,)
        )

        self.db.execute(
            "UPDATE combat_stats SET wins = wins + 1 WHERE user_id = ?",
            (winner_id,)
        )
        self.db.execute(
            "UPDATE combat_stats SET losses = losses + 1 WHERE user_id = ?",
            (loser_id,)
        )
        self.db.commit()

    @app_commands.command(
        name="stats_combat",
        description="Consulte les statistiques de combat d'un membre."
    )
    @app_commands.describe(membre="Le membre dont tu veux voir les statistiques")
    async def stats_combat(
        self,
        interaction: discord.Interaction,
        membre: discord.Member = None
    ):
        membre = membre or interaction.user

        wins, losses, draws = self.get_stats(membre.id)
        total = wins + losses + draws
        taux = (wins / total * 100) if total else 0

        embed = discord.Embed(
            title=f"⚔️ Statistiques de {membre.display_name}",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=membre.display_avatar.url)
        embed.add_field(name="🏆 Victoires", value=str(wins))
        embed.add_field(name="💀 Défaites", value=str(losses))
        embed.add_field(name="🤝 Égalités", value=str(draws))
        embed.add_field(name="⚔️ Combats", value=str(total))
        embed.add_field(name="📊 Taux de victoire", value=f"{taux:.1f}%")

        await interaction.response.send_message(embed=embed)

    def cog_unload(self):
        self.db.close()


async def setup(bot):
    await bot.add_cog(Duel(bot))
