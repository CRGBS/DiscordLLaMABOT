import subprocess
import asyncio
import discord
import os

###EDIT IT
CHANNEL_ID = INPUTURCHANNELID
BOT_TOKEN = "INPUTURTOKEN"
ROLE = 'inputurrole'
###

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)

# 定義變數，用來紀錄蒐集到的文字
collected_text = ''
process = None
msgr = None   # 声明变量 msgr 并初始化为 None 对象

async def open_exe_file():
    global process, collected_text
    # edit to your llamacpp location
    command = "title MH8BOT & J:/GPTAI/llamacpp/main.exe -m zh-models/13B/ggml-model-q5_0.bin -f prompts/alpaca.txt -ins -c 2048 --temp 0.2 -n 256 -t 7 --top_k 40 --top_p 0.5 --repeat_last_n 256 --batch_size 1024 --repeat_penalty 1.17647 --temp 0.68"
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    while True:
        # 檢查進程是否已經停止
        if process.returncode is not None:
            break

        output = await process.stdout.read(512)
        if output:
            decoded_output = output.decode('utf-8', errors='replace').rstrip()
            if decoded_output.strip():
                print(decoded_output)

                # 判斷訊息是否為第一次輸入
                if collected_text == '':
                    collected_text = decoded_output
                    msgr = await client.get_channel(CHANNEL_ID).send(f'FR：{collected_text}')
                else:
                    collected_text += decoded_output
                    await msgr.edit(content=f'NR：{collected_text}')
                    
async def send_command(cmd):
    global process, collected_text
    if process is None:
        await open_exe_file()
    if process.returncode is None:
        intext = cmd.encode('utf-8')
        process.stdin.write(intext)
        print(f'Received command: {intext}')
        await process.stdin.drain()
        collected_text = ''
        msgr = ''

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        if not any(role.name == ROLE for role in message.author.roles):
            await message.channel.send('只有至高無上的月球指名能指使我做事!!')
            return
        else:
            await message.channel.send('Let Me Think 🤔')
            cmd = message.content.split(f'<@{client.user.id}>')[1].strip()
            await send_command(cmd)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await open_exe_file()

client.run(BOT_TOKEN)
