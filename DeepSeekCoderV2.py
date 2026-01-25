import os

from modelinterface import ModelInterface
from ollama import chat, Client

from util import load_env


class DeepSeekCoderV2(ModelInterface):
    def __init__(self):
        self.model_name = None
        self.temp = None
        self.client = None
        self.sys_prompt = ""
        self.client = None

    def init_model(self):
        host = load_env('OLLAMA_HOST')
        self.client = Client(host=host)

    def send_model_request(self, message: str):
        response = self.client.chat(
            model='deepseek-coder-v2',
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

    def stream_model_request(self, message: str):
        response = self.client.chat(
            model='deepseek-coder-v2',
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
            },
            stream=True,
        )
        return response