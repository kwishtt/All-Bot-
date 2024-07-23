import discord
import random
from discord.ext import commands
import time
import asyncio
TOKEN = "your_token_here"
ALLOWED_CHANNEL_ID = 1260260294538563585  # Thay thế bằng ID kênh của bạn
admin = [1151938921261957120, 1119601947683590145, 1260203823771815998, 1260203823771815998]

intents = discord.Intents.default()
intents.messages = True
intents.typing = True
client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


user_balances = {}

def load_user_balances():
    global user_balances
    try:
        with open('money.txt', 'r') as file:
            for line in file:
                user_id, balance = line.strip().split(',')
                user_balances[int(user_id)] = int(balance)
    except FileNotFoundError:
        user_balances = {}

def save_user_balances():
    with open('money.txt', 'w') as file:
        for user_id, balance in user_balances.items():
            file.write(f'{user_id},{balance}\n')

def user_has_enough_money(user_id, amount):
    return user_balances.get(user_id, 0) >= amount


def update_user_balance(user_id, amount):
    if user_id in user_balances:
        user_balances[user_id] += amount
    else:
        user_balances[user_id] = amount
    save_user_balances()


#lệnh nhận coin hàng ngày
from datetime import datetime, timedelta

# This is a dictionary mapping from user IDs to the last time they received daily coins
last_received = {}
ls_earn = [
    "{ctx.author.mention} đã móc bọc được {rd_coin} MCoin  🎉",
    "{ctx.author.mention} đã đâm thuê chém mướn được {rd_coin} MCoin 🎉",
    "{ctx.author.mention} giật túi {rd_coin} MCoin    🎉",
    "{ctx.author.mention} đã nhặt được {rd_coin} MCoin 🎉",
    "{ctx.author.mention} đã xách vữa {rd_coin} MCoin  🎉",
    "{ctx.author.mention} đã móc túi được {rd_coin} MCoin    🎉",
    "Ô ai đánh rơi {rd_coin} MCoin ở đây vậy? {ctx.author.mention} nó thó đi rồi 🎉",
    "Con mèo nhà {ctx.author.mention} đã mang về cho họ {rd_coin} MCoin 🎉"]
@client.command()
async def earn(ctx):
    user_id = ctx.author.id
    now = datetime.now()

    if user_id in last_received and now - last_received[user_id] < timedelta(hours=12):
        cd_time_earn = (now - last_received[user_id]).seconds
        cd_time_earn = 12 - cd_time_earn // 3600

        await ctx.send("Nay bạn đã nhận rồi! Hãy quay lại sau {} giờ.".format(cd_time_earn))
    else:
        # This is pseudocode, replace it with your actual function to update the user's balance
        e_coin = discord.utils.get(ctx.guild.emojis, name='mcn')
        rd_coin = random.randint(1, 30)
        update_user_balance(user_id, rd_coin)
        last_received[user_id] = now
        await ctx.send(random.choice(ls_earn).format(ctx=ctx, rd_coin=rd_coin))
