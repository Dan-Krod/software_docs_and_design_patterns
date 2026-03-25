from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def send(self, data: dict):
        """Відправити один рядок даних у сховище"""
        pass