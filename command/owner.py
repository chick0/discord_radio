# -*- coding: utf-8 -*-
from os import path, mkdir

from discord.errors import HTTPException, NotFound
from discord.ext import commands


class Command(commands.Cog, name="봇 주인용 명령어"):
    @commands.command(help="봇을 종료합니다")
    @commands.is_owner()
    async def close(self, ctx: commands.context):
        await ctx.send(":wave:")
        await ctx.bot.close()

    @commands.command(help="모든 음성 채널에서 나갑니다")
    @commands.is_owner()
    async def leave_all(self, ctx: commands.context):
        for voice_client in ctx.bot.voice_clients:
            await voice_client.disconnect()

    @commands.command(help="노래를 업로드 합니다")
    @commands.is_owner()
    async def upload(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send("```\n"
                           "업로드할 파일을 찾지 못함\n"
                           "```")
            return

        if not path.exists(path.join("music")):
            mkdir("music")

        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                print("YEAH")

            if path.exists(path.join("music", attachment.filename)):
                await ctx.send("```\n"
                               "이미 업로드된 파일입니다.\n"
                               "```")
            else:
                _u = await attachment.read()
                if _u[:2].hex() == "ffbb" or _u[:3].hex() == "494443":
                    try:
                        await attachment.save(fp=path.join("music", attachment.filename))
                        await ctx.send("```\n"
                                       f"업로드 완료 : {attachment.filename}\n"
                                       "- 해당 음악을 재생목록에 추가하려면 라디오를 껐다 켜야 합니다\n"
                                       "```")
                    except (HTTPException, NotFound):
                        await ctx.send("```\n"
                                       "업로드 하는 파일을 다운받지 못함\n"
                                       "```")
                else:
                    await ctx.send("```\n"
                                   "허용되는 파일 형식이 아님\n"
                                   "```")
