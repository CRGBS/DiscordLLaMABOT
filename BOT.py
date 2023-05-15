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

# 定義變數
collected_text, process, msgr = None, None, None
#TODO 讓中文能被正確交互
async def open_exe_file():
    global process, collected_text
    # edit to your llamacpp location
    command = "title MH8BOT & J:/GPTAI/llamacpp/main.exe -m zh-models/13B/ggml-model-q5_0.bin -f prompts/alpaca.txt -ins -c 2048 --keep 2048 -n 512 -t 7 --mlock --memory_f32 --top_k 40 --top_p 0.53 --repeat_last_n 256 --batch_size 1024 --repeat_penalty 1.17647 --temp 0.667"
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE
    )

    while True:
        # 檢查進程是否已經停止
        if process.returncode is not None:
            break

        output = await process.stdout.read(512)
        if output:
            decoded_output = output.decode('utf-8', errors='replace')#.rstrip()
            if decoded_output.strip():
                print(decoded_output)

                # 判斷訊息是否為第一次輸入
                if collected_text is None:
                    collected_text = decoded_output
                    msgr = await client.get_channel(CHANNEL_ID).send(f'Replay：{collected_text}')
                else:
                    collected_text += decoded_output
                    await msgr.edit(content=f'Reply：{collected_text}')
                    

async def send_command(cmd):
    global process, collected_text
    if process is None:
        await open_exe_file()
    if process.returncode is None:
        intext = cmd.encode('utf-8') + b'/n'
        process.stdin.write(intext)
        print(f"Received command: {intext}")
        await process.stdin.drain()
        collected_text, msgr = None, None

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        if not any(role.name == ROLE for role in message.author.roles):
            await message.channel.send('Role Denied!!')
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
