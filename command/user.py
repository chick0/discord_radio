# -*- coding: utf-8 -*-
from io import StringIO
from os import path, listdir
from hashlib import md5

from discord import File
from discord.ext import commands
from discord.errors import Forbidden

from module.url import get_link


class Command(commands.Cog, name="모든 유저들을 위한 명령어"):
    @commands.command(help="접속하고 있는 길드(서버)를 알려줍니다")
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def guilds(self, ctx: commands.context):
        await ctx.reply(
            "```\n"
            f" - ( {len(ctx.bot.guilds)} ) 개의 길드에 연결됨,\n"
            f"   ( {ctx.bot.shard_count} ) 개의 샤드를 사용중"
            "```"
        )

    @commands.command(help="개인메시지로 봇 초대 링크를 보냅니다")
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def invite(self, ctx: commands.context):
        try:
            await ctx.author.send(
                "> 봇 초대 링크\n"
                f"{get_link(bot=ctx.bot)}"
            )
        except Forbidden:
            await ctx.reply(
                f"`{get_link(bot=ctx.bot)}`"
            )

    @commands.command(help="라디오가 작동 중인 길드를 확인합니다")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def status(self, ctx: commands.context):
        await ctx.reply("```\n"
                        f"( {len(ctx.bot.voice_clients)} )개의 서버에서 작동중\n"
                        "```")

    @commands.command(help="재생목록을 확인합니다")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def playlist(self, ctx: commands.context):
        playlist, index = "", 0
        for music in listdir(path.join("music")):
            if music.endswith(".mp3"):
                playlist += f"[{index:03d}] {music}\n"
                index += 1
        await ctx.reply(content=f"재생목록 버전: `{md5(playlist.encode()).hexdigest()}`",
                        file=File(fp=StringIO(playlist),
                                  filename="playlist.txt"))
