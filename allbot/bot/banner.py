import discord
from discord.ext import commands, tasks
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

# Danh sách từ cấm
banned_words = [
    "địt", "cặc", "lồn", "đụ", "đụ má", "đụ mẹ",
    "sex", "buồi", "lồn", "dái", "địt", "óc chó", "đụ", "parky",
    "cặc", "dái", "đĩ", "đụ má", "cặc kẹ", "địt mẹ", "địt con mẹ mày",
    "bitch", "asshole", "cock", "shit", "penis", "vú", "đít", "svl"
]

# Danh sách các kênh bỏ qua
excluded_channels = ["1245114225739960492"]  # Thay bằng ID của kênh bạn muốn bỏ qua

# ID của kênh để gửi log
log_channel_id = 1250791755159179346  # Thay bằng ID của kênh log bạn muốn

# Tạo defaultdict để theo dõi số lần vi phạm của người dùng
user_warnings = defaultdict(int)
user_mute_times = {}  # Từ điển để theo dõi thời gian mute của người dùng

# Thiết lập intents
intents = discord.Intents.default()
intents.messages = True  # Cho phép bot lắng nghe các sự kiện tin nhắn

# Thiết lập client và command prefix
client = commands.Bot(command_prefix='pl.', intents=discord.Intents.all())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Kiểm tra xem tin nhắn có trong kênh cần bỏ qua không
    if str(message.channel.id) in excluded_channels:
        return

    # Trích xuất và xử lý nội dung tin nhắn
    content = message.content.lower().strip()

    # Kiểm tra từng từ trong message có trong banned_words không
    for word in banned_words:
        if word in content:
            await asyncio.sleep(1)
            await message.delete()
            user_warnings[message.author.id] += 1  # Tăng số lần vi phạm của người dùng

            if user_warnings[message.author.id] == 2:
                await message.channel.send(
                    f"{message.author.mention} mồm xinh nay đi chơi hơi xa, nhắc lần 2 nhé, không có lần 3 đâu cưng",
                    delete_after=60
                )

            if user_warnings[message.author.id] >= 3:
                # Mute người dùng
                muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Tên role mute
                if muted_role:
                    await message.author.add_roles(muted_role)
                    user_mute_times[message.author.id] = datetime.now() + timedelta(minutes=30)  # Lưu thời gian mute
                    await message.channel.send(
                        f"{message.author.mention} đã bị mute vì vi phạm nhiều lần.",
                        delete_after=60
                    )
                    # Gỡ mute sau 30 phút
                    await unmute_after_delay(message.author, muted_role, message.guild)
                else:
                    await message.channel.send(
                        f"{message.author.mention} vừa nói gì thế? ANH NHẮC EM ĐẤY! Lần nữa anh mute em 30 phút!",
                        delete_after=60
                    )
            else:
                await message.channel.send(
                    f"{message.author.mention} vừa nói gì thế? ANH NHẮC EM ĐẤY! Lần nữa anh mute em 30 phút!",
                    delete_after=60
                )
            break

    await client.process_commands(message)

async def unmute_after_delay(member, role, guild):
    await asyncio.sleep(1800)  # Chờ 30 phút
    await member.remove_roles(role)
    log_channel = client.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"{member.mention} đã được gỡ mute sau 30 phút.")
    user_mute_times.pop(member.id, None)  # Xóa thời gian mute sau khi gỡ mute

@client.command()
async def muted_list(ctx):
    if not user_mute_times:
        await ctx.send("Hiện không có ai bị mute.")
        return
    
    mute_list = "Danh sách người bị mute:\n"
    for user_id, unmute_time in user_mute_times.items():
        user = await client.fetch_user(user_id)
        time_left = unmute_time - datetime.now()
        minutes_left = int(time_left.total_seconds() // 60)
        mute_list += f"{user.name}#{user.discriminator} - {minutes_left} phút còn lại\n"

    await ctx.send(mute_list)

token = 'YOUR_BOT_TOKEN'
# Chạy bot
client.run(token)


