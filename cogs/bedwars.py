import discord
from discord.ext import commands
from discord.ext.commands import Context
import dotenv
import requests
import os
from colorama import Fore
import sqlite3

dotenv.load_dotenv()


class Bedwars(commands.Cog, name="bedwars"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = sqlite3.connect("player_cache.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS player_cache
                          (uuid TEXT PRIMARY KEY, name TEXT)"""
        )

    @commands.hybrid_command(
        name="bedwars", description="Shows the Bedwars stats of a player"
    )
    async def bedwars(self, context: Context, player: str) -> None:
        await context.interaction.response.defer()
        """
        This command shows the Bedwars stats of a player
        :param player: The player's name
        """
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
                self.c.execute("INSERT INTO player_cache VALUES (?, ?)", (uuid, player))
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
            apikey = os.getenv("HYPIXEL")
            request = requests.get(
                f"https://api.hypixel.net/v2/player?uuid={uuid}&key={apikey}"
            ).json()
            bwstats = request["player"]["stats"].get("Bedwars", {})

            wins = round(bwstats.get("wins_bedwars", 0))
            losses = round(bwstats.get("losses_bedwars", 0))
            wlr = round(wins / losses, 2) if losses != 0 else wins

            finalkills = round(bwstats.get("final_kills_bedwars", 0))
            finaldeaths = round(bwstats.get("final_deaths_bedwars", 0))
            fkdr = (
                round(finalkills / finaldeaths, 2) if finaldeaths != 0 else finalkills
            )

            beds_broken = round(bwstats.get("beds_broken_bedwars", 0))
            beds_lost = round(bwstats.get("beds_lost_bedwars", 0))
            bblr = round(beds_broken / beds_lost, 2) if beds_lost != 0 else beds_broken

            kills = round(bwstats.get("kills_bedwars", 0))
            deaths = round(bwstats.get("deaths_bedwars", 0))
            kdr = round(kills / deaths, 2) if deaths != 0 else kills

            winstreak = bwstats.get("winstreak", 0)

            embed = discord.Embed(
                title=f"Bedwars Stats for {player}",
                description=f"Wins: {wins}\nLosses: {losses}\n**WLR: {wlr}**\n\nFinal Kills: {finalkills}\nFinal Deaths: {finaldeaths}\n**FKDR: {fkdr}**\n\nBeds Broken: {beds_broken}\nBeds Lost: {beds_lost}\n**BBLR: {bblr}**\n\nKills: {kills}\nDeaths: {deaths}\n**KDR: {kdr}**\n\nWinstreak: {winstreak}",
                color=discord.Color.green(),
            )
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occured trying to get the player's stats.\nAre you sure that player has played Hypixel?",
                color=discord.Color.red(),
            )
            await context.send(embed=embed)
            print(
                f"{Fore.RED}An error occured in {context.author.guild.name} with command /{context.invoked_with} {player} trying to get hypixel stats:\n{e}{Fore.WHITE}"
            )

    @commands.hybrid_command(
        name="winstreak", description="Shows the winstreakss of a player"
    )
    async def winstreak(self, context: Context, player: str) -> None:
        """
        This command shows the Bedwars stats of a player
        :param player: The player's name
        """
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
                self.c.execute("INSERT INTO player_cache VALUES (?, ?)", (uuid, player))
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
            apikey = os.getenv("HYPIXEL")
            request = requests.get(
                f"https://api.hypixel.net/v2/player?uuid={uuid}&key={apikey}"
            ).json()
            ws_bw = request["player"]["stats"].get("Bedwars", {}).get("winstreak", 0)
            ws_duels = (
                request["player"]["stats"].get("Duels", {}).get("current_winstreak", 0)
            )
            ws_sw = request["player"]["stats"].get("SkyWars", {}).get("winstreak", 0)
            ws_tnt = request["player"]["stats"].get("TNTGames", {}).get("winstreak", 0)
            ws_uhc = request["player"]["stats"].get("UHC", {}).get("winstreak", 0)
            embed = discord.Embed(
                title=f"Winstreaks for {player}",
                description=f"Bedwars: {ws_bw}\nDuels: {ws_duels}\nSkywars: {ws_sw}\nTNT Games: {ws_tnt}\nUHC: {ws_uhc}",
                color=discord.Color.green(),
            )
            await context.send(embed=embed)
        except Exception as e:
            print(
                f"{Fore.RED}An error occured in {context.author.guild.name} with command /{context.invoked_with} {player} trying to get hypixel stats:\n{e}{Fore.WHITE}"
            )
            return

    def cog_unload(self):
        self.conn.close()


async def setup(bot) -> None:
    await bot.add_cog(Bedwars(bot))
