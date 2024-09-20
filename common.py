import disnake
from disnake.ext import commands


SlashInteraction = disnake.ApplicationCommandInteraction

intents = disnake.Intents.default()
intents.members = True
bot = commands.InteractionBot(intents=intents)

ALERT = 0xe9967a
NEUTRAL = 0xbdc0c1
SUCCESS = 0x2ecc71
COLORS = [0xFFCA1F, 0x198BCC, 0xFF2020]