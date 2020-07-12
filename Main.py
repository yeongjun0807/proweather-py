import re
import Get
import smtplib
import asyncio
from discord import *
from email.mime.text import MIMEText
from time import sleep
from random import randint
from discord.ext import commands
from threading import Thread
from captcha.image import ImageCaptcha

bot = commands.Bot(command_prefix = '/')
bot.remove_command('help')

Cooltime = 0
MAX_COOLTIME = 20
Token = Get.GET_TOKEN()

@bot.event
async def on_ready():
    global channel
    
    await bot.change_presence(status = Status.online, activity = Game("Questions & Commands"))
    print("디스코드 봇 로그인이 완료되었습니다")
    print("디스코드 봇 이름 : " + bot.user.name)
    print("디스코드 봇 ID : " + str(bot.user.id))
    print("디스코드 봇 버전  : " + Get.GET_VERSION())

    channel = bot.get_channel(728197481002827828)
    bot.loop.create_task(Back_Task())

async def Back_Task():
    await bot.wait_until_ready()

    while True:
        await channel.send("hi")
        await asyncio.sleep(60*60*24)

@bot.event
async def on_typing(channel, user, when):
    global Cooltime
    
    if Cooltime == 0:
        await channel.send(f"{str(user)}님이 작성중입니다")
        Cooltime = MAX_COOLTIME

'''@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    await channel.send(str(message.author) + f"이/가 메세지를 삭제하였습니다 : '{message.content}'")'''

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    
    await channel.send(f"{before.author}이/가 {before.content}에서 {after.content}로 변경하였습니다")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    await channel.send(f"{user}이/가 {reaction.emoji}반응을 추가하였습니다")

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return

    await channel.send(f"{user}이/가 {reaction.emoji}반응을 제거하였습니다")

@bot.event
async def on_member_join(member):
    rolename = utils.get(member.guild.roles, name = "신입")

    if not rolename:
        return

    await member.add_roles(rolename)
    await member.send("안녕하신가 휴먼, 우리 서버에 오신것을 환영한다")
    await channel.send(f"{member}이/가 우리 서버에 오셨습니다")

@bot.event
async def on_member_remove(member):
    await member.send("잘가라, 휴먼")

@bot.event
async def on_member_update(before, after):
    change = []
    nick = after.nick

    if after.nick == None and before.nick == None:
        #await channel.send(f"누군가 ")
        return
    
    elif before.nick != after.nick:
        change.extend([before.nick, after.nick])

    elif before.status != after.status:
        change.extend([before.status, after.status])

    elif before.activity != after.activity:
        change.extend([before.activity, after.activity])

    await channel.send(f"{nick}이/가 {change[0]}에서 {change[1]}로 프로필을 바꾸었습니다")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    message_content = message.content

    regex = re.compile("씨발|개새끼|닥쳐|꺼져|미친|ㅆㅂ|ㅁㅊ|바보|ㅂㅂ|fuck|려차", re.I)
    match = regex.search(message_content)

    if message.author.bot:
        if message_content == "Hi":
            reaction_list = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤"]

            for i in reaction_list:
                await message.add_reaction(i)

    if match:
        await message.channel.send("바르고 고운말을 사용해라, 휴먼")
        await message.delete()
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')


@bot.command()
async def Tts(ctx, message):
    await ctx.send(message, tts = True)

@bot.command()
async def hi(ctx):
    await ctx.send("안녕하신가, 휴먼")

@bot.command()
async def clear(ctx, amount = 1000):
    
    await ctx.channel.purge(limit = amount)

@bot.command()
async def name(ctx):
    await ctx.send("제 이름은 KANG입니다, 휴먼")

@bot.command()
async def speak(ctx, message):
    await ctx.send(f"{ctx.author.mention}, {message}")

