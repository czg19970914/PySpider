from Spider import Spider
from SpiderStrategy.BilibiliSpider.SingleBilibiliVideoStrategyImpl import SingleBilibiliVideoStrategy
from SpiderStrategy.TikTokSpider.SingleTikTokVideoStrategyImpl import SingleTikTokVideoStrategy
from SpiderStrategy.YouTubeSpider.SingleYouTubeVideoStrategyImpl import SingleYouTubeVideoStrategy


if __name__ == "__main__":
    spider = Spider()

    # Bilibili单个视频爬取
    # url = "https://www.bilibili.com/video/BV1a5mDYpEhc/"
    # singleBilibiliVideoStrategy = SingleBilibiliVideoStrategy()
    # spider.setSpiderStrategy(singleBilibiliVideoStrategy)
    # spider.getContent(url)

    # YouTube单个视频爬取(未完成，中道崩殂)
    # url = "https://www.youtube.com/watch?v=2oStKdgT3Bg"
    # singleYouTubeVideoStrategy = SingleYouTubeVideoStrategy()
    # spider.setSpiderStrategy(singleYouTubeVideoStrategy)
    # spider.getContent(url)

    # TikTok单个视频爬取
    url = 'https://www.douyin.com/user/MS4wLjABAAAAONnizyktEAHaD6-RzkhIpx95eucJ0WfdfWHzzNgZ3CuPnhDbjEiXl1bCkOlhDSul?from_tab_name=main&modal_id=7444034558456040742&vid=7438929463808773426'
    singleTikTokVideoStrategy = SingleTikTokVideoStrategy()
    spider.setSpiderStrategy(singleTikTokVideoStrategy)
    spider.getContent(url)
