import re
import discord
from discord.ext import commands
from discord.ext.commands import Context
import dotenv
import requests
import os
from colorama import Fore
import math
from datetime import datetime
import sqlite3

dotenv.load_dotenv()


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = sqlite3.connect("player_cache.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS player_cache
                          (uuid TEXT PRIMARY KEY, name TEXT)"""
        )

    @commands.hybrid_command(
        name="general", description="Shows general information about a player"
    )
    async def general(self, context: Context, player: str) -> None:
        """
        This command shows the general hypixel stats of a player
        :param player: The player's name
        """
        await context.interaction.response.defer()
        headers = {"Api-Key": os.getenv("POLSU"), "User-Agent": os.getenv("USER_AGENT")}
        self.c.execute("SELECT uuid FROM player_cache WHERE name = ?", (player,))
        cached_uuid = self.c.fetchone()
        if cached_uuid:
            uuid = cached_uuid[0]
        else:
            try:
                request = requests.get(
                    f"https://api.polsu.xyz/polsu/minecraft/player?player={player}",
                    headers=headers,
                ).json()
                uuid = request["data"]["uuid"]
                self.c.execute(
                    "INSERT or REPLACE INTO player_cache VALUES (?, ?)", (uuid, player)
                )
                self.conn.commit()
            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description="An error occured trying to convert the username to a UUID.\nAre you sure that player exists?",
                    color=discord.Color.red(),
                )
                await context.send(embed=embed)
                print(
                    f"{Fore.RED}An error occured in {context.author.guild.name} with command /{context.invoked_with} {player} trying to get uuid from username:\n{e}{Fore.WHITE}"
                )
                return
        try:
            key = os.getenv("HYPIXEL")
            request = requests.get(
                f"https://api.hypixel.net/v2/player?uuid={uuid}&key={key}",
                headers={
                    "User-Agent": os.getenv("USER_AGENT"),
                },
            ).json()
            prefix = request["player"].get("prefix", "NoPrefix")
            if prefix != "NoPrefix":
                prefix = re.sub(r"§.", "", prefix)
            rank = request["player"].get("newPackageRank", "DEFAULT")
            mvppp = request["player"].get("monthlyPackageRank", "not_pp")
            if prefix != "NoPrefix":
                rank = prefix
            elif mvppp == "SUPERSTAR":
                rank = "[MVP++]"
            elif rank == "MVP_PLUS":
                rank = "[MVP+]"
            elif rank == "MVP":
                rank = "[MVP]"
            elif rank == "VIP_PLUS":
                rank = "[VIP+]"
            elif rank == "VIP":
                rank = "[VIP]"
            else:
                rank = "non :skull:"
            networkExperience = request["player"]["networkExp"]
            networkLevel = (math.sqrt((2 * networkExperience) + 30625) / 50) - 2.5
            networkLevel = round(networkLevel, 2)
            giftingMeta = request["player"].get("giftingMeta", {})
            ranks = giftingMeta.get("ranksGiven", 0)
            fl = int(request["player"].get("firstLogin", 0) // 1000)
            ll = int(request["player"].get("lastLogin", 0) // 1000)
            fl = datetime.fromtimestamp(fl).strftime("%d.%m.%Y %H:%M:%S")
            ll = datetime.fromtimestamp(ll).strftime("%d.%m.%Y %H:%M:%S")
            embed = discord.Embed(
                title=f"Stats for {request['player']['displayname']}",
                color=discord.Color.green(),
                description=f"Rank: {rank}\nHypixel Level: {networkLevel}\nKarma: {request['player']['karma']}\nRanks gifted: {ranks}\n\nFirst Login: {fl}\nLast Login: {ll}",
            )
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occured trying to get the player's data from the Hypixel API.\nAre you sure that player has played Hypixel?",
                color=discord.Color.red(),
            )
            await context.send(embed=embed)
            print(
                f"{Fore.RED}An error occured in {context.author.guild.name} with command /{context.invoked_with} {player} trying to get player data from the Hypixel API:\n{e}{Fore.WHITE}"
            )
            return

    def cog_unload(self):
        self.conn.close()


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
