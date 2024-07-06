import discord
from discord.ext import commands
from discord.ext.commands import Context
import dotenv
import requests
import os
from colorama import Fore

dotenv.load_dotenv()


class Bedwars(commands.Cog, name="bedwars"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="bedwars", description="Shows the Bedwars stats of a player"
    )
    async def bedwars(self, context: Context, player: str) -> None:
        """
        This command shows the Bedwars stats of a player
        :param player: The player's name
        """
        # Convert the players name to uuid
        headers = {"Api-Key": os.getenv("POLSU")}
        try:

            request = requests.get(
                f"https://api.polsu.xyz/polsu/minecraft/player?player={player}",
                headers=headers,
            ).json()
            uuid = request["data"]["uuid"]
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
        await context.interaction.response.defer()
        try:

            apikey = os.getenv("HYPIXEL")
            request = requests.get(
                f"https://api.hypixel.net/v2/player?uuid={uuid}&key={apikey}"
            ).json()
            bwstats = request["player"]["stats"]["Bedwars"]

            wins = round(bwstats["wins_bedwars"])
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


async def setup(bot) -> None:
    await bot.add_cog(Bedwars(bot))
