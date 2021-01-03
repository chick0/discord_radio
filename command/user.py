# -*- coding: utf-8 -*-

from discord.ext import commands

from module.url import get_link


class Command(commands.Cog, name="모든 유저들을 위한 명령어"):
    @commands.command(help="접속하고 있는 길드(서버)를 알려줍니다")
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def guilds(self, ctx: commands.context):
        await ctx.send(
            "```\n"
            f" - ( {len(ctx.bot.guilds)} ) 개의 길드에 연결됨,\n"
            f"   ( {ctx.bot.shard_count} ) 개의 샤드를 사용중"
            "```"
        )

    @commands.command(help="개인메시지로 봇 초대 링크를 보냅니다")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def invite(self, ctx: commands.context):
        await ctx.author.send(
            "> 봇 초대 링크\n"
            f"{get_link(bot=ctx.bot)}"
        )
