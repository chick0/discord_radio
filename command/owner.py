# -*- coding: utf-8 -*-

from discord.ext import commands


class Command(commands.Cog, name="관리자용 명령어"):
    @commands.command(help="봇을 종료합니다", hidden=True)
    @commands.is_owner()
    async def close(self, ctx: commands.context):
        await ctx.send(":wave:")
        await ctx.bot.close()

    @commands.command(help="모든 음성 채널에서 나갑니다", hidden=True)
    @commands.is_owner()
    async def leave_all(self, ctx: commands.context):
        for voice_client in ctx.bot.voice_clients:
            await voice_client.disconnect()
