from modelinterface import ModelInterface
from openai import OpenAI

from util import load_api_key

class DeepSeekCoderV2(ModelInterface):
    def __init__(self):
        self.model_name = None
        self.temp = None
        self.client = None

    def init_model(self):
        api_key = load_api_key("DEEPSEEK_API_KEY")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        self.temp = 0.7
        self.model_name = "deepseek-coder"
        self.sys_prompt = "You are a helpful coding assistant that writes clean, efficient Python code."

    def send_model_request(self, message: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content":message}
            ],
            temperature=self.temp
        )