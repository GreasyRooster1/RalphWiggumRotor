from abc import ABC, abstractmethod

from openai import OpenAI

from util import load_api_key


class ModelInterface(ABC):
    @abstractmethod
    def init_model(self):
        pass

    @abstractmethod
    def send_model_request(self, message: str):
        pass