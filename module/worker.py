# -*- coding: utf-8 -*-
from os import path, listdir
from random import shuffle
from logging import getLogger
from asyncio import run_coroutine_threadsafe

from discord import FFmpegOpusAudio

logger = getLogger()


class Radio:
    def __init__(self, ctx, voice_client):
        self.ctx = ctx
        self.voice_client = voice_client
        self.loop = ctx.bot.loop

        self.music_list = []
        for music in listdir(path.join("music")):
            if music.endswith(".mp3"):
                self.music_list.append(music)
        shuffle(self.music_list)

        self.now = "undefined"

    def _set_next(self):
        try:
            self.now = self.music_list.pop()
            self.music_list.insert(0, self.now)
        except IndexError:
            run_coroutine_threadsafe(
                coro=self.ctx.send("```\n"
                                   "음악 폴더에 파일이 없음\n"
                                   "```"),
                loop=self.loop
            )
            run_coroutine_threadsafe(
                coro=self.voice_client.disconnect(),
                loop=self.loop
            )

    def _play_radio(self):
        if self.now == "undefined":
            return

        player = FFmpegOpusAudio(
            source=path.join("music", self.now),
            bitrate=384,
            options='-af "volume=0.2"'
        )

        self.voice_client.play(
            source=player,
            after=self.play_next
        )

    def play_next(self, error):
        if error is not None:
            logger.error(f"{error}")

        if self.voice_client.is_connected():
            self._set_next()
            self._play_radio()
