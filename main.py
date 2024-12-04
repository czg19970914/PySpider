from Spider import Spider
from SpiderStrategy.BilibiliSpider.SingleBilibiliVideoStrategyImpl import SingleBilibiliVideoStrategy
from SpiderStrategy.TikTokSpider.TikTokVideoByAuthorStrategyImpl import TikTokVideoByAuthorStrategy
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

    # 从作者页面爬取抖音视频
    tikTokVideoByAuthorStrategy = TikTokVideoByAuthorStrategy()
    spider.setSpiderStrategy(tikTokVideoByAuthorStrategy)
    spider.getContent("")
