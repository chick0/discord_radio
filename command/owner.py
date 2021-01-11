# -*- coding: utf-8 -*-
from os import path, mkdir, listdir, remove
from random import shuffle
from asyncio import TimeoutError

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

    @commands.command(help="음악을 삭제합니다")
    @commands.is_owner()
    async def pop(self, ctx: commands.context, music_id: int = -1):
        target, index = None, 0
        for music in listdir(path.join("music")):
            if music.endswith(".mp3"):
                if index == music_id:
                    target = music
                    break
                index += 1

        if target is None:
            return

        safe_code = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        shuffle(safe_code)
        safe_code = "".join(safe_code)[:4]

        def chk(message):
            if message.channel.id == ctx.channel.id and message.author.id == ctx.author.id:
                if message.content == safe_code:
                    return True
            return False

        ask = await ctx.send("```\n"
                             f"'{target}'\n"
                             f"- 해당 노래를 재생목록에서 삭제하시겠습니까?\n"
                             f"- 삭제하려면 [{safe_code}]를 채팅창에 보내주세요\n"
                             f"```")

        try:
            await ctx.bot.wait_for("message", check=chk, timeout=10)
        except TimeoutError:
            await ask.edit(content="```\n요청 만료됨\n```")
            return

        try:
            remove(path.join("music", target))
            await ask.edit(content="```\n삭제 완료됨\n```")
        except (PermissionError, FileNotFoundError):
            await ask.edit(content="```\n요청 만료됨\n```")
            await ask.reply("```\n"
                            "삭제 실패\n"
                            "- 권한이 없거나 파일을 찾을 수 없음\n"
                            "```")

    @commands.command(help="노래를 업로드 합니다")
    @commands.is_owner()
    async def upload(self, ctx: commands.context):
        if len(ctx.message.attachments) == 0:
            await ctx.reply("```\n"
                            "업로드할 파일을 찾지 못함\n"
                            "```")
            return

        if not path.exists(path.join("music")):
            mkdir("music")

        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                if path.exists(path.join("music", attachment.filename)):
                    await ctx.reply("```\n"
                                    "이미 업로드된 파일입니다.\n"
                                    "```")
                else:
                    sig = await attachment.read()
                    if sig[:2].hex() == "fffb" or sig[:3] == b"ID3":
                        try:
                            await attachment.save(fp=path.join("music", attachment.filename))
                            await ctx.reply("```\n"
                                            f"업로드 완료 : {attachment.filename}\n"
                                            "- 해당 음악을 재생목록에 추가하려면 라디오를 껐다 켜야 합니다\n"
                                            "```")
                        except (HTTPException, NotFound):
                            await ctx.reply("```\n"
                                            "업로드 하는 파일을 다운받지 못함\n"
                                            "```")
                    else:
                        await ctx.reply("```\n"
                                        "허용되는 파일 형식이 아님\n"
                                        "```")
