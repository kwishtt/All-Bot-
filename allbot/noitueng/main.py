import discord
from discord.ext import commands
from discord import app_commands
import re
import asyncio


bot = commands.Bot(command_prefix='nt.', intents=discord.Intents.all())
 

#Define hàm và biến

current_word = ''
last_word_id = ""
admin_role_name = "ADMINISTRATOR"
used_words = []
reset_in_progress = False


def load_words(filename):
    with open(filename, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

def save_channel_id(channel_id, filename):
    with open(filename, 'w') as file:   
        for id in channel_id: 
            file.write(str(id) + "\n")


def load_channel_id(filename):
    channel_id = []
    with open(filename, 'r') as file:
        for line in file:
            channel_id.append(int(line.strip()))
    return channel_id

def remove_channel_id(channel_id, filename):
    with open(filename, 'r') as file:
        channel_ids = [line.strip() for line in file if line.strip() != str(channel_id)]

    with open(filename, 'w') as file:
        file.write('\n'.join(channel_ids))
        
def save_used_words(used_word, filename):
    with open(filename, 'w') as file:
        for word in used_word:
            file.write(word + '\n')

def load_used_words(filename):
    loaded_words = []
    with open(filename, 'r') as file:
        for line in file:
            loaded_words.append(line.strip())
    return loaded_words
def clear_used_words(filename):
    with open(filename, 'w') as file:
        file.write('')
        
def save_last_id(last_id,filename):
    with open(filename,"w") as file:
        file.write(str(last_id))

def load_last_id(filename):
    lastid = ""
    with open(filename,"r") as file:
        for line in file:
            lastid = int(line.strip())
    return lastid
def clear_last_id(filename):
    with open(filename, 'w') as file:
        file.write('')
        
def save_connect(connect,filename):
    with open(filename,"w") as file:
        file.write(str(connect))

def load_connect(filename):
    connect = ""
    with open(filename,"r") as file:
        for line in file:
            connect = line.strip()
    return connect

def save_dumb(dumb,filename):
    with open(filename,"w") as file:
        for line in dumb:
            file.write(str(line) + "\n")
            
def load_dumb(filename):
    dum = []
    with open(filename,"r") as file:
        for line in file:
            if line != "":
                dum.append(line.strip())
    return dum

def remove_dumb(dumb,filename):
    with open(filename,"r") as file:
        lines = file.readlines()

    modified_lines = [line for line in lines if line.strip() != dumb]

    with open(filename, "w") as file:
        file.writelines(modified_lines)
def save_banned(channel_id, filename):
    with open(filename, 'w') as file:
        for id in channel_id:
            file.write(str(id) + "\n")
            
def load_banned(filename):
    dum = []
    with open(filename,"r") as file:
        for line in file:
            if line != "":
                dum.append(line.strip())
    return dum

def remove_banned(dumb,filename):
    with open(filename,"r") as file:
        lines = file.readlines()

    modified_lines = [line for line in lines if line.strip() != dumb]

    with open(filename, "w") as file:
        file.writelines(modified_lines)

def clear_banned_word(filename):
    with open(filename,"w") as file:
        file.write("")
    
    
english_words = load_words('words.txt')
word_channel_filename = 'word_channel_id.txt'
used_words_filename = "used words.txt"
word_channel_id = load_channel_id(word_channel_filename)
last_word_id_filename = "last_word_id.txt"
used_words = load_used_words(used_words_filename)
last_word_id = load_last_id(last_word_id_filename)
connect_filename = "toggle connect.txt"
connectable = load_connect(connect_filename)
dumb_filename = "dumb.txt"
dumb = load_dumb(dumb_filename)
banned_filename = "banned.txt"
banned_word = load_banned(banned_filename)

#Thủ tục

@bot.command()
async def set_channel(ctx):
    global word_channel_id
    if ctx.author.guild_permissions.administrator:
        word_channel_id.append(ctx.channel.id)
        save_channel_id(word_channel_id, word_channel_filename)
        await ctx.send(f"Đã đặt channel nối từ!")
    else:
        await ctx.send("Bạn cần có quyền admin để thực hiện lệnh này!")

@bot.command()
async def reset_game(ctx):
    global current_word
    global used_words
    global last_word_id
    global connectable
    global reset_in_progress

    if ctx.author.guild_permissions.administrator:
        await ctx.send(f"<@{ctx.author.id}> Chăc chưa??(y/n)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            reset_in_progress = True
            message = await bot.wait_for('message', check=check, timeout=15.0)
            response = message.content.lower().strip()

            if response == "y":
                current_word = ''
                used_words = []
                clear_used_words(used_words_filename)
                last_word_id = ""
                clear_last_id(last_word_id_filename)
                connectable = False
                save_connect(connectable, connect_filename)
                reset_in_progress = False
                await ctx.send("Đã reset game!")
            elif response == "n":
                await ctx.send("Đã huỷ quá trình reset!")
                reset_in_progress = False
        except asyncio.TimeoutError:
            await ctx.send("Đã huỷ quá trình reset!(Hết thời gian)")
            reset_in_progress = False
                
    else:
        await ctx.send("Bạn cần có quyền admin để thực hiện lệnh này!")
        
@bot.command()
async def remove_channel(ctx):
    global word_channel_filename
    
    if ctx.author.guild_permissions.administrator:
        remove_channel_id(ctx.channel.id,word_channel_filename)
        await ctx.send("Đã remove channel nối từ!")
    else:
        await ctx.send("Bạn cần có quyền admin để thực hiện lệnh này!")
        
@bot.command()
async def toggle_connect(ctx):
    global connectable
    if str(connectable) == "False":
        connectable = True
        save_connect(connectable,connect_filename)
        await ctx.send("Người chơi bây giờ **__có thể__** nối từ hai lần liên tiếp!")
    elif str(connectable) == "True":
        connectable = False
        save_connect(connectable,connect_filename)
        await ctx.send("Người chơi bây giờ **__không thể__** nối từ hai lần liên tiếp!")
        
#Main gameplay        

@bot.event
async def on_message(message):
    global current_word
    global used_words
    global last_word_id
    global dumb
    
    if reset_in_progress:
        return

    if message.author == bot.user:
        return

    if current_word == '' and message.channel.id in word_channel_id and len(used_words) == 0:
        word = message.content.lower().strip()
        
        if word == "djt":
            await message.channel.send("me may")
        
        elif re.match("^[a-zA-Z]+$", word):
            
            if word in english_words and word[-1] not in banned_word:
                current_word = word
                used_words.append(word)
                await message.channel.send(f"Game nối từ đã bắt đầu với từ: `{current_word}`")
                await message.add_reaction('✅')
                save_used_words(used_words,used_words_filename)
                last_word_id = message.author.id
                save_last_id(last_word_id,last_word_id_filename)
            elif word[-1] in banned_word and str(message.author.id) in dumb:
                await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                await message.channel.send(f"Từ mày vừa nối có kí tự cuối là `{word[-1]}` (Đã bị ban)")
            elif word[-1] in banned_word :
                await message.add_reaction('❌')
                await message.channel.send(f"Từ bạn vừa nối có kí tự cuối là `{word[-1]}` (Đã bị ban)")    
            elif word in english_words and message.author.id in dumb:
                await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                await message.channel.send(f"Từ `{word}` không tồn tại trong từ điển, thằng ngu!")
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"Từ `{word}` không tồn tại trong từ điển!")
    elif message.channel.id in word_channel_id:
        word = message.content.lower().strip()
        current_word = used_words[-1]
        
        if word == "djt":
            await message.channel.send("me may")
        
        elif re.match("^[a-zA-Z]+$", word):
            
            if (last_word_id == message.author.id and not connectable) and str(message.author.id) in dumb:
                await message.add_reaction('❌')
                await message.channel.send("Mày vừa mới nối từ trước đó rồi thg ngu")            
            elif last_word_id == message.author.id and not connectable:
                await message.add_reaction('❌')
                await message.channel.send("Bạn vừa mới nối từ trước đó!")
            elif word in english_words  and word[-1] not in banned_word:
                
                if word.startswith(current_word[-1]) and word not in used_words:
                    
                    if word not in used_words and str(message.author.id) in dumb:
                        used_words.append(word)
                        save_used_words(used_words,used_words_filename)
                        last_word_id = message.author.id
                        save_last_id(last_word_id,last_word_id_filename)
                        await message.add_reaction('<:chithanh:1229080109336760512>')
                        current_word = word
                    
                    elif word not in used_words:
                        used_words.append(word)
                        save_used_words(used_words,used_words_filename)
                        last_word_id = message.author.id
                        save_last_id(last_word_id,last_word_id_filename)
                        await message.add_reaction('✅')
                        current_word = word
                elif not word.startswith(current_word[-1]) and str(message.author.id) in dumb:
                    await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                    await message.channel.send(f"Từ `{word}` không nối với chữ `{current_word[-1]}`, thằng ngu!")
                elif not word.startswith(current_word[-1]):
                    await message.add_reaction('❌')
                    await message.channel.send(f"Từ `{word}` không nối với chữ `{current_word[-1]}`!")
                elif word in used_words and str(message.author.id) in dumb:
                    await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                    await message.channel.send(f"Từ `{word}` đã được nối trước đó rồi thằng ngu!")                
                elif word in used_words:
                    await message.add_reaction('❌')
                    await message.channel.send(f"Từ `{word}` đã được nối trước đó")
            
            elif word[-1] in banned_word and str(message.author.id) in dumb:
                await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                await message.channel.send(f"Từ mày vừa nối có kí tự cuối là `{word[-1]}` (Đã bị ban)")
            elif word[-1] in banned_word :
                await message.add_reaction('❌')
                await message.channel.send(f"Từ bạn vừa nối có kí tự cuối là `{word[-1]}` (Đã bị ban)")
                    
            elif word not in english_words and str(message.author.id) in dumb:
                await message.add_reaction('<:lebronsunshinecover:1236337168809721948>')
                await message.channel.send(f"Từ `{word}` không tồn tại trong từ điển, thằng ngu!")
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"Từ `{word}` không tồn tại trong từ điển!")
        else:
            pass

    await bot.process_commands(message)

