import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="😟 ")

bot.run(os.environ["IGRW_TOKEN"])
