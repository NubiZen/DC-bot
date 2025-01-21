import os
import asyncio
import discord

token = "fffff"  # Masukkan token user Anda
replyMessage = 'Hallo Guys'
channelId = 984941796272521229  # Ganti dengan ID kanal valid
send_delay = 50  # Delay pengiriman pesan (dalam detik)
delete_delay = 100  # Delay penghapusan pesan (dalam detik)

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
        try:
            channel = self.get_channel(channelId)
            if channel is None:
                print("Invalid channel ID. Please check.")
                return

            # Kirim pesan terus-menerus sesuai waktu yang diatur
            for i, msg in enumerate(mainMessages):
                sent_message = await channel.send(msg.strip())  # Menghapus newline (\n)
                print(f'Sent message {i + 1} in #{channel.name}.')
                
                # Jadwalkan penghapusan pesan
                asyncio.create_task(self.delete_message_after(sent_message, delete_delay))
                
                # Tunggu sebelum mengirim pesan berikutnya
                await asyncio.sleep(send_delay)

        except Exception as e:
            print(f"Error: {e}")

    async def delete_message_after(self, message, delay):
        """Menghapus pesan setelah jeda tertentu."""
        await asyncio.sleep(delay)
        try:
            await message.delete()
            print(f'Deleted message: {message.content}')
        except discord.NotFound:
            print("Message already deleted or not found.")
        except Exception as e:
            print(f"Error while deleting message: {e}")

    async def on_message(self, message):
        # Balas pesan DM jika pengirim tidak ada di blacklist
        if isinstance(message.channel, discord.DMChannel) and message.author.id != self.user.id:
            with open('blacklist.txt', 'r', encoding='UTF-8') as file:
                if str(message.author.id) not in file.read():
                    try:
                        sent_message = await message.reply(replyMessage)
                        print(f'Replied to {message.author.name}.')
                        
                        # Jadwalkan penghapusan pesan DM
                        asyncio.create_task(self.delete_message_after(sent_message, delete_delay))
                        
                        # Tambahkan pengirim ke blacklist
                        with open('blacklist.txt', 'a', encoding='UTF-8') as file:
                            file.write(f'{message.author.id}\n')
                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == '__main__':
    intents = discord.Intents.default()
    client = Main(intents=intents)
    client.run(token, bot=False)