#Slash Command

@bot.event
async def on_ready():
    print("This bot is usable now")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
@bot.tree.command(name="help",description="Cảm thấy khó dùng...?")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("Ko bé oi")

@bot.tree.command(name="say",description="say something...")
@app_commands.describe(thing_to_say = "lmao")
async def say(interaciton: discord.Interaction, thing_to_say: str):
    await interaciton.response.send_message(f"{thing_to_say}")

@bot.tree.command(name="set_channel", description="Đặt channel nối từ")
async def set_channel(interaction: discord.Interaction):
    global word_channel_id
    if interaction.user.guild_permissions.administrator:
        word_channel_id.append(interaction.channel_id)
        word_channel_id = list(set(word_channel_id))
        save_channel_id(word_channel_id, word_channel_filename)
        await interaction.response.send_message(content="Đã đặt channel nối từ!")
    else:
        await interaction.response.send_message(content="Bạn cần có quyền admin để thực hiện lệnh này!")
        
@bot.tree.command(name="reset_game",description="Reset các từ đã nối")
async def reset_game(interaction:discord.Interaction):
    global current_word
    global used_words
    global last_word_id
    global connectable
    global reset_in_progress

    if interaction.user.guild_permissions.administrator:
        reset_in_progress = True
        
        await interaction.response.send_message(f"<@{interaction.user.id}> ARE YOU SURE ABOUT THAT??(y/n)")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            while True:
                message = await bot.wait_for('message', check=check, timeout=15.0)
                response = message.content.lower().strip()

                if response == "y":
                    current_word = ''
                    used_words = []
                    clear_used_words(used_words_filename)
                    last_word_id = ""
                    clear_last_id(last_word_id_filename)
                    connectable = False
                    save_connect(connectable, connect_filename)
                    await interaction.channel.send("Đã reset game!")
                    reset_in_progress = False
                    break
                elif response == "n":
                    await interaction.channel.send("Đã huỷ quá trình reset!")
                    reset_in_progress = False
                    break
        except asyncio.TimeoutError:
            await interaction.channel.send("Đã huỷ quá trình reset! (Hết thời gian)")
            reset_in_progress = False
                
    else:
        await interaction.response.send_message("Bạn cần có quyền admin để thực hiện lệnh này!")
        
