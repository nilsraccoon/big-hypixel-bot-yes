import discord
from discord.ext import commands
import dotenv
import os
import platform

dotenv.load_dotenv()


intents = discord.Intents.all()


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None,
        )

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        print("trying to enable extensions")
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """

        await self.load_cogs()


TOKEN = os.getenv("TOKEN")
bot = DiscordBot()
bot.run(TOKEN)
