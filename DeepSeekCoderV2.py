from modelinterface import ModelInterface
from ollama import chat

class DeepSeekCoderV2(ModelInterface):
    def __init__(self):
        self.model_name = None
        self.temp = None
        self.client = None
        self.sys_prompt = ""

    def init_model(self):
        pass

    def send_model_request(self, message: str):
        response = chat(
            model='gemma3',
            messages=[
                {
                    'role': 'system',
                    'content': self.sys_prompt,
                },
                {
                    'role': 'user',
                    'content': message,
                },
            ],
            options={
                'temperature': self.temp,
            }
        )