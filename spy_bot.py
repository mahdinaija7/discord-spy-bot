import discord
import asyncio
import requests
import os

client = discord.Client()
#checking if image folder exist
if not os.path.isdir("./images"):
    try:
        os.mkdir("images")
    except OSError:
        print("Creation of the directory Images failed")
        exit(1)
    else:
        print("Successfully created the Images")

#parsing bot configs
def get_configs():
    try:
        with open("config.txt","r",encoding="utf-8") as config:
            lines = list(map(lambda x:x.strip(),config.readlines()))
            return lines[0].split(" "),lines[1].split(" "),lines[2]
    except IndexError:
        print("Please Check The Target File")
        exit(1)





@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



#copy every message from a channel and send to the target channel
@client.event
async def on_message(message):
    msg_channel_id=str(message.channel.id)
    if  message.author != client.user and msg_channel_id in from_channels_id :
            target_channel_id=dict_tokens[msg_channel_id]
            to_channel_name = client.get_channel(int(target_channel_id))
            if message.embeds:
                embed = message.embeds[0]
                if embed.type=="gifv":
                    await to_channel_name.send(message.content)
                else:
                    await to_channel_name.send(embed=embed)
                return
            try:
                image = message.attachments[0].url
            except IndexError:
                image = None

            if not image :
                await to_channel_name.send(message.content)
            else:
                response = requests.get(message.attachments[0].url, stream=True)
                response.raise_for_status()
                with open("./images/"+message.attachments[0].filename,"wb") as image_file_hand:
                    for block in response.iter_content(1024):
                        image_file_hand.write(block)
                image_file=discord.File("images/"+message.attachments[0].filename)
                await to_channel_name.send(message.content,file=image_file)



async def main_func():
    await client.start(discord_token, bot=True)

if __name__=='__main__':
    from_channels_id,to_channels_id,discord_token=get_configs()
    dict_tokens=dict(zip(from_channels_id,to_channels_id))
    asyncio.get_event_loop().run_until_complete(main_func())
