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
    @commands.command(help="음성 채널에 들어옵니다 (라디오 시작)",
                      aliases=["j", "start", "켜기"])
    @commands.cooldown(3, 10, commands.BucketType.guild)
    @commands.check(is_public)
    async def join(self, ctx: commands.context, options: str = ""):
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

        np, index = False, None
        options = options.lower().split(",")
        for option in options:
            if option.startswith("np=true"):
                np = True
            if option.startswith("idx="):
                try:
                    index = int(option.split("=")[-1])
                except (ValueError, IndexError):
                    index = None

        radio = Radio(ctx=ctx, voice_client=voice_client, np=np)
        radio.start(index=index)

    @commands.command(help="음성 채널에서 나갑니다 (라디오 종료)",
                      aliases=["e", "leave", "나가기", "끄기"])
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
    @commands.cooldown(3, 5, commands.BucketType.guild)
    @commands.check(is_public)
    async def re(self, ctx: commands.context):
        try:
            if ctx.author.voice.channel.id == ctx.guild.voice_client.channel.id:
                channel = ctx.guild.voice_client.channel
                await ctx.guild.voice_client.disconnect()

                voice_client = await channel.connect()

                radio = Radio(ctx=ctx, voice_client=voice_client)
                radio.start(index=None)
            else:
                await ctx.reply("```\n"
                                "봇이랑 동일한 음성 채널에 들어와야합니다.\n"
                                "```")
        except AttributeError:
            pass

    @commands.command(help="다음 노래로 넘깁니다",
                      aliases=["s", "sk", "스킵"])
    @commands.cooldown(3, 5, commands.BucketType.guild)
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
