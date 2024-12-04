# -*- coding: utf-8 -*-
import os
import re
import subprocess
import time
import requests
import hashlib

from SpiderStrategy.SpiderStrategyInterface import SpiderStrategyInterface
from Utils.FileUtils import FileUtils
from Utils.DownloadUtils import DownloadUtils


class SingleBilibiliVideoStrategy(SpiderStrategyInterface):
    __save_dir_name = 'BilibiliVideo'

    def get_content(self, url):
        self.__spider(url)

    def __spider(self, url):
        print("b站开始爬取视频....")
        headers = {
            # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
            "Referer": url,

            "cookie": "CURRENT_FNVAL=4048; buvid3=291F6CD9-AE81-5041-66BB-C6570C10199689909infoc; b_nut=1727956989; _uuid=10FD2F1EE-1087C-A3E7-5311-5C9951103986F90506infoc; buvid4=F1B3D5A3-9F01-8A29-BCBB-4653B9ACC04890525-024100312-hGb8GhyCXnf9C1xrfP1UYw%3D%3D; enable_web_push=DISABLE; home_feed_column=5; browser_resolution=1432-782; DedeUserID=34755469; DedeUserID__ckMd5=25f688f3014c8d3f; LIVE_BUVID=AUTO4017279570403239; PVID=1; header_theme_version=CLOSE; fingerprint=49cc01ae66394e9c1d0dfae03e88f174; buvid_fp_plain=undefined; buvid_fp=49cc01ae66394e9c1d0dfae03e88f174; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM0MDM5OTksImlhdCI6MTczMzE0NDczOSwicGx0IjotMX0.KlnrSNt4eiZ70fztvQBf1KKR5zftvKcJcfYqnv_mOck; bili_ticket_expires=1733403939; SESSDATA=a9eb2bc7%2C1748696800%2C007a2%2Ac2CjAWsFkmJNFJdjdPEMyDid7SozOEJUwGPg5Bb2p7_59s81tniyOKUYXv03v6MF3ee3ISVkdTV0JEbkZIeHljTjQ5ajVjanROY2hpdnRialA2cVlIRFBFcVNyR3ZSRHFCMjRZZFBIRVd3WTExcmgyUW1ZNUZHM3dBc2NtWEc3bHNCeTBTMkJxVHl3IIEC; bili_jct=1d9de7b20319db3a50de93ab40efc98c; sid=6cmgi7c3; rpdid=|(klY~u~luum0J'u~JJuRR)|Y; bp_t_offset_34755469=1006338686020747264; b_lsid=147655A4_1938A5E9A84",

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }

        response = requests.get(url=url, headers=headers)
        html = response.text
        title = re.findall('title="(.*?)"', html)[0]

        # 请求视频文件信息
        play_url = "https://api.bilibili.com/x/player/wbi/playurl"
        play_avid = re.findall('"aid":(.*?),', html)[0]
        play_bvid = re.findall('"bvid":"(.*?)",', html)[0]
        play_cid = re.findall('"cid":(.*?),', html)[0]
        play_session = ""  # 不校验
        play_dm_img_inter = ""  # 不校验
        play_wts = str(int(time.time()))
        # b站使用了MD5加密获取w_rid来校验请求
        d = ['avid=' + play_avid,
             'bvid=' + play_bvid,
             'cid=' + play_cid,
             'dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBJc…zVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC',
             'dm_img_inter=' + play_dm_img_inter,
             'dm_img_list=%5B%5D',
             'dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',
             'fnval=4048',
             'fnver=0',
             'fourk=1',
             'from_client=BROWSER',
             'gaia_source=',
             'isGaiaAvoided=false',
             'is_main_page=true',
             'need_fragment=false',
             'qn=0',
             'session=' + play_session,
             'voice_balance=1',
             'web_location=1315873',
             'wts=' + play_wts]
        m = '&'.join(d)
        s = 'ea1db124af3c7062474693fa704f4ff8'
        MD5 = hashlib.md5()
        MD5.update((m + s).encode('utf-8'))
        play_w_rid = MD5.hexdigest()

        play_data = {
            'avid': play_avid,
            'bvid': play_bvid,
            'cid': play_cid,
            'qn': '0',
            'fnver': '0',
            'fnval': '4048',
            'fourk': '1',
            'gaia_source': '',
            'from_client': 'BROWSER',
            'is_main_page': 'true',
            'need_fragment': 'false',
            'isGaiaAvoided': 'false',
            'session': play_session,
            'voice_balance': '1',
            'web_location': '1315873',
            'dm_img_list': '[]',
            'dm_img_str': 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',
            'dm_cover_img_str': 'QU5HTEUgKEludGVsLCBJbnRlbChSKSBJcmlzKFIpIFhlIEdyYXBoaWNzICgweDAwMDA0NkE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC',
            'dm_img_inter': play_dm_img_inter,
            'w_rid': play_w_rid,
            'wts': play_wts
        }
        play_response = requests.get(url=play_url, params=play_data, headers=headers)
        play_json_data = play_response.json()
        video_url = play_json_data['data']['dash']['video'][0]['baseUrl']
        audio_url = play_json_data['data']['dash']['audio'][0]['baseUrl']
        video_content = requests.get(url=video_url,
                                     headers=headers,
                                     stream=True)
        audio_content = requests.get(url=audio_url,
                                     headers=headers,
                                     stream=True)

        # 保存视频与音频
        dir_path = os.path.join(FileUtils.get_project_dir(), self.__save_dir_name)
        FileUtils.create_dir(dir_path)
        video_file_path = os.path.join(dir_path, title + '.mp4')
        DownloadUtils.download_file(video_file_path, video_content,
                                    f'正在下载{title}视频中......')
        audio_file_path = os.path.join(dir_path, title + '.mp3')
        DownloadUtils.download_file(audio_file_path, audio_content,
                                    f'正在下载{title}音频中......')

        # 音、视频合并
        print("音、视频合并......")
        merge_file_path = os.path.join(dir_path, title + '_output.mp4')
        FileUtils.video_merge_audio(video_file_path,
                                    audio_file_path,
                                    merge_file_path)

        # 删除分开的音频和视频文件
        FileUtils.delete_file(video_file_path)
        FileUtils.delete_file(audio_file_path)

        print("完成......")
