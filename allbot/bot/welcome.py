import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
bot = commands.Bot(command_prefix="_", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

def get_random_color():
    return discord.Color(random.randint(0, 0xFFFFFF))

@bot.event
async def on_member_join(member):
    channel_id = 1243546262129737879  # Thay thế bằng ID kênh của bạn
    channel = bot.get_channel(channel_id)
    main_channel = 1155783568488927252
    main = bot.get_channel(main_channel)
    if channel:
        member_count = member.guild.member_count  # Đếm số lượng thành viên
        embed = discord.Embed(
            title="Welcome to Mẫu Giáo Lớn! \n Giờ bạn đã là thành viên mới của bang hội Mẫu Giáo Lớn nhưng trẻ trâu này rồi! \nCùng tạo cho nhau kỉ niệm đẹp nhé.",
            description=f"Chào {member.mention}, bạn là đứa con thứ {member_count} <33 \n Đừng ngại ghé qua các kênh dưới đây nhé.",
            color=get_random_color()
        )

        # thêm ảnh random vào embed
        img_ls = ['img_1.png', 'img_2.png','img_3.png']
        img_path = random.choice(img_ls)
        file = discord.File(img_path, filename="welcome.png")
        embed.set_image(url="attachment://welcome.png")
        view = discord.ui.View()

        button_rule = discord.ui.Button(label="Hãy đọc kỹ luật nhé", style=discord.ButtonStyle.link, url="https://discord.com/channels/1150823311954149426/1244588495108964403")  # Thay bằng URL thực của kênh luật
        button_newbie = discord.ui.Button(label="Kênh tân thủ", style=discord.ButtonStyle.link, url="https://discord.com/channels/1150823311954149426/1245431596698439741")  # Thay bằng URL thực của kênh tân thủ
        button_chat = discord.ui.Button(label="Kênh Chat Nè", style=discord.ButtonStyle.link, url="https://discord.com/channels/1150823311954149426/1155783568488927252")  # Thay bằng URL thực của kênh chat

        view.add_item(button_rule)
        view.add_item(button_newbie)
        view.add_item(button_chat)

        ms = await channel.send(embed=embed, file=file, view=view)  # Gửi tin nhắn kèm file và view
        await ms.add_reaction("👋")
        await ms.add_reaction("🎉")
        await ms.add_reaction("🎈")
        await ms.add_reaction("🎊")
        tag_role = discord.utils.get(member.guild.roles, name="Lễ Tân")
        mess_tag = discord.Embed(
            title="Chao Xìn",
            description=f"{tag_role.mention} Tiếp đón bạn {member.mention} đi nèeeeeeeeee <3",
            color=get_random_color()
        )
        await main.send(embed=mess_tag)
        await channel.send(f"Mẫu Giáo Lớn xin chào {member.mention} nhesssss <3")



@bot.command()
async def wlc(ctx):
    await ctx.send("Chào mừng bạn đến với Mẫu Giáo Lớn nhaaaaaaaa! \nĐừng ngần ngại tham gia các kênh voice và chat để giao lưu với mọi người nhé <3")



bot.run()
