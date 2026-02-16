from .base import classproperty, BaseService
import inspect
from todoist_api_python.api import TodoistAPI
import os
import yt_dlp
from sounds.sound_control import PlayAudioManager
from ytmusicapi import YTMusic

class MusicManager(BaseService):
    MUSIC_PATH = ".temp_folder/temp_music"
    def __init__(self):
        super().__init__()
        self.ytm = YTMusic()


    from ytmusicapi import YTMusic

    def search_and_get_url(self, query):
        search_results = self.ytm.search(query, filter="songs", limit=1)
        
        if search_results:
            video_id = search_results[0]['videoId']
            title = search_results[0]['title']
            artist = search_results[0]['artists'][0]['name']
            
            url = f"https://music.youtube.com/watch?v={video_id}"
            print(f"Найдено: {artist} - {title}")
            return url
        else:
            print("Ничего не найдено.")
            return None

    def download_from_ytm(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.MUSIC_PATH, 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        print("Загрузка трека...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        


    def handle(self, song_name):
        song_url = self.search_and_get_url(song_name)
        if song_url is None:
            return "Song hasnt been found"
        self.download_from_ytm(song_url)
        PlayAudioManager().play_sound(f"{self.MUSIC_PATH}.mp3", is_thread=False)
        return "Song was played"
        


    @classproperty
    def info(cls):
        return f"""
        This module can turn on any song on youtube music
        require arguments:
        song_name - this is name of song
        
        """        
        

