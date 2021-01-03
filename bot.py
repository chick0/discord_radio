#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from logging import getLogger

import discord
from discord.ext import commands

from config import config
from command import owner, radio, user

from module import log
from module import event
logger = getLogger()


if __name__ == "__main__":
    if config["bot"]["use_shard"].lower() == "true":
        bot = commands.AutoShardedBot(command_prefix=config["bot"]["prefix"])
        logger.info("Client is 'AuthShard' Client")
    else:
        bot = commands.Bot(command_prefix=config["bot"]["prefix"])
        logger.info("Client is 'Normal' Client")

    async def call_on_ready():
        await event.on_ready(bot=bot)

    bot.add_listener(call_on_ready, "on_ready")
    bot.add_listener(event.on_command, "on_command")
    bot.add_listener(event.on_command_error, "on_command_error")

    bot.add_cog(owner.Command(bot))
    bot.add_cog(radio.Command(bot))
    bot.add_cog(user.Command(bot))

    try:
        bot.run(config["token"]["discord"])
    except KeyError:
        with open(path.join("conf", "token.ini"), mode="w", encoding="utf-8") as fp:
            fp.write("[token]\n")
            fp.write("discord=YOUR_TOKEN")
        logger.critical("Token not found. Edit the file './conf/token.ini'")
    except discord.errors.LoginFailure:
        logger.critical("Fail to Login. Edit the file './conf/token.ini'")
    except Exception as st_error:
        logger.critical(f"Fail to start Bot | {st_error.__class__.__name__}: {st_error}")
