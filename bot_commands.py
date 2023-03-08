from discord.ext import commands
import discord
import asyncio
import yt_dlp
import os


ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # 'outtmpl': None,  # This is set in the function itself
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}


class MusicBot(commands.Cog):

    def __init__(self, bot: commands.Bot, config):
        self.bot = bot
        self.music_directory = config["music_directory"]
        self.default_repetitions = config["default_repetitions"]
        self.stop_all = False

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        # check if already connected to a channel. If so, disconnect
        voice_client = ctx.message.guild.voice_client
        if ctx.message.guild.voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        # check if author is connected to a voice channel
        if not ctx.message.author.voice:
            await ctx.send(f"Error: {ctx.message.author.name} is not connected to a voice channel.")
            return
        # connect to author's channel
        author_channel = ctx.message.author.voice.channel
        try:
            await author_channel.connect()
        except Exception as e:
            await ctx.send(f"Error: {e}")
            return False
        return True

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        # check if bot is connected to a voice channel. If so, disconnect
        if ctx.message.guild.voice_client and ctx.message.guild.voice_client.is_connected():
            await ctx.message.guild.voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='play', help='To play song')
    async def play(self, ctx, name="amazing_song", total_repetitions: int = None):
        # use default total repetition if not given
        if total_repetitions is None:
            total_repetitions = self.default_repetitions
        # connect to voice channel if not already
        if not ctx.message.guild.voice_client:
            connected = await self.join(ctx)
            if not connected:
                return
        # check if song was downloaded
        song_path = os.path.join(self.music_directory, f'{name}.mp3')
        if not os.path.isfile(song_path):
            await ctx.send(f"There is no song named {name}.mp3. Aborting...")
            return
        # check if a song was already being played. If so stop
        if ctx.message.guild.voice_client.is_playing() or ctx.message.guild.voice_client.is_paused():
            await self.stop(ctx)
        await ctx.send(f"Playing {name}.mp3.")
        repetitions = 0
        self.stop_all = False
        while repetitions < total_repetitions:
            # if stopped or voice channel was left by bot, stop
            if self.stop_all or not ctx.message.guild.voice_client:
                break
            ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(song_path),
                                                after=lambda e: print(e if e else "", end=""))
            # Let the user be aware of having been Rick Rolled
            if name == "amazing_song":
                await asyncio.sleep(2)
                await ctx.send(f'I am required to inform you that you have been Rick Rolled.')
            # wait until song ends
            while ctx.message.guild.voice_client and \
                    (ctx.message.guild.voice_client.is_playing() or ctx.message.guild.voice_client.is_paused()):
                await asyncio.sleep(.1)
            repetitions += 1
        if total_repetitions > 1:
            await ctx.send(f'Finished last repetition.')

    @commands.command(name='download', help='Download a song form YouTube')
    async def download(self, ctx, url, name):
        song_path = os.path.join(self.music_directory, f"{name}.%(ext)s")
        # check if song already exists
        if os.path.isfile(song_path):
            await ctx.send(f"A song named {name}.mp3 already exists. Aborting...")
            return
        # download it
        ydl_opts['outtmpl'] = song_path
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)
            if error_code:
                await ctx.send(f"Error: {error_code}")

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        if ctx.message.guild.voice_client.is_playing():
            ctx.message.guild.voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        if ctx.message.guild.voice_client.is_paused():
            ctx.message.guild.voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this.")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        if ctx.message.guild.voice_client.is_playing() or ctx.message.guild.voice_client.is_paused():
            ctx.message.guild.voice_client.stop()
            self.stop_all = True
        else:
            await ctx.send("The bot is not playing anything at the moment.")
