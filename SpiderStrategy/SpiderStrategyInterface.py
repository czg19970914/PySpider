from abc import ABC, abstractmethod


class SpiderStrategyInterface(ABC):
    @abstractmethod
    def get_content(self, url: str):
        pass

    @abstractmethod
    def set_cookie(self, cookie: str):
        pass

    @abstractmethod
    def set_user_agent(self, user_agent: str):
        pass
