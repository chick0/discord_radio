# -*- coding: utf-8 -*-

from discord.ext import commands
from discord.abc import PrivateChannel

from discord.errors import ClientException

from module.worker import Radio


def is_public(ctx: commands.context):
    return not isinstance(
        ctx.message.channel,
        PrivateChannel
    )


class Command(commands.Cog, name="라디오 조작 명령어"):
    @commands.command(help="지정한 음악을 재생합니다")
    @commands.cooldown(3, 10, commands.BucketType.guild)
    @commands.check(is_public)
    async def play(self, ctx: commands.context, index: int):
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except AttributeError:
            await ctx.reply("```\n"
                            "먼저 음성 채널에 들어가야 합니다.\n"
                            "```")
            return
        except ClientException as why:
            await ctx.reply("```\n"
                            "음성 채널 접속에 실패하였습니다.\n"
                            f"> {why}\n"
                            "```")
            return

        radio = Radio(ctx=ctx, voice_client=voice_client)
        radio.set_start(index=index)

    @commands.command(help="음성 채널에 들어옵니다 (라디오 시작)")
    @commands.cooldown(3, 10, commands.BucketType.guild)
    @commands.check(is_public)
    async def join(self, ctx: commands.context, option: str = None):
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except AttributeError:
            await ctx.reply("```\n"
                            "먼저 음성 채널에 들어가야 합니다.\n"
                            "```")
            return
        except (ClientException, Exception) as why:
            await ctx.reply("```\n"
                            "음성 채널 접속에 실패하였습니다.\n"
                            f"> {why}\n"
                            "```")
            return

        if option in ["now", "np"]:
            radio = Radio(ctx=ctx, voice_client=voice_client, np=True)
        else:
            radio = Radio(ctx=ctx, voice_client=voice_client)

        radio.play_next(error=None)

    @commands.command(help="음성 채널에서 나갑니다 (라디오 종료)")
    @commands.check(is_public)
    async def exit(self, ctx: commands.context):
        try:
            if ctx.author.voice.channel.id == ctx.guild.voice_client.channel.id:
                await ctx.guild.voice_client.disconnect()
            else:
                await ctx.reply("```\n"
                                "봇이랑 동일한 음성 채널에 들어와야합니다.\n"
                                "```")
        except AttributeError:
            pass

    @commands.command(help="음성 채널에서 나갔다가 들어옵니다")
    @commands.check(is_public)
    async def re(self, ctx: commands.context):
        try:
            if ctx.author.voice.channel.id == ctx.guild.voice_client.channel.id:
                channel = ctx.guild.voice_client.channel
                await ctx.guild.voice_client.disconnect()

                voice_client = await channel.connect()

                radio = Radio(ctx=ctx, voice_client=voice_client)
                radio.play_next(error=None)
            else:
                await ctx.reply("```\n"
                                "봇이랑 동일한 음성 채널에 들어와야합니다.\n"
                                "```")
        except AttributeError:
            pass

    @commands.command(help="다음 노래로 넘깁니다")
    @commands.cooldown(3, 10, commands.BucketType.guild)
    @commands.check(is_public)
    async def skip(self, ctx: commands.context):
        try:
            if ctx.author.voice.channel.id == ctx.guild.voice_client.channel.id:
                await ctx.guild.voice_client.stop()
            else:
                await ctx.reply("```\n"
                                "봇이랑 동일한 음성 채널에 들어와야합니다.\n"
                                "```")
        except (AttributeError, TypeError):
            pass
