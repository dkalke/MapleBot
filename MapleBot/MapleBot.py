
import discord
from discord.ext import tasks
from datetime import datetime
import os
import sched
from dotenv import load_dotenv


# 每個List需要維持一樣的index
channel_list = []
mention_list = []
status_list = []

@tasks.loop(seconds=60)
async def HitTheBoss():
  time = datetime.now().strftime("%M")
  print(time)
  try:
    if time == '28' or time == '58':
      for channel in channel_list:
        index = channel_list.index(channel)
        if status_list[index]:
          msg = ''
          for i in mention_list[index]:
            msg += i + ' '
          await channel.send(msg + "打影子拉!")
  except AttributeError as e:
    print("沒有設定頻道!")


load_dotenv()
client = discord.Client()
HitTheBoss.start()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  try:
    if message.content.startswith('$開始提醒'):
      status_list[channel_list.index(message.channel)] = True
      await message.channel.send('Start!')

    elif message.content.startswith('$停止提醒'):
      status_list[channel_list.index(message.channel)] = False
      await message.channel.send('Stop!')
    
    elif message.content.startswith('$新增人員'):
      mention_list[channel_list.index(message.channel)].append(message.author.mention)
      await message.channel.send('Add Done!')

    elif message.content.startswith('$刪除人員'):
      mention_list[channel_list.index(message.channel)].remove(message.author.mention)
      await message.channel.send('Delete Done!')

    elif message.content.startswith('$人員列表'):
      msg = ''
      for i in mention_list[channel_list.index(message.channel)]:
        msg += i + ''
      await message.channel.send('現在提醒的人有 ' + msg)

    elif message.content.startswith('$新增頻道'):
      channel_list.append(message.channel)
      mention_list.append([])
      status_list.append(True)
      await message.channel.send('Channel Done!')

    elif message.content.startswith('$刪除頻道'):
      index = channel_list.index(message.channel)
      del channel_list[index]
      del mention_list[index]
      del status_list[index]
      await message.channel.send('Channel Done!')
  except ValueError as e:
      await message.channel.send('頻道/人員不存在!')

client.run(os.getenv('TOKEN'))

