# -*- coding: utf-8 -*-
import json
import os
import re
import requests
import yt_dlp

from SpiderStrategy.SpiderStrategyInterface import SpiderStrategyInterface
from Utils.FileUtils import FileUtils


class YouTubeVideoStrategy(SpiderStrategyInterface):
    __save_dir_name = 'YoutubeVideo'
    __cookie = 'PREF=tz=Asia.Shanghai; VISITOR_INFO1_LIVE=YPxV_O5ALEQ; VISITOR_PRIVACY_METADATA=CgJKUBIEGgAgWA%3D%3D; SID=g.a000rAjq9eNI0irtMd5Hh53lAwIu3BS4G3VwjJvvFx3wzDKifCdDxPLO8j63Y8MOgC57fd9XMgACgYKAYoSARQSFQHGX2MiDzQtXPbeOkClOgpzuymzbxoVAUF8yKowFSF9EvTjsGxMSXnUHh9i0076; __Secure-1PSID=g.a000rAjq9eNI0irtMd5Hh53lAwIu3BS4G3VwjJvvFx3wzDKifCdD5S9YfWrqTttXUZGAFSQeowACgYKAb8SARQSFQHGX2Mibf7ZMCv1A45ECmZw_fnxvBoVAUF8yKqnbkZn9k6QmN4rRxo9p0o_0076; __Secure-3PSID=g.a000rAjq9eNI0irtMd5Hh53lAwIu3BS4G3VwjJvvFx3wzDKifCdDZESD-dxCFE39eTqSgzUo_gACgYKAdQSARQSFQHGX2MiiXk-vZUiODNuTEAV7xd_-RoVAUF8yKolzOJj5vsOYQGHvuqKsSEi0076; HSID=AnwOVD8r1EXTX85m4; SSID=Af84es8fWYaxToUFd; APISID=s0RsxkZyCslwvV4F/AyEIYMYGaeuN0o0Fk; SAPISID=FbCiURTy5ZJgPNau/AjjI9c7DJwL0bCG4A; __Secure-1PAPISID=FbCiURTy5ZJgPNau/AjjI9c7DJwL0bCG4A; __Secure-3PAPISID=FbCiURTy5ZJgPNau/AjjI9c7DJwL0bCG4A; LOGIN_INFO=AFmmF2swRQIhAPY56Fr_j7JLCI9vsMpRPlTH_qA8cZ5lSEobw6OPXhB_AiBcnGSc7Dw6m5CPh8I0_fBlfxltEU31_yqEGxarN4GwOw:QUQ3MjNmelMweGpKUWxaV0o0cjRQakJOcXBFS2R6Q3N5YXY0LXlRM2ozRUJOZklXRHNORXlhSk54aUVjaENPbnlscnpyTTd4YmotZGpuR1lUUURxWm55WDRhbkc0THVWaTgtQ3gwYWhjMi1wSFBBVEE4TnMxelN5a3lNNEFJOEN0TGVYbDZLV2dvU2ZuS042enZpbnBuSjZKN0JNOExOdjBR; YSC=KcI8BT3EDWQ; __Secure-1PSIDTS=sidts-CjIBQT4rX2aRV9XpWuRJWgj2v7mLlroL7A5hA53aIlaUpYq6YwUT9oKlxClogMelLMNb8RAA; __Secure-3PSIDTS=sidts-CjIBQT4rX2aRV9XpWuRJWgj2v7mLlroL7A5hA53aIlaUpYq6YwUT9oKlxClogMelLMNb8RAA; SIDCC=AKEyXzVG3hgRDGyZ4OAGaIBrSDWHBHcpkIl1kVLHNkuMz2f_jQTEYyem8XXwNmJZo4vjFmnzEQ; __Secure-1PSIDCC=AKEyXzU6LGpruXDNmBIY_u54yxsDWh5Bj3jZ7ei4UYaKboxe4ITj3chyXriFVWQJEir-88nNWQ; __Secure-3PSIDCC=AKEyXzVA1GplYNNvFaS6hDMLa9hu5Ey9n1IIO_4MzkVt9VLlMTQESCogU-JmTFtxR66e0gpA-l8'
    __user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    def set_cookie(self, cookie: str):
        self.__cookie = cookie

    def set_user_agent(self, user_agent: str):
        self.__user_agent = user_agent

    def get_content(self, url: str):
        self.__spider_single_video(url)

    def __spider_single_video(self, url):
        print("开始爬取Youtube视频.....")

        headers = {
            'referer': url,
            'cookie': self.__cookie,
            "user-agent": self.__user_agent
        }
        response = requests.get(url=url, headers=headers)
        html = response.text
        # print(html)

        play_json_str = re.findall('var ytInitialPlayerResponse = (.*?);var', html)[0]
        play_json = json.loads(play_json_str)

        title = play_json['videoDetails']['title']
        self.__download_video_by_google_api(url, title)

        # video_url = play_json['streamingData']['adaptiveFormats'][0]['url']
        # video_content_length = play_json['streamingData']['adaptiveFormats'][0]['contentLength']
        # audio_url = play_json['streamingData']['adaptiveFormats'][-2]['url']
        #
        # # 现在这个url，访问403，无法爬取，其它资源没有发现视频对应的下载链接
        # video_content = requests.get(url=video_url, stream=True)
        # print(video_content)

    def __download_video_by_google_api(self, url: str, title: str):
        dir_path = os.path.join(FileUtils.get_project_dir(), self.__save_dir_name)
        FileUtils.create_dir(dir_path)
        video_file_path = os.path.join(dir_path, title + '.mp4')
        cookie_file_path = os.path.join(dir_path, 'cookies.txt')

        # 设置参数，估计要查看文档
        ydl_opts = {
            'outtmpl': video_file_path,
            'cookiefile': cookie_file_path
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
