import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from datetime import datetime, timedelta

TOKEN = "ODM4NjY4"
ALLOWED_CHANNEL_ID = 1260885086065393744  # Thay thế bằng ID của kênh được phép

intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix='$', intents=discord.Intents.all())

user_balances = {}
last_game_time = {}

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
#tạo hàm in ra thời gian còn lại của game

class TicTacToe:
    def __init__(self):
        self.board = ["⬜" for _ in range(25)]
        self.current_winner = None

    def print_board(self):
        return '\n'.join([' '.join(self.board[i*5:(i+1)*5]) for i in range(5)])

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == "⬜"]

    def make_move(self, square, mark):
        if self.board[square] == "⬜":
            self.board[square] = mark
            return True
        return False

    def check_winner(self, mark):
        for condition in winning_conditions:
            if all(self.board[i] == mark for i in condition):
                self.current_winner = mark
                return True
        return False


class TicTacToeView(View):
    def __init__(self, game, player1, player2, turn, embed_msg):
        super().__init__(timeout=None)
        self.game = game
        self.player1 = player1
        self.player2 = player2
        self.turn = turn
        self.embed_msg = embed_msg
        self.create_buttons()
        self.game_over = False
        self.message = None
        game_over = False

        
    def create_buttons(self):
        for i in range(25):
            button = Button(label="", emoji=self.game.board[i], custom_id=str(i), style=discord.ButtonStyle.secondary)
            button.callback = self.button_callback
            self.add_item(button)

    def disable_all_buttons(self):
        for button in self.children:
            button.disabled = True

    async def button_callback(self, interaction):
        if interaction.user != self.turn:
            await interaction.response.send_message("Tay nhanh hơn não rồi.\nBớt lanh chanh lại nhé.", ephemeral=True)
            return
        
        pos = int(interaction.data['custom_id'])
        mark = "❌" if self.turn == self.player1 else "0️⃣"
        if self.game.make_move(pos, mark):
            button = [item for item in self.children if item.custom_id == str(pos)][0]
            button.emoji = mark
            button.disabled = True

            if self.game.check_winner(mark):
                self.game_over = True
                self.disable_all_buttons()
                self.embed_msg.description = f"<@{self.turn.id}> thắng!"
                await interaction.response.edit_message(embed=self.embed_msg, view=self)
                update_user_balance(self.turn.id, 10)
                await interaction.followup.send(f"<@{self.turn.id}> đã thắng! Và nhận được 10 MCoins.")
                game_over = True
                last_game_time[self.player1.id] = datetime.now()
                last_game_time[self.player2.id] = datetime.now()
                return
            if all(item.disabled for item in self.children):
                self.game_over = True
                self.embed_msg.description = "# Hết lượt đánh rồi!"
                await interaction.response.edit_message(embed=self.embed_msg, view=self)
                last_game_time[self.player1.id] = datetime.now()
                last_game_time[self.player2.id] = datetime.now()
                game_over = True
                return
            
            self.turn = self.player1 if self.turn == self.player2 else self.player2
            self.embed_msg.description = f"Đến lượt của <@{self.turn.id}>."
            await interaction.response.edit_message(embed=self.embed_msg, view=self)
        else:
            await interaction.response.send_message("Vị trí không hợp lệ hoặc đã được đánh dấu. Chọn vị trí khác.", ephemeral=True)


user_balances = {}
game_over = True

