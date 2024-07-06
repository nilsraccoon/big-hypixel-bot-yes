import discord
from discord.ext import commands


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="sync", description="Syncs the bots slash commands")
    @commands.is_owner()
    async def sync(self, context: commands.Context) -> None:
        """
        This command syncs the bots slash commands
        """
        await context.bot.tree.sync()
        embed = discord.Embed(
            title="Successfully synced all slash commands", color=discord.Color.green()
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unsync", description="Unsyncs the bots slash commands"
    )
    @commands.is_owner()
    async def unsync(self, context: commands.Context) -> None:
        """
        This command unsyncs the bots slash commands
        """
        context.bot.tree.clear_commands(guild=None)
        await context.bot.tree.sync()
        embed = discord.Embed(
            title="Successfully unsynced all slash commands",
            color=discord.Color.green(),
        )
        await context.send(embed=embed)

    @commands.hybrid_command(name="reload", description="Reloads a cog")
    @commands.is_owner()
    async def reload(self, context: commands.Context, cog: str) -> None:
        """
        This command reloads a cog
        :param cog: The name of the cog
        """
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            embed = discord.Embed(
                title=f"Successfully reloaded cog '{cog}'", color=discord.Color.green()
            )
            await context.send(embed=embed)
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            embed = discord.Embed(
                title=f"Failed to reload cog '{cog}'",
                description=exception,
                color=discord.Color.red(),
            )
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