@bot.tree.command(name="remove_channel",description="Reset channel nối từ")
async def remove_channel(interaction:discord.Interaction):
    global word_channel_filename
    
    if interaction.user.guild_permissions.administrator:
        remove_channel_id(interaction.channel.id,word_channel_filename)
        await interaction.response.send_message("Đã remove channel nối từ!")
    else:
        await interaction.response.send_message("Bạn cần có quyền admin để thực hiện lệnh này!")

@bot.tree.command(name="toggle_connect",description="Bật hoặc tắt nối từ liên tiếp")
async def toggle_connect(interaction:discord.Interaction):
    global connectable
    
    if interaction.user.guild_permissions.administrator:
        if str(connectable) == "False":
            connectable = True
            save_connect(connectable,connect_filename)
            await interaction.response.send_message("Người chơi bây giờ **__có thể__** nối từ hai lần liên tiếp!")
        elif str(connectable) == "True":
            connectable = False
            save_connect(connectable,connect_filename)
            await interaction.response.send_message("Người chơi bây giờ **__không thể__** nối từ hai lần liên tiếp!")
    else:
        await interaction.response.send_message("Bạn cần có quyền admin để thực hiện lệnh này!")
        
@bot.tree.command(name="wtf",description="Thử đi thì biết.")
@app_commands.describe(user_id = "User id đầy đủ")
async def wtf(interaction:discord.Interaction,user_id:str):
    global dumb
    dumb.append(user_id)
    dumb = list(set(dumb))
    save_dumb(dumb,dumb_filename)
    await interaction.response.send_message("Done!")
        