#bank command cho phép người chơi chuyển tiền cho người khác
@client.command()
async def bank(ctx, user: discord.User, amount: int):
    if not user_has_enough_money(ctx.author.id, amount):
        await ctx.send("Đếch có tiền mà cứ ngó vào đây!")
        return
    if amount <= 0:
        await ctx.send("Số tiền phải lớn hơn 0!")
        return
    if user == ctx.author:
        await ctx.send("Bạn không thể chuyển tiền cho chính mình!")
        return
    #xác nhận người chơi chuẩn bị chuyển tiền
    await ctx.send(f"{ctx.author.mention} bạn có chắc chắn muốn chuyển {amount} MCoin cho {user.mention}? (yes/no)\nGiao dịch sẽ hủy sau 30 giây.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError as e:
        await ctx.send("Hết thời gian chờ!")
        return
    if msg.content.lower() != 'yes':
        await ctx.send("Hủy bỏ!")
        return
        
    update_user_balance(ctx.author.id, -amount)
    update_user_balance(user.id, amount)
    await ctx.send("Ting Ting!!")
    await ctx.send(f"{ctx.author.mention} đã chuyển {amount} MCoin cho {user.mention} thành công!")

ib_random = ["Cùng tương tác nhé!!",
             "Cùng phát triển server nào",
             "Chúc chơi game vui vẻ!!",
             "Chúc ngày tốt lànhhhhhh",

]
@client.command()
async def coin(ctx):
    e_coin = discord.utils.get(ctx.guild.emojis, name='mcn')
    user_id = ctx.author.id
    balance = user_balances.get(user_id, 0)
    say_rd = random.choice(ib_random)
    if user_id != ctx.author.id:
        await ctx.send("Săm soi cái giề?")
    else:
        if balance <= 0:
            await ctx.author.send(f"Hình như bạn không thể ngửi thấy mùi tiền nhỉ!\nTôi ngửi thấy mùi nghèo từ {balance} MCoin {e_coin} của bạn đếy!")
        else:
            # gửi tin nhắn riêng 
            await ctx.author.send(f"Bạn đang sở hữu {balance} MCoin {e_coin}!\n{say_rd}")

@client.command()
async def topcoin (ctx):
    top = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Top 5 người giàu nhất", color=random.randint(0, 0xFFFFFF))
    for i, (user_id, balance) in enumerate(top[:5]):
        user = await client.fetch_user(user_id)
        embed.add_field(name=f"{i+1}. {user.name}", value=f"{balance} MCoin 💸", inline=False)
    await ctx.send(embed=embed)



@client.command()
async def check(ctx, user: discord.User):
    if ctx.author.id in admin:
        balance = user_balances.get(user.id, 0)
        await ctx.author.send(f"Số dư của {user.mention} là {balance} MCoin")
    else:
        await ctx.send("Bạn không có quyền truy cập lệnh này!")

@client.command()
async def set(ctx, user: discord.User, amount: int):
    if ctx.author.id in admin:
        user_balances[user.id] = amount
        save_user_balances()
        await ctx.author.send(f"Đã cập nhật số dư của {user.mention} thành {amount} MCoin")
    else:
        await ctx.send("Bạn không có quyền truy cập lệnh này!")

@client.command()
async def add(ctx, user: discord.User, amount: int):
    if ctx.author.id in admin:
        update_user_balance(user.id, amount)
        await ctx.author.send(f"Đã thêm {amount} MCoin cho {user.mention}")
    else:
        await ctx.send("Bạn không có quyền truy cập lệnh này!")

@client.command()
async def guide(ctx):
    e_heart = discord.utils.get(ctx.guild.emojis, name='bl15')
    e_blink = discord.utils.get(ctx.guild.emojis, name='bl17')
    e_ar = discord.utils.get(ctx.guild.emojis, name='ar')
    e_no = discord.utils.get(ctx.guild.emojis, name='bl27')
    e_cl = discord.utils.get(ctx.guild.emojis, name='bl22')
    e_mgl1 = discord.utils.get(ctx.guild.emojis, name='MGL1')
    e_mgl2 = discord.utils.get(ctx.guild.emojis, name='MGL2')
    e_mgl3 = discord.utils.get(ctx.guild.emojis, name='MGL3')

    embed = discord.Embed(title=f"{e_blink} Trợ giúp {e_cl}", color=random.randint(0, 0xFFFFFF))
    embed.add_field(name=f"{e_heart} Chào mừng đến với Funny Game MGL.{e_heart}\n                              {e_mgl1} {e_mgl2} {e_mgl3}", value="Đây là hướng dẫn sử dụng bot Casino MGL", inline=False)
    embed.add_field(name=f"{e_no} Các lệnh:", value="Dưới đây là danh sách các lệnh mà bạn có thể sử dụng", inline=False)
    embed.add_field(name="Lệnh Kiếp Đỏ Đen.", value=f"                    {e_heart} {e_heart} {e_heart} {e_heart}\n--------------------", inline=False)
    embed.add_field(name=f"{e_ar} $bc", value="Bắt đầu trò chơi", inline=False)
    embed.add_field(name=f"{e_ar} $c <tên icon> <số tiền>", value="Đặt cược vào biểu tượng", inline=False)
    embed.add_field(name="Lệnh Tiền Bạc", value=f"                    {e_heart} {e_heart} {e_heart} {e_heart}\n--------------------", inline=False)
    embed.add_field(name=f"{e_ar} $earn", value="Nhận coin hàng ngày", inline=False)
    embed.add_field(name=f"{e_ar} $bank <@tên người dùng> <số tiền>", value="Chuyển coin cho người khác", inline=False)
    embed.add_field(name=f"{e_ar} $coin", value="Kiểm tra số dư của bạn", inline=False)
    embed.add_field(name=f"{e_ar} $topcoin", value="Xem top 3 người giàu nhất", inline=False)
    embed.add_field(name="Lệnh  X-O", value=f"                    {e_heart} {e_heart} {e_heart} {e_heart}\n--------------------", inline=False)
    embed.add_field(name=f"{e_ar} $xo <@tên người chơi>", value="Chơi game X-O với người khác", inline=False)
    embed.add_field(name=f"{e_ar} $gg", value="Đầu hàng game X-O", inline=False)

    await ctx.send(embed=embed)
    


client.run(TOKEN)
