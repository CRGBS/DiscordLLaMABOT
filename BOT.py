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
async def open_exe_file():
    global process, collected_text
    # edit to your llamacpp location
    command = "title MH8BOT & J:/GPTAI/llamacpp/mainMH8.exe -m zh-models/13B/ggml-model-q5_0.bin -f prompts/alpaca.txt -ins"
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
                async with client.get_channel(CHANNEL_ID).typing():
                    print(decoded_output)

                    # 判斷訊息是否為第一次輸入
                    if collected_text is None:
                        collected_text = decoded_output
                        embed = discord.Embed(title="Thinking..", description=collected_text)
                        msgr = await client.get_channel(CHANNEL_ID).send(embed=embed)
                    
                        #msgr = await client.get_channel(CHANNEL_ID).send(f'Replay：{collected_text}')
                    else:
                        collected_text += decoded_output
                        embed = discord.Embed(title="answer:", description=collected_text)
                        await msgr.edit(embed=embed)
                    
                        #await msgr.edit(content=f'Reply：{collected_text}')
                    

async def send_command(cmd):
    global process, collected_text
    if process is None:
        await open_exe_file()
    if process.returncode is None:
        question = cmd
        intext = cmd.encode('utf-8') + b'\n'
        process.stdin.write(intext)
        print(f"cmd: {cmd}")
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
            await message.channel.send('Let me thing.. 🤔')
            cmd = message.content.split(f'<@{client.user.id}>')[1].strip()
            await send_command(cmd)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await open_exe_file()

client.run(BOT_TOKEN)
