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
    @commands.command(name="stats_combat")
    async def stats_combat(self, ctx, membre: discord.Member = None):
        membre = membre or ctx.author
    
        wins, losses, draws = self.get_stats(membre.id)
    
        await ctx.send(
            f"⚔️ **Statistiques de {membre.display_name}**\n"
            f"🏆 Victoires : {wins}\n"
            f"💀 Défaites : {losses}\n"
            f"🤝 Égalités : {draws}"
        )

    def cog_unload(self):
        self.db.close()


async def setup(bot):
    await bot.add_cog(Duel(bot))
