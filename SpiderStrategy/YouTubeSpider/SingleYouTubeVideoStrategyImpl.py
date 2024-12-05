# -*- coding: utf-8 -*-
import json
import os
import re
import requests
import yt_dlp

from SpiderStrategy.SpiderStrategyInterface import SpiderStrategyInterface
from Utils.FileUtils import FileUtils


class SingleYouTubeVideoStrategy(SpiderStrategyInterface):
    __save_dir_name = 'YoutubeVideo'
    __cookie = ''
    __user_agent = ''

    def set_cookie(self, cookie: str):
        pass

    def set_user_agent(self, user_agent: str):
        pass

    def get_content(self, url: str):
        self.__spider(url)

    def __spider(self, url):
        print("开始爬取Youtube视频.....")

        headers = {
            'referer': url,

            "cookie": "VISITOR_INFO1_LIVE=YwwfeA2Td9g; VISITOR_PRIVACY_METADATA=CgJDThIEGgAgFg%3D%3D; YSC=xoWP3oL3auc; __Secure-ROLLOUT_TOKEN=CIqu9PvS2eeaHhDz-Kjm_uWJAxjEiL_1p4uKAw%3D%3D; PREF=tz=Asia.Shanghai&f4=4000000; __Secure-1PSIDTS=sidts-CjIBQT4rX3vZ0aQwMFm6ecVDPC6VneBrjWnVWQmLgA4gPeefYyYXSx8SW301OTDeR7hbDhAA; __Secure-3PSIDTS=sidts-CjIBQT4rX3vZ0aQwMFm6ecVDPC6VneBrjWnVWQmLgA4gPeefYyYXSx8SW301OTDeR7hbDhAA; HSID=Ant9JCQb6QRxJfFxT; SSID=AC7HvlehxUJGOacX-; APISID=H-QAC9zOraNo8LIr/AusGsEyOhPQT638CW; SAPISID=dT8ntD4GA7JljVOe/ASbPpkSEhG1l01e5C; __Secure-1PAPISID=dT8ntD4GA7JljVOe/ASbPpkSEhG1l01e5C; __Secure-3PAPISID=dT8ntD4GA7JljVOe/ASbPpkSEhG1l01e5C; SID=g.a000qwjq9d5t7URkQUvr1e4B5vCt_ew2H1vHdyAAMgkR8fY7SCTzJRE-3zXTJ2S__8-7NNSFfgACgYKAUsSARQSFQHGX2MiDdJownp3u0YHJKMubG1_ChoVAUF8yKphp2H4VZS0Pn-vqqBnOPgz0076; __Secure-1PSID=g.a000qwjq9d5t7URkQUvr1e4B5vCt_ew2H1vHdyAAMgkR8fY7SCTzSXRzqUU5dXOBM4jODug74wACgYKASMSARQSFQHGX2MioYfYylPnpQCOcRWM7gM4QxoVAUF8yKpFUS6bIooIBTa48_HyNjln0076; __Secure-3PSID=g.a000qwjq9d5t7URkQUvr1e4B5vCt_ew2H1vHdyAAMgkR8fY7SCTzPxnQ4BIsVpur1ksmko0N7QACgYKASoSARQSFQHGX2Miq7MxhpdATso1GlkPXRVigBoVAUF8yKrigP5je0n-crIoHvjXKcn20076; LOGIN_INFO=AFmmF2swRQIhAP5bH69CL4e2rGrf69CKlDen0ULyXhiX9N2JTEGfLphpAiAVLEhl5_MBSGaP6FrB3yF5o3zR_g9en0dokZAVT5UfAA:QUQ3MjNmeWl6SmctbWdmdXNGS052SlByMkYyRHh2NzVkd1V0OW5oNEZLUzVIel9pZWZ1b1Y3MWV6Vm9zeXIySWFJNmd3a25FaGdwQzYzdjdKLW1SbVJnYUhLaWh0NDdBTnl1emtpc2tYQ3M2Y1RuVWdHVUxLVDRaaWppaEpKcGo1Z3FiOVRCcFZDQUpJY29PVU13SWw0dktjemFTYW1FdV9B; SIDCC=AKEyXzWqeRDAdJ-ImBKql4PFsAKcy95MYt8_9hG2Q_GOnZL8qXmmNuQo44uuEI6k8j8YOTUpHA; __Secure-1PSIDCC=AKEyXzUZ4AIXuubYmwTV760Xtoi_zAQBkQlhgntERi13jcalg8YyD7MuU1tkTfSv2e6mQv7YdA; __Secure-3PSIDCC=AKEyXzVu6-9MAFQKbfZnFoe5u4UuJyRkYSJ0d3P-h91IqNedC7LLTzCfxv_XSa3aPkLR5lzu",

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        response = requests.get(url=url, headers=headers)
        html = response.text
        # print(html)

        play_json_str = re.findall('var ytInitialPlayerResponse = (.*?);var', html)[0]
        play_json = json.loads(play_json_str)

        # print(play_json)
        title = play_json['videoDetails']['title']
        self.__download_video_by_google_api(url, title)
        # video_url = play_json['streamingData']['adaptiveFormats'][0]['url']
        # video_content_length = play_json['streamingData']['adaptiveFormats'][0]['contentLength']
        # audio_url = play_json['streamingData']['adaptiveFormats'][-2]['url']

        # 现在这个url，访问403，无法爬取，其它资源没有发现视频对应的下载链接
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
