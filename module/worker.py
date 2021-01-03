# -*- coding: utf-8 -*-
from os import path, listdir
from random import shuffle
from logging import getLogger

from discord import FFmpegOpusAudio

logger = getLogger()


class Radio:
    def __init__(self, ctx, voice_client):
        self.ctx = ctx
        self.voice_client = voice_client
        self.loop = ctx.bot.loop

        self.music_list = listdir(path.join("music"))
        shuffle(self.music_list)

        try:
            self.music_list.remove("README.txt")
        except ValueError:
            pass

        self.now = "undefined"

    def _set_next(self):
        self.now = self.music_list.pop(1)
        self.music_list.append(self.now)

    def play_next(self, error):
        if error is not None:
            logger.error(f"{error}")

        if self.voice_client.is_connected():
            self._set_next()
            self.play_radio()

    def play_radio(self):
        player = FFmpegOpusAudio(
            source=path.join("music", self.now),
            bitrate=384,
            options='-af "volume=0.2"'
        )

        self.voice_client.play(
            source=player,
            after=self.play_next
        )
