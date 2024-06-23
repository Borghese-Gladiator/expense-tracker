from abc import ABC, abstractmethod

class BaseDatasource(ABC):
    @abstractmethod
    def get_transactions(self):
        pass
