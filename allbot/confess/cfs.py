import discord
from discord.ext import commands
from discord import app_commands
import random

# Thay thế 'YOUR_BOT_TOKEN' bằng token của bot
TOKEN = 'your_token_here'
# Định nghĩa prefix cho lệnh của bot, ví dụ: '!'

GUILD_ID = '1150823311954149426'  # Thay thế bằng ID của guild/server của bạn
import discord
from discord.ext import commands


class allin(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="cfs.", intents=discord.Intents.all())
        self.synced = False

    async def setup_hook(self):
        if not self.synced:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            self.synced = True

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

bot = allin()

@bot.tree.command(name="confess", description="Gửi confession ẩn danh")
async def confess(interaction: discord.Interaction, message: str):
    msg = str(message)
    confession_channel_id = 1249000997112774767
    confession_channel = interaction.guild.get_channel(confession_channel_id)
    log_id = 1250791755159179346
    log_channel = interaction.guild.get_channel(log_id)
    count = 0

    if confession_channel:
        embed = discord.Embed(title="Thay lời muốn nói", description=message, color=random.randint(0, 0xFFFFFF))
        embed.set_footer(text="Mẫu Giáo Lớn with ❤️")
        async for message in confession_channel.history(limit=None):
            count += 1

        confession_message = await confession_channel.send(embed=embed)
        log_embed = discord.Embed(title="Log", description=f"Confession thứ {count} đã được gửi bởi {interaction.user.mention} \n`{msg}`", color = discord.Color.blue())
        log_embed.set_footer(text="Mẫu Giáo Lớn with ❤️")
        await log_channel.send(embed=log_embed)

        thread = await confession_message.create_thread(name=f"Trả lời confess thứ #{count}")

        await interaction.response.send_message('Confession của bạn đã được gửi thành công!', ephemeral=True)
    else:
        await interaction.response.send_message('Không tìm thấy kênh. Vui lòng kiểm tra lại.', ephemeral=True)


# Chạy bot
bot.run(TOKEN)
