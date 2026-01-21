from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def init_model(self):
        pass

    @abstractmethod
    def send_model_request(self, message: str):
        pass