@bot.command()
async def token(ctx, secretcode = None, mail = None, type = None):
    if not secretcode:
        await channel.send(embed = Embed(title="시크릿 코드 없음", description = """시크릿 코드를 입력해 주세요
                                                                                    시크릿 코드가 없다면 토큰을 발급받을 수 없습니다.""", color = 0xff0000))
        return
    
    elif secretcode == "a152b":
        await ctx.channel.purge(limit = 1)
        Captcha = ImageCaptcha()
    
        Str = ''

        for _ in range(6):
            Str += str(randint(0, 9))

        ImageName = "Captcha/" + str(randint(10000000, 99999999)) + ".png"
        Captcha.write(Str, ImageName)

        await ctx.channel.send(file = File(ImageName))

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            message = await bot.wait_for("message", timeout = 60, check = check)
        except:
            await ctx.channel.send(embed = Embed(title = "시간초과입니다", description = """시간초과입니다
            토큰을 발급받을 수 없습니다""", color = 0xff0000))
            return

        if message.content == Str:
            await ctx.channel.send(embed = Embed(title="정답입니다", description = "정답입니다", color = 0x00ff00))
        else:
            await ctx.channel.send(embed = Embed(title="오답입니다", description = """오답입니다
            토큰을 발급받을 수 없습니다""", color = 0xff0000))
            return

        await ctx.channel.send(embed = Embed(title = "토큰을 발급하는 중입니다", description = """토큰을 발급하는 중입니다....
                                                                                                최대 30초 정도가 걸릴 수 있습니다."""))

        sleep(randint(1, 3))
        Secret_token = Get.GET_SECRET_TOKEN()
        Delete_SECRET_TOKEN = Thread(target = Delete_secret_token)
        Delete_SECRET_TOKEN.start()

        if mail:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login("kangkangii0101@gmail.com", "kangkang0101")
            
            msg = MIMEText(f"""시크릿 토큰입니다.\n{Secret_token}""")
            msg["Subject"] = "시크릿 토큰입니다"
            msg["To"] = mail
            smtp.sendmail("kangkangii0101@gmail.com", mail, msg.as_string())
            
            smtp.quit()

        await ctx.channel.send(embed = Embed(title = "토큰이 발급되었습니다", description = """토큰을 1분내로 입력해 주세요
        토큰은 1분후에 만료됩니다."""))
        return

    else:
        await ctx.channel.send(embed = Embed(title="시크릿 코드 틀림", description = "시크릿 코드가 틀렸습니다", color = 0xff0000))
        return  

@bot.command()
async def kick(ctx, user : Member, secrettoken = None, reason = None):
    if ctx.author.guild_permissions.kick_members:
        FileOpen = open("Secret_token.txt", "r", encoding = "utf-8")
        FileRead = FileOpen.read()

        if not FileRead:
            await channel.send(embed = Embed(title="토큰이 아직 없습니다.", description = """토큰을 아직 발급하지 않았습니다.
            토큰을 발급해주세요.""", color = 0xff0000))
            return

        elif FileRead[0] == '!':
            await channel.send(embed = Embed(title="토큰이 만료됨", description = """토큰이 만료되었습니다.
            새로운 토큰을 발급해주세요.""", color = 0xff0000))
            return
        
        elif not secrettoken:
            await channel.send(embed = Embed(title="토큰 오류", description = """토큰을 입력해주세요""", color = 0xff0000))
            return

        elif secrettoken == FileRead:
            await ctx.channel.purge(limit = 1)
            await user.send(embed = Embed(title="킥 당하셨습니다.", description = f"당신은 {ctx.author} 님에게 {ctx.guild.name} 서버에서 킥당하셨습니다. 이유:```{reason}```", color = 0x00ff00))
            await user.kick(reason = reason)
            await ctx.channel.send(embed = Embed(title="킥 성공", description = f"{ctx.author} 님이 {user} 님을 이 서버에서 킥하셨습니다. 이유:```{reason}```", color = 0x00ff00))

        else:
            await ctx.channel.send(embed = Embed(title="토큰이 틀렸습니다.", description = """토큰이 틀렸습니다.
            다시 입력해주세요.""", color = 0xff0000))

    else:
        await ctx.channel.send(embed = Embed(title="권한 부족", description = f"{ctx.author.mention}님은 유저를 킥할 수 있는 권한이 없습니다.", color = 0xff0000))
        return

