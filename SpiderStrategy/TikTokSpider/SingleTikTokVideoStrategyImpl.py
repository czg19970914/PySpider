import json
import os
import re
from urllib.parse import unquote

import requests

from SpiderStrategy.SpiderStrategyInterface import SpiderStrategyInterface
from Utils.DownloadUtils import DownloadUtils
from Utils.FileUtils import FileUtils


class SingleTikTokVideoStrategy(SpiderStrategyInterface):
    __save_dir_name = 'TikTokVideo'
    __cookie = '__ac_referer=__ac_blank; douyin.com; ttwid=1%7CNXF5glZ8Ikxn3r7I1qrHL7KRB-PSoktrjAavkN--OFE%7C1733296797%7Cf9e787f9e90393853ae03bb878818a73fbaab94927f54a2a5d6fb20cb50084a4; UIFID_TEMP=26198ff38959f773c63a6fc9b3542e2fdcfd2f10d2782124ed1adc24709862df6966cc507912a8c031e2f8ae655b466fe022d16701a5af00f7ec47a8d3da843fcc332e4005d7aeb888028b0876ff95c3; douyin.com; is_dash_user=0; s_v_web_id=verify_m49k5uo6_4m9AqkMx_hNdj_44VJ_AjOg_AgJn3nn2Gx0k; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; dy_swidth=1440; dy_sheight=900; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; strategyABtestKey=%221733296801.19%22; csrf_session_id=e738ab204f7023c33c2aa36372577f45; xgplayer_user_id=192690070966; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; passport_csrf_token=b676a76d9f2b5132b12ec0cb46c55b2f; passport_csrf_token_default=b676a76d9f2b5132b12ec0cb46c55b2f; fpk1=U2FsdGVkX1+9fwTdlMg5LL6Q+iuiAs0iHjfkIyhDpVNS7ofduodiHv2x65WALVwrDcapVW9UnwVNzCHEMpLJNw==; fpk2=ffc3218438300d069a0fd5dfa5c6e851; bd_ticket_guard_client_web_domain=2; UIFID=26198ff38959f773c63a6fc9b3542e2fdcfd2f10d2782124ed1adc24709862dfda4ff8cfbb32359aa1eb682c5f5a45dfb454a4b0a176df057a47bdbca0347696f67a1b93fcb45e9a210cc99ba5e469d9138620dd98a40538584c623cc243440d703bff8b3476d101664748d368a29053d333d0903f596f72c0a4f1959ed8568830f6ee4438c6f27af08c4bc21e5127361cb384b3e769a4a7078509cf2d61a21c; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; download_guide=%222%2F20241204%2F1%22; xg_device_score=7.773323026485472; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e5827292771273f27343730303334323c37363632342778; bit_env=EblzEuJh9zdB5dZisai7KXDmu61zL6aPnlhcWh9TSDecnwlpumoJ7lTpcn779aR6KFceQWt5xk54kN2zTMHNgcmBpGGHijekq_4OS_cIjMIm0C7jRsj0CZXTsPc4MrLxMwE81K475XJQEHbGNLDyQqcl_QhmxfMeYl84gxl3Hl54wK5rnHBkTmLtvnzzM4NJchxPxkildZ7EzP6NAIaCQU8rFtACzamWIinT2JWAORcoePE4H3upnQa_xY-TckLDvIUyWCcecr3nWyCEEiOHOXcuj3IvOcyeco-9UNAay5_McAdig_AcmBHufjbyHyRArl2kK0LYa5mGNnsa5DDthdh67Z8P754nKuZ_3x4IsFTFbCzDpvgbC9ZMwGE-NZgNpQTRu-M-p6Vl4z9zfFLgfLBTtr6ZEzGgeGPpICEPvK8tWxuww-5Uwmm7H8_hpsbBjZc1qPUflpGMqJWn7TPGGaLyltu3WqhxL5OKEF4oBdfiSh8836eOTnPpOnKVetFznZVQLPzKAgyudSweMDin-L9VIhOABJ1vZJxnPk5fz8E%3D; gulu_source_res=eyJwX2luIjoiZjgxMDM2NjljMjZmMzZkODQ0MmQwMTUzZTdlODMyODRlYzdmN2M3M2UwMDRlMTE3N2JkMjVkNjIyOGYyNTNhYiJ9; passport_auth_mix_state=ioqsf8v82u0me8cq40l6sx3tluj4myczcodjb3g3lbd66hwt; passport_mfa_token=CjWEfYwFJVQ%2Fe4ISsmt1gugVrTGx5qOwAvHgduQX1zBt9tW4MUDsaMl7t41I2Am4QT9re09YiRpKCjyFWfl84oZ2%2FaSQZFkWhDhpTCE5Z6HRZTK8iQh8mxYwht152Mpzrb48%2Bb0zXjXyRLQkmxJTSCkSJWv2PggQjZnjDRj2sdFsIAIiAQOphF5c; d_ticket=15d709d7826c9c981553190f0b7ac0ebbde93; passport_assist_user=CjzF008-NC8P9vJXUnqJSmBSyg6Bs5RIkTvRbU26j1tFKKjcYI4XaUGg99RNPxhC1gGYAxpudXw8kFoGPmAaSgo8QKZ8N5E1HvazAcbXi3UfuE-xPtsks_9NTNB6EAK3XS_hc7czSsDUPORgOXJ1ro29ylQ3upyIW4m_jlMUEJeZ4w0Yia_WVCABIgEDXVUV9Q%3D%3D; n_mh=Q6tKpoyd6DcUlOf-NHlriySQi5JhjK3RNqnaDw1rVRc; sso_uid_tt=6071484fe200df17f67fdeb6ec3b4f44; sso_uid_tt_ss=6071484fe200df17f67fdeb6ec3b4f44; toutiao_sso_user=dcc557b7bf5d1cb21245db9d86fdf45f; toutiao_sso_user_ss=dcc557b7bf5d1cb21245db9d86fdf45f; sid_ucp_sso_v1=1.0.0-KDFhYWM1MTJlN2E3MjBkN2ViNGJjNjFmMmQ0NWYxZjhiMWE5ZDU0ZmIKHwj8m525iAIQj4nAugYY7zEgDDCzhMTOBTgGQPQHSAYaAmxmIiBkY2M1NTdiN2JmNWQxY2IyMTI0NWRiOWQ4NmZkZjQ1Zg; ssid_ucp_sso_v1=1.0.0-KDFhYWM1MTJlN2E3MjBkN2ViNGJjNjFmMmQ0NWYxZjhiMWE5ZDU0ZmIKHwj8m525iAIQj4nAugYY7zEgDDCzhMTOBTgGQPQHSAYaAmxmIiBkY2M1NTdiN2JmNWQxY2IyMTI0NWRiOWQ4NmZkZjQ1Zg; passport_auth_status=d991b360c9d3cbf722b91ef460ef6e84%2C; passport_auth_status_ss=d991b360c9d3cbf722b91ef460ef6e84%2C; uid_tt=d2111f7c662f60f974435cbecc53e28f; uid_tt_ss=d2111f7c662f60f974435cbecc53e28f; sid_tt=98e60525cc264fd999cf13afe9bc8b06; sessionid=98e60525cc264fd999cf13afe9bc8b06; sessionid_ss=98e60525cc264fd999cf13afe9bc8b06; is_staff_user=false; __ac_nonce=06750049100550666ccd6; passport_fe_beating_status=true; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=777b35118fae6004818728ec444a5d9e; __security_server_data_status=1; sid_guard=98e60525cc264fd999cf13afe9bc8b06%7C1733297299%7C5183999%7CSun%2C+02-Feb-2025+07%3A28%3A18+GMT; sid_ucp_v1=1.0.0-KDRjZTg2YTFmNjE3MmFjYjk3NGIzMmJjMjQ0ZWZmOTA0MjkxNWUwZWYKGQj8m525iAIQk4nAugYY7zEgDDgGQPQHSAQaAmxmIiA5OGU2MDUyNWNjMjY0ZmQ5OTljZjEzYWZlOWJjOGIwNg; ssid_ucp_v1=1.0.0-KDRjZTg2YTFmNjE3MmFjYjk3NGIzMmJjMjQ0ZWZmOTA0MjkxNWUwZWYKGQj8m525iAIQk4nAugYY7zEgDDgGQPQHSAQaAmxmIiA5OGU2MDUyNWNjMjY0ZmQ5OTljZjEzYWZlOWJjOGIwNg; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A1%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; SelfTabRedDotControl=%5B%5D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAvEKYsQoJGlQKquyJ9y78NcYHw8Mgq6VYPcPvmdOYL84%2F1733328000000%2F0%2F1733297312119%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTzh5VTcySmkrZTEwMjNRZDdUbnY5dDZlR2RMc3Q3M2s1THJKT2sxUGszU0tXRDUrUThDaE9wWmVDSlpaek9tWG8wSkFvdlpDZTZ0ZUc2cGpCTjJvYkE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; publish_badge_show_info=%220%2C0%2C0%2C1733297316906%22; biz_trace_id=cbdde00a; odin_tt=b88ea8434525a1212b818c08a24f770cc6cbc486ab283282226dfc9802fe330220804350b7351be23d1695f737f2c5a268a388980b95f2411c968ce5bc2ae824; store-region=cn-js; store-region-src=uid; WallpaperGuide=%7B%22showTime%22%3A1733297330516%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; IsDouyinActive=false'
    __user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    def get_content(self, url: str):
        self.__spider(url)

    def __spider(self, url: str):
        print("开始抖音视频爬取......")
        headers = {
            # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
            "Referer": url,
            "cookie": self.__cookie,
            "user-agent": self.__user_agent
        }
        response = requests.get(url=url, headers=headers)
        html = response.text

        video_message = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', html)[0]
        # 信息需要解码
        video_message_decode = unquote(video_message)
        video_json_data = json.loads(video_message_decode)
        title = video_json_data['app']['videoDetail']['desc']
        video_url = 'https:' + video_json_data['app']['videoDetail']['video']['playAddr'][0]['src']
        video_content = requests.get(url=video_url,
                                     headers=headers,
                                     stream=True)

        # 保存视频
        dir_path = os.path.join(FileUtils.get_project_dir(), self.__save_dir_name)
        FileUtils.create_dir(dir_path)
        video_file_path = os.path.join(dir_path, title + '.mp4')
        DownloadUtils.download_file(video_file_path, video_content,
                                    f'正在下载{title}视频中......')

        print("爬取完成")

    def set_cookie(self, cookie: str):
        self.__cookie = cookie

    def set_user_agent(self, user_agent: str):
        self.__user_agent = user_agent
