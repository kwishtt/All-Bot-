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



game_active = False
betting_players = {}
icons = ['🍎', '🍊', '🍇', '🍓', '🍒', '🍑']
icon_names = {
    'a': '🍎',
    'o': '🍊',
    'g': '🍇',
    's': '🍓',
    'c': '🍒',
    'p': '🍑'
}
choices = {}

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

@client.event
async def on_ready():
    load_user_balances()
    print(f'Đã đăng nhập với tư cách {client.user}')

def is_allowed_channel(ctx):
    return ctx.channel.id == ALLOWED_CHANNEL_ID
@client.command()
async def bc(ctx):
    e_coin = discord.utils.get(ctx.guild.emojis, name='mcn')
    if not is_allowed_channel(ctx):
        return
    global game_active
    if game_active:
        await ctx.send("Đang chờ về bờ!\nĐợi game sau nhé")
        return
    game_active = True
 
    # Tạo Embed cho bàn chơi
    embed_board = discord.Embed(title="Bắt đầu trò chơi!", color=random.randint(0, 0xFFFFFF))
    embed_board.add_field(name="Biểu tượng: \na: 🍎         |         o: 🍊         |         g: 🍇 \n\n ---------------------------------------\n\ns: 🍓         |         c: 🍒         |         p: 🍑\n \n", value="   \n~\nDùng $c <kí hiệu> <tiền> \nĐặt cược vào chữ cái tượng trưng cho HOA QUẢ bạn chọn. \nVí dụ $c p 100", inline=False)
    board_msg = await ctx.send(embed=embed_board)
    
    # Tạo Embed cho đếm thời gian
    embed_timer = discord.Embed(title="Bắt đầu đếm ngược!", color=random.randint(0, 0xFFFFFF))
    embed_timer.description = "Sau 60 giây sẽ quay số!"
    embed_timer.set_footer(text="Thời gian chỉ là tương đối!")
    time_msg = await ctx.send(embed=embed_timer)


    cd = 60
    while cd > 0:
        embed_timer.description = f"Sau {cd} giây sẽ quay số!"
        await time_msg.edit(embed=embed_timer)
        await asyncio.sleep(1)
        cd -= 1
    if cd <= 1:
        await board_msg.edit(content="Quay số!")
        await roll(ctx)
    
@client.command()
async def c(ctx, name: str, amount: str):
    e_coin = discord.utils.get(ctx.guild.emojis, name='mcn')
    global game_active, betting_players
    if not is_allowed_channel(ctx):
        return
    if not game_active:
        await ctx.send("Không có trò chơi nào đang hoạt động!")
        return

    if amount == 'all' and name in icon_names:
        amount = user_balances.get(ctx.author.id, 0)
        if amount == 0:
            await ctx.send("Bạn không có tiền để đặt cược.")
            return
        if ctx.author.id not in betting_players:
            betting_players[ctx.author.id] = []
        betting_players[ctx.author.id].append((icon_names[name], amount))
        await ctx.send(f"{ctx.author.mention} đã đặt cược {amount} MCoin {e_coin} vào {icon_names[name]}!")
        update_user_balance(ctx.author.id, -amount)

        return

    if not amount.isdigit():
        await ctx.send("Số tiền không hợp lệ! Vui lòng nhập một số nguyên dương. Ví dụ: $c a 100")
        return
    amount = int(amount)
    if not user_has_enough_money(ctx.author.id, amount):
        await ctx.send("Đếch có tiền mà cứ ngó vào đây !")
        return
    if name not in icon_names:
        await ctx.send("Tên không hợp lệ! Vui lòng chọn một tên từ danh sách.")
        return

    if ctx.author.id not in betting_players:
        betting_players[ctx.author.id] = []
    betting_players[ctx.author.id].append((icon_names[name], amount))
    await ctx.send(f"{ctx.author.mention} đã đặt cược {amount} MCoin  {e_coin} vào {icon_names[name]}!")
    update_user_balance(ctx.author.id, -amount)



@client.command()
async def roll(ctx):
    if ctx.author.id not in admin and ctx.command.name != "bc":
        await ctx.send("Bạn không có quyền truy cập lệnh này!")
        return
    e_coin = discord.utils.get(ctx.guild.emojis, name='mcn')
    global game_active, betting_players
    if not is_allowed_channel(ctx):
        return
    if not game_active:
        # await ctx.send("Không có trò chơi nào đang hoạt động!")
        return
    game_active = False

    message = await ctx.send("Kết quả: ")
    for i in range(4):
        kq = random.choice(icons)
        kq2 = random.choice(icons)
        kq3 = random.choice(icons)
        await message.edit(content=f"# Quay số: {kq} {kq2} {kq3}")
        ss = await ctx.send("tưng tưng tứng tứng từng từng tưng tưng")
        await asyncio.sleep(0.04)
        await ss.delete()

    await message.delete()
    rd1 = random.choice(icons)
    rd2 = random.choice(icons)
    rd3 = random.choice(icons)
    winning_icons = [rd1, rd2, rd3]
    await ctx.send(f"# Kết quả: {' '.join(winning_icons)}")

    if len(betting_players) == 0:
        await ctx.send("Không có người chơi nào đã đặt cược.")
    else:
        for user_id, bets in betting_players.items():
            total_payout = 0
            user = await client.fetch_user(user_id)
            results = []
            for icon, bet_amount in bets:
                match_count = winning_icons.count(icon)
                payout = bet_amount * match_count
                if payout > 0:
                    update_user_balance(user_id, payout)
                    total_payout += payout
                    # cộng tiền cho người chơi
                    update_user_balance(user_id, payout)   
                    results.append(f"{bet_amount} MCoin  {e_coin} vào {icon} thừa thắng xông lên {payout*2} MCoin")
                else:
                    results.append(f"{bet_amount} MCoin  {e_coin} vào {icon} xa bờ quá!")
            result_message = "\n".join(results)
            await ctx.send(f"{user.mention}:\n{result_message}")
        betting_players.clear()
    await ctx.send("Trò chơi đã kết thúc!")
    game_active = False

client.run(TOKEN)
