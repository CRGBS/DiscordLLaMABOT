import subprocess
import asyncio
import discord
import os
import re

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)
CHANNEL_ID = INPUTURCHANNELID
BOT_TOKEN = "INPUTURTOKEN"

process = None
async def open_exe_file():
    global proces
    s#edit to ur llamacpp location
    command = "J:/GPTAI/llamacpp/main.exe -m zh-models/13B/ggml-model-q5_0.bin --color -f prompts/alpaca.txt -ins -c 2048 --temp 0.2 -n 256 -t 16 --repeat_penalty 1.1 --temp 0.4"
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE, shell=True, env=os.environ
    )

    while True:
        # 檢查進程是否已經停止
        if process.returncode is not None:
            break

        output = await process.stdout.read(1024)
        if output:
            decoded_output = output.decode('big5', errors='replace').rstrip()
            if decoded_output.strip():
                # 移除 ansi 顏色代碼
                ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
                plain_text_output = ansi_escape.sub('', decoded_output)
                print(plain_text_output)
                if plain_text_output.strip():
                    await client.get_channel(CHANNEL_ID).send(plain_text_output)

    # 關閉標準輸出
    if process.stdout:
        process.stdout.close()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        await message.channel.send('hello，bot loading')
        cmd = message.content.split(f'<@{client.user.id}>')[1].strip()
        print(f'Received command: {cmd}')
        if process is not None:
            process.stdin.write(cmd.encode('utf-8') + b'\n')
            await process.stdin.drain()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    #global process
    #if process is None:
    await open_exe_file()
    #else:
    #    print('Exe file is opened:', process is not None)
    #asyncio.create_task(read_stdout())

client.run(BOT_TOKEN)
