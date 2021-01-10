# -*- coding: utf-8 -*-
from random import choice
from logging import getLogger

from discord import Status, Activity, ActivityType

from config import config

logger = getLogger()


async def on_ready(bot):
    def get_status(option: str):
        if option == "idle":
            return Status.idle
        elif option == "dnd":
            return Status.dnd
        elif option == "offline":
            return Status.offline
        else:
            return Status.online

    def get_type(option: str):
        if option == "streaming":
            return ActivityType.streaming
        elif option == "listening":
            return ActivityType.listening
        elif option == "watching":
            return ActivityType.watching
        else:
            return ActivityType.playing

    logger.info("-" * 50)
    logger.info(f" - BOT Login : {bot.user}")
    logger.info(f" - Connected to ( {len(bot.guilds)} ) guilds!")
    logger.info("-" * 50)

    await bot.change_presence(
        status=get_status(config["status"]["status"]),
        activity=Activity(
            type=get_type(config["status"]["activity"]),
            name=config["status"]["name"]
        )
    )


async def on_command(ctx):
    logger.info(f"[{ctx.author.id}]{ctx.author} use [{ctx.message.content}]")


async def on_command_error(ctx, error):
    if error.__class__.__name__ == "CommandOnCooldown":
        time = str(error).rsplit(" ", 1)[-1][:-1]
        message = ["고양이가 횡단보도를 건너는 중...",
                   "너구리가 솜사탕을 헹구는 중...",
                   "스폰지밥이 게살버거를 뒤집는 중...",
                   "오븐에서 산딸기 파이가 구워지는 중...",
                   "오리너구리 페리가 두펀스머츠를 제압하는 중...",
                   "행복 회로가 불타는 중...",
                   "돼지 저금통에 동전을 넣는 중...",
                   "넥서스가 공격받는 중...",
                   "엘 루비오의 금고가 털리는 중...",
                   "고양이가 그루밍 하는 중...",
                   "컴파일하는 척하면서 고양이 쓰다듬는 중...",
                   "선생님 몰래 춤추는 중...",
                   "치킨이 튀겨지는 중...",
                   "고양이가 파쿠르 하는 중...",
                   "샷건으로 키보드가 부서지는 중...",
                   "하늘에서 음식이 내리는 중...",
                   "하울의 성이 움직이는 중...",
                   "가상머신이 부팅되는 중...",
                   "좌측담장 넘어가는 중...",
                   "저궤도 이온 포를 준비하는 중..."]

        await ctx.reply(f"```\n{choice(message)} {time}초만 기다려주세요...\n```")
        return

    if error.__class__.__name__ in ["CommandNotFound", "CheckFailure", "NotOwner"]:
        return

    logger.info(f"[{ctx.author.id}]{ctx.author} meet the error!")
    logger.error(f"{error.__class__.__name__}: {error}")
