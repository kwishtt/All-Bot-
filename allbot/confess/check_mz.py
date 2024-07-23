import discord
from discord.ext import commands
from discord import app_commands
import random

# Thay thế 'YOUR_BOT_TOKEN' bằng token của bot
TOKEN = '   '

bot = commands.Bot(command_prefix='mz.', intents=discord.Intents.all())

music_bot = [
    411916947773587456, 944016826751389717, 776095696646438972, 339926969548275722,
    1066057160125059112, 1093771910388662343, 1244953067988979722, 1245342437874864238,
    1207851471434031144, 1257282210227159061, 1257282254418350222
]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello', help='Trả về câu chào')
async def hello(ctx):
    response = "Hello!"
    await ctx.send(response)

async def check_music_bots(ctx):
    active_bots = []
    inactive_bots = []
    no_active_bots = []

    for member in ctx.guild.members:
        if member.bot:
            if member.voice and member.voice.channel:
                active_bots.append(member)
            else:
                inactive_bots.append(member)

    for i in music_bot:
        member = ctx.guild.get_member(i)
        if member and member not in active_bots:
            no_active_bots.append(member)

    pages = []
    bots_per_page = 10

    all_bots = active_bots + no_active_bots
    for i in range(0, len(all_bots), bots_per_page):
        page_bots = all_bots[i:i + bots_per_page]
        embed = discord.Embed(title="Check music bot", description="", color=0x00ff00)
        embed.add_field(name="Đang làm việc:", value="\n".join([member.display_name for member in page_bots if member in active_bots]) or "không có bot nào đang phát nhạc.", inline=False)
        embed.add_field(name="Bot không hoạt động:", value="\n".join([member.display_name for member in page_bots if member in no_active_bots]) or "tất cả bot đều đang phát nhạc.", inline=False)
        pages.append(embed)

    if not pages:
        embed = discord.Embed(title="Check music bot", description="", color=0x00ff00)
        embed.add_field(name="Đang làm việc:", value="không có bot nào đang phát nhạc.", inline=False)
        embed.add_field(name="Bot không hoạt động:", value="tất cả bot đều đang phát nhạc.", inline=False)
        pages.append(embed)

    class BotPages(discord.ui.View):
        def __init__(self, pages):
            super().__init__(timeout=None)
            self.pages = pages
            self.current_page = 0
            self.message = None

        async def send_initial_message(self, ctx):
            self.message = await ctx.send(embed=self.pages[self.current_page], view=self)

        @discord.ui.button(label="👈", style=discord.ButtonStyle.secondary)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.current_page > 0:
                self.current_page -= 1
                await self.message.edit(embed=self.pages[self.current_page])
                await interaction.response.edit_message(embed=self.pages[self.current_page])

        @discord.ui.button(label="👉", style=discord.ButtonStyle.secondary)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.current_page < len(self.pages) - 1:
                self.current_page += 1
                await self.message.edit(embed=self.pages[self.current_page])
                await interaction.response.edit_message(embed=self.pages[self.current_page])

    view = BotPages(pages)
    await view.send_initial_message(ctx)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'mz' == message.content.lower():
        ctx = await bot.get_context(message)
        await check_music_bots(ctx)

    await bot.process_commands(message)

bot.run(TOKEN)
