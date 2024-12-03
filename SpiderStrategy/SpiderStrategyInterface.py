from abc import ABC, abstractmethod


class SpiderStrategyInterface(ABC):
    @abstractmethod
    def get_content(self, url):
        pass
