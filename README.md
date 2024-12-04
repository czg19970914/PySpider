# PySpider
一个python的爬虫，建设中...... <br>
采用策略模式，在main文件中替换不同的爬虫策略爬取不同的网站

## 已完成
- b站单个视频的爬取（SingleBilibiliVideoStrategy）
  - 输入：b站播放页面的url，例如https://www.bilibili.com/video/BV11K6KYeEKJ/
  - 输出：播放页的视频（mp4），保存在根目录的BilibiliVideo文件夹下
  - 注意：由于b站视频、音频分开，需要安装ffmpeg合并音频、视频，自行下载

- 抖音单个视频爬取（SingleTikTokVideoStrategy）
    - 输入：视频播放页url，注意最好从作者跳转到对应url，例如https://www.douyin.com/user/MS4wLjABAAAAONnizyktEAHaD6-RzkhIpx95eucJ0WfdfWHzzNgZ3CuPnhDbjEiXl1bCkOlhDSul?from_tab_name=main&modal_id=7444034558456040742&vid=7438929463808773426
    - 输出：播放页的视频（mp4），保存在根目录的TikTokVideo文件夹下
