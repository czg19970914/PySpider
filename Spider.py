from SpiderStrategy import SpiderStrategyInterface


class Spider:
    __spiderStrategyInterface: SpiderStrategyInterface

    def setSpiderStrategy(self, spiderStrategyInterface: SpiderStrategyInterface):
        self.__spiderStrategyInterface = spiderStrategyInterface

    def getContent(self, url):
        if self.__spiderStrategyInterface is not None:
            self.__spiderStrategyInterface.get_content(url)