@bot.command()
async def info(ctx):
    embed = Embed(name = "KANG", title = "봇 정보", colour = Colour.blurple(), description = "봇입니다.")
    embed.set_thumbnail(url = "https://media.discordapp.net/attachments/724928149036597370/726457061289885807/e6b870e262e6df09.jpg")

    await ctx.send(embed = embed)

@bot.command()
async def RSP(ctx):
    def RSP(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.channel.send("가위")
    sleep(1)
    await ctx.channel.send("바위")
    sleep(1)
    await ctx.channel.send("보")
    sleep(1)
    message = await bot.wait_for("message", check = RSP)

    if message.content == '가위' or message == '바위' or message == '보':
        await ctx.channel.send("ff")

@bot.command()
async def dm(ctx, user : Member, content):
    await user.send(content)

@bot.command()
async def clashroyale(ctx):
    await ctx.channel.send("```미완성입니다.```")

@bot.command()
async def setrole(ctx, user : Member, role):
    rolename = utils.get(ctx.guild.roles, name = role)

    if not rolename:
        await ctx.channel.send(embed = Embed(title = "역할이 없습니다.", description = f"{role}이라는 역할이 없습니다.", color = 0xff0000))
        return

    try:
        await user.add_roles(rolename)
    except discord.errors.Forbidden:
        await ctx.channel.send(embed = Embed(title="권한 부족", description = f"{ctx.author.mention}님은 유저의 역할을 바꿀 수 있는 권한이 없습니다.", color = 0xff0000))
        return
    
    await ctx.channel.send(f"{ctx.author}이/가 {user}에게 {rolename} 역할을 부여하셨습니다.")

@bot.command()
async def test(ctx):
    return

@bot.command()
async def status(ctx, user : Member):
    if not user.activities:
        await ctx.channel.send(f"{user}은/는 오프라인입니다")
    
    else:
        await ctx.channel.send(f"{user}은/는 온라인입니다")

@bot.command()
async def help(ctx):
    await ctx.channel.send("""```hi : 인사
/info : 봇 정보
/dm (user, content) : (user)에게 (content)를 보냄
/kick (user, secretcode, [reason]) : (user)를 kick 함, 이유 : (reason)```""")

@bot.command()
async def captcha(ctx):
    Captcha = ImageCaptcha()
    
    Str = ''

    for _ in range(6):
        Str += str(randint(0, 9))

    ImageName = "Captcha/" + str(randint(10000000, 99999999)) + ".png"
    Captcha.write(Str, ImageName)

    await ctx.channel.send(file = File(ImageName))

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await bot.wait_for("message", timeout = 60, check = check)
    except:
        await ctx.channel.send("시간초과입니다")
        return

    if message.content == Str:
        await ctx.channel.send("정답입니다")
    else:
        await ctx.channel.send("오답입니다")

def SetCoolTime():
    global Cooltime

    while True:
        if Cooltime != 0:
            sleep(1)
            Cooltime -= 1

def Delete_secret_token():
    FileOpen = open("Secret_token.txt", "r", encoding = "utf-8")
    FileRead = FileOpen.read()
    Token_Delete = 60

    while True:
        if not FileRead or FileRead[0] == '!' or Token_Delete == 0:
            FileOpen.close()
            FileOpen = open("Secret_token.txt", "w", encoding = "utf-8")
            FileOpen.write('!' + FileRead)

            return

        Token_Delete -= 1
        sleep(1)


SCTTRD = Thread(target = SetCoolTime)
SCTTRD.start()

bot.run(Token)