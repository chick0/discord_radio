# -*- coding: utf-8 -*-
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
        await ctx.send(f"```\n"
                       f" - 뭐 그리 급해, {time}초만 기다려\n"
                       f"```<@{ctx.author.id}>")
        return

    if error.__class__.__name__ in ["CommandNotFound", "CheckFailure", "NotOwner"]:
        return

    logger.info(f"[{ctx.author.id}]{ctx.author} meet the error!")
    logger.error(f"{error.__class__.__name__}: {error}")