@client.command()
async def xo(ctx, p2: discord.Member):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"Bạn chỉ có thể chơi trò chơi này trong kênh <#{ALLOWED_CHANNEL_ID}>.")
        return

    load_user_balances()
    global game_over, board, player1, player2, turn
    if ctx.author == p2:
        await ctx.send("Bạn không thể chơi với chính mình.")
        return
    if ctx.author.bot or p2.bot:
        await ctx.send("Bot không thể tham gia trò chơi.")
        return
    if not user_has_enough_money(ctx.author.id, 5):
        await ctx.send(f"{ctx.author.mention}, bạn không đủ MCoins để chơi trò chơi này.")
        return
    if not user_has_enough_money(p2.id, 5):
        await ctx.send(f"{p2.mention}, bạn không đủ MCoins để chơi trò chơi này.")
        return
    now = datetime.now()
    if ctx.author.id in last_game_time and now - last_game_time[ctx.author.id] < timedelta(minutes=1):
        sec = (last_game_time[ctx.author.id] + timedelta(minutes=1) - now).seconds

        await ctx.send(f"{ctx.author.mention}, bạn cần đợi {sec} giây nữa trước khi chơi tiếp.")
        return
    if p2.id in last_game_time and now - last_game_time[p2.id] < timedelta(minutes=1):
        sec = (last_game_time[p2.id] + timedelta(minutes=1) - now).seconds
        await ctx.send(f"{p2.mention}, bạn cần đợi {sec} giây nữa trước khi chơi tiếp.")
        return
    if game_over == True:
        await ctx.send(f"{p2.mention}, <@{ctx.author.id}> muốn chơi trò chơi X-O với bạn. Mỗi người cược 5 MCoins. Bạn có muốn chấp nhận không (y/n)?")
        try:
            def check(m):
                return m.author == p2 and m.channel == ctx.channel and m.content.lower() in ['y', 'n']
            msg = await client.wait_for('message', check=check, timeout=30)
            if msg.content.lower() == 'n':
                await ctx.send(f"{p2.mention} đã từ chối lời mời chơi X-O.")
                return
        except asyncio.TimeoutError:
            await ctx.send("Hết thời gian phản hồi.")
            return

        update_user_balance(ctx.author.id, -5)
        update_user_balance(p2.id, -5)

        board = TicTacToe()
        game_over = False
        e_heart = discord.utils.get(ctx.guild.emojis, name='bl15')
        e_blink = discord.utils.get(ctx.guild.emojis, name='bl17')
        e_ar = discord.utils.get(ctx.guild.emojis, name='ar')
        e_no = discord.utils.get(ctx.guild.emojis, name='bl27')
        e_cl = discord.utils.get(ctx.guild.emojis, name='bl22')
        e_mgl1 = discord.utils.get(ctx.guild.emojis, name='MGL1')
        e_mgl2 = discord.utils.get(ctx.guild.emojis, name='MGL2')
        e_mgl3 = discord.utils.get(ctx.guild.emojis, name='MGL3')
        

        # Gửi tin nhắn embed cho luật chơi
        embed_rules = discord.Embed(title="XO Game - Luật chơi", color=random.randint(0, 0xFFFFFF))
        embed_rules.add_field(name=f"{e_heart} Hướng dẫn {e_heart}", value=f"{e_no} Mỗi người cược 5 đồng, chơi trong 3 phút.\n{e_blink}Dùng các nút dưới để chơi.\n{e_ar}Nối 4 ô liên tiếp chéo | dọc | ngang là win\n ", inline=False)
        embed_rules.set_footer(text=" Thời gian còn lại: 180 giây")
        msg = await ctx.send(embed=embed_rules)

        # Gửi tin nhắn embed cho thông tin trò chơi

        num = random.randint(1, 2)
        turn = ctx.author if num == 1 else p2
        player1 = ctx.author
        player2 = p2
        embed_game_info = discord.Embed(title=f"XO Game - Thông tin trò chơi\n                    {e_mgl1}{e_mgl2}{e_mgl3}", color=random.randint(0, 0xFFFFFF))
        embed_game_info.description = f"START | Lượt của <@{turn.id}>.\nThời gian chỉ mang tính tương đối."
        view = TicTacToeView(board, player1, player2, turn, embed_game_info)
        message = await ctx.send(embed=embed_game_info, view=view)
        view.message = message
         
        


        cd = 180
        while cd > 0 and not game_over:
            await asyncio.sleep(1)
            cd -= 1
            embed_rules.set_footer(text=f"# Thời gian còn lại: {cd} giây")
            await msg.edit(embed=embed_rules)
            check = view.game_over
            if check == True:
                game_over = True

                break


            if cd == 0:
                await message.edit(view=view)
                await message.channel.send("Hết giờ chơi. Tiếc quá. ")
                view.game_over = True
                view.disable_all_buttons()
                game_over = True
                last_game_time[player1.id] = datetime.now()
                last_game_time[player2.id] = datetime.now()
        if game_over:
            view.disable_all_buttons()
            view.game_over = True



    else:
        await ctx.send("Trò chơi đang diễn ra, hãy chờ kết thúc trước khi bắt đầu một trò mới.")

@client.command()
async def gg(ctx):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"Bạn chỉ có thể kết thúc trò chơi này trong kênh <#{ALLOWED_CHANNEL_ID}>.")
        return

    global game_over
    if not game_over:
        if ctx.author == player1:

            await ctx.send(f"Trò chơi đã kết thúc. <@{ctx.author.id}> đã đầu hàng.\n<@{player2.id}> thắng 10 MCoins.")
            update_user_balance(player2.id, 10)
            game_over = True
            last_game_time[player1.id] = datetime.now()
            last_game_time[player2.id] = datetime.now()
            # xóa nút của bot





        elif ctx.author == player2:

            await ctx.send(f"Trò chơi đã kết thúc. <@{ctx.author.id}> đã đầu hàng.\n<@{player1.id}> thắng 10 MCoins.")
            update_user_balance(player1.id, 10)
            game_over = True
            last_game_time[player1.id] = datetime.now()
            last_game_time[player2.id] = datetime.now()




        else:
            await ctx.send("Bạn không phải người chơi trong trò chơi này.")
    else:
        await ctx.send("Không có trò chơi nào đang diễn ra.")

winning_conditions = [
    (0, 1, 2, 3), (1, 2, 3, 4),
    (5, 6, 7, 8), (6, 7, 8, 9),
    (10, 11, 12, 13), (11, 12, 13, 14),
    (15, 16, 17, 18), (16, 17, 18, 19),
    (20, 21, 22, 23), (21, 22, 23, 24),

    (0, 5, 10, 15), (5, 10, 15, 20),
    (1, 6, 11, 16), (6, 11, 16, 21),
    (2, 7, 12, 17), (7, 12, 17, 22),
    (3, 8, 13, 18), (8, 13, 18, 23),
    (4, 9, 14, 19), (9, 14, 19, 24),

    (0, 6, 12, 18), (1, 7, 13, 19),
    (5, 11, 17, 23), (6, 12, 18, 24),

    (3, 7, 11, 15), (4, 8, 12, 16),
    (8, 12, 16, 20), (9, 13, 17, 21),
]

client.run(TOKEN)
