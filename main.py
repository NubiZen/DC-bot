import os
import asyncio
import discord

token = "your_user_token"  # Masukkan token user Anda
replyMessage = 'Hallo Guys'
channelId = 182651  # Ganti dengan ID kanal valid
send_delay = 50  # Delay pengiriman pesan
delete_delay = 7  # Delay penghapusan pesan

mainMessages = [
    'Welcome to everyone that just joined!',
    'Let’s go guys, keep it up!',
    'Be active!',
    'How can you guys type so fast?',
    'You guys still grinding here?',
    'Stay motivated and never give up!',
    'Remember, success takes time and effort.',
    'Let’s build a great community here!',
    'Don’t forget to help each other out.',
    'Who’s ready for some challenges?',
    'Keep pushing forward, no matter what!',
    'Teamwork makes the dream work!',
    'Any fun stories to share today?',
    'What are you guys working on right now?',
    'Consistency is the key to success!',
    'Don’t be shy, let’s chat!',
    'Let’s make today productive!',
    'Always remember to take breaks!',
    'You guys are doing great, keep going!',
    'The grind never stops, let’s go!',
]

class Main(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists('blacklist.txt'):
            with open('blacklist.txt', 'w', encoding='UTF-8'):
                pass

    async def on_ready(self):
        print(f'Logged in as {self.user}.')
        while True:
            try:
                channel = self.get_channel(channelId)
                if channel is None:
                    print("Invalid channel ID. Please check.")
                    break
                for i, msg in enumerate(mainMessages):
                    sent_message = await channel.send(msg)
                    print(f'Sent message {i + 1} in #{channel.name}.')
                    await asyncio.sleep(send_delay) 
                    await sent_message.delete()  
                    await asyncio.sleep(delete_delay)  
            except Exception as e:
                print(f"Error: {e}")
                break

    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and message.author.id != self.user.id:
            with open('blacklist.txt', 'r', encoding='UTF-8') as file:
                if str(message.author.id) not in file.read():
                    try:
                        sent_message = await message.reply(replyMessage)
                        print(f'Replied to {message.author.name}.')
                        await asyncio.sleep(delete_delay) 
                        await sent_message.delete() 
                        with open('blacklist.txt', 'a', encoding='UTF-8') as file:
                            file.write(f'{message.author.id}\n')
                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == '__main__':
    intents = discord.Intents.default()
    client = Main(intents=intents)
    client.run(token, bot=False) 