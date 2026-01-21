from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def loadModel(self):
        #initialize the model
        pass

    @abstractmethod
    def send_model_request(self, message: str):
        #Model makes a request and writes to the codebase, no return type
        pass