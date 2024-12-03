from Spider import Spider
from SpiderStrategy.BilibiliSpider.SingleBilibiliVideoStrategyImpl import SingleBilibiliVideoStrategy

if __name__ == "__main__":
    spider = Spider()

    # bilibili单个视频爬取
    url = "https://www.bilibili.com/video/BV11K6KYeEKJ/"
    singleBilibiliVideoStrategy = SingleBilibiliVideoStrategy()
    spider.setSpiderStrategy(singleBilibiliVideoStrategy)
    spider.getContent(url)
