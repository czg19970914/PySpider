from Spider import Spider
from SpiderStrategy.BilibiliSpider.SingleBilibiliVideoStrategyImpl import SingleBilibiliVideoStrategy
from SpiderStrategy.TikTokSpider.SingleTikTokVideoStrategyImpl import SingleTikTokVideoStrategy
from SpiderStrategy.YouTubeSpider.SingleYouTubeVideoStrategyImpl import SingleYouTubeVideoStrategy


if __name__ == "__main__":
    spider = Spider()

    # Bilibili单个视频爬取
    # url = "https://www.bilibili.com/video/BV1knzPYpEZX/"
    # singleBilibiliVideoStrategy = SingleBilibiliVideoStrategy()
    # spider.setSpiderStrategy(singleBilibiliVideoStrategy)
    # spider.getContent(url)

    # YouTube单个视频爬取(未完成，中道崩殂)
    url = "https://www.youtube.com/shorts/-lPAoOTIa5E"
    singleYouTubeVideoStrategy = SingleYouTubeVideoStrategy()
    spider.setSpiderStrategy(singleYouTubeVideoStrategy)
    spider.getContent(url)

    # TikTok单个视频爬取
    # url = 'https://www.douyin.com/user/MS4wLjABAAAAO6EmrlV6vVc-GikErYV33_kBmN_vx-szh065MtO7Z30Btn_HDJWVBhX42IwUCLbp?from_tab_name=main&modal_id=7436812106562899219&vid=7436812106562899219'
    # singleTikTokVideoStrategy = SingleTikTokVideoStrategy()
    # spider.setSpiderStrategy(singleTikTokVideoStrategy)
    # spider.getContent(url)
