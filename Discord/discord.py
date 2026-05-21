import os
import discord
from core.config import BOT_TOKEN, USER_ID

DATA_PATH = "data"
MAX_SIZE = 25 * 1024 * 1024  # 25MB

class MyClient(discord.Client):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")


client = MyClient()


async def send_zips_handler(interaction: discord.Interaction) -> None:
    zip_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".zip")]

    if not zip_files:
        await interaction.response.send_message("Nenhum arquivo .zip encontrado.")
        return

    await interaction.response.send_message(f"Enviando {len(zip_files)} arquivo(s)...")

    for filename in zip_files:
        path = os.path.join(DATA_PATH, filename)
        if os.path.getsize(path) > MAX_SIZE:
            await interaction.followup.send(f"⚠️ `{filename}` ultrapassa 25MB, pulando...")
            continue
        await interaction.followup.send(
            file=discord.File(path, filename=filename)
        )


@client.tree.command(name="send_zips", description="Envia todos os zips da pasta data")
async def send_zips(interaction: discord.Interaction) -> None:
    await send_zips_handler(interaction)


if __name__ == "__main__":
    client.run(BOT_TOKEN)