@bot.tree.command(name="remove_wtf",description="Như tên")
@app_commands.describe(user_id = "User id đầy đủ")
async def remove_wtf(interaction:discord.Interaction,user_id:str):
    global dumb
    if user_id in dumb:
        dumb.remove(user_id)
        remove_dumb(user_id,dumb_filename)
        
    else:
        await interaction.response.send_message("Không tồn tại user này trong danh sách!")
    
@bot.tree.command(name="ban_word",description="Cấm nối từ có chứa kí tự cuối như trên")
@app_commands.describe(word_to_ban = "Kí tự muốn ban")
async def ban_word(interaction:discord.Interaction,word_to_ban:str):
    global banned_word
    
    if len(word_to_ban) == 1 and re.match("^[a-zA-Z]+$", word_to_ban) and word_to_ban not in banned_word:
        banned_word.append(word_to_ban)
        save_banned(banned_word,banned_filename)
        await interaction.response.send_message(f"Người chơi bây giờ **__không thể__** nối từ có kí tự `{word_to_ban}` ở cuối!")
    elif len(word_to_ban) == 1 and re.match("^[a-zA-Z]+$", word_to_ban) and word_to_ban in banned_word:
        await interaction.response.send_message(f"Kí tự `{word_to_ban}` đã bị ban trước đó")
    else:
        await interaction.response.send_message("Hãy nhập **__một__** kí tự hợp lệ (a-z)!")

@bot.tree.command(name="unban_word",description="Như tên")
@app_commands.describe(word_to_ban = "Kí tự muốn unban")
async def unban_word(interaction:discord.Interaction,word_to_ban:str):
    global banned_word
    
    if len(word_to_ban) == 1 and re.match("^[a-zA-Z]+$", word_to_ban) and word_to_ban in banned_word:
        banned_word.remove(word_to_ban)
        remove_banned(word_to_ban,banned_filename)
        await interaction.response.send_message(f"Người chơi bây giờ **__có thể__** nối từ có kí tự `{word_to_ban}` ở cuối!")
    elif len(word_to_ban) == 1 and re.match("^[a-zA-Z]+$", word_to_ban) and word_to_ban not in banned_word:
        await interaction.response.send_message(f"Từ `{word_to_ban}` chưa bị ban!")
    else:
        await interaction.response.send_message("Hãy nhập **__một__** kí tự hợp lệ (a-z)!")

@bot.tree.command(name="banned_list",description="Danh sách những kí tự bị ban!")
async def banned_list(interaction:discord.Interaction):
    A = []
    for i in banned_word:
        if i == "[" or i == "]":
            continue
        elif i == ",":
            continue
        else:
            A.append(i)
    l = ", ".join(A)
    if len(l) != 0:
        await interaction.response.send_message(f"Những chữ đã bị ban: {l}")
    else:
        await interaction.response.send_message("Chưa có gì ở đây!")
        
@bot.tree.command(name="unban_all",description="Unban tất cả các word bị ban")
async def unban_all(interaction:discord.Interaction):
    global banned_word
    
    banned_word = []
    clear_banned_word(banned_filename)
    await interaction.response.send_message("Đã unban all!")
    
# General

@bot.command()
async def ping(ctx):
    bot_latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{bot_latency}ms`")

@bot.tree.command(name="ping", description="Độ trễ của bot")
async def ping(interaction:discord.Interaction):
    bot_latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! `{bot_latency}ms`")

#Run
bot.run("YOUR_BOT_TOKEN")
