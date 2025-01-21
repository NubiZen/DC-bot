import os
import asyncio
import discord

token = "fffff"  # Masukkan token user Anda
replyMessage = 'Hallo Guys'
channelId = 984941796272521229  # Ganti dengan ID kanal valid
send_delay = 50  # Delay pengiriman pesan
delete_delay = 100  # Delay penghapusan pesan

# Fungsi untuk membaca pesan dari file eksternal
def load_messages_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='UTF-8') as file:
            return file.readlines()
    else:
        print(f"File {file_name} tidak ditemukan.")
        return []

# Mengambil pesan dari file 'messages.txt'
mainMessages = load_messages_from_file('messages.txt')

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

                # Kirimkan satu pesan pada satu waktu
                for i, msg in enumerate(mainMessages):
                    # Kirim pesan dari file
                    sent_message = await channel.send(msg.strip())  # Menghapus newline (\n)
                    print(f'Sent message {i + 1} in #{channel.name}.')
                    await asyncio.sleep(delete_delay)  # Tunggu untuk penghapusan pesan
                    await sent_message.delete()  # Hapus pesan setelah delay
                    await asyncio.sleep(send_delay)  # Tunggu sebelum mengirim pesan selanjutnya

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
                        await asyncio.sleep(delete_delay)  # Tunggu sebelum menghapus pesan
                        await sent_message.delete()  # Hapus pesan setelah reply
                        with open('blacklist.txt', 'a', encoding='UTF-8') as file:
                            file.write(f'{message.author.id}\n')
                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == '__main__':
    intents = discord.Intents.default()
    client = Main(intents=intents)
    client.run(token, bot=False)