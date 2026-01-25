import os

from DeepSeekCoderV2 import DeepSeekCoderV2
from dotenv import load_dotenv


load_dotenv()

programmer_model = DeepSeekCoderV2()
programmer_model.init_model()

programmer_model.sys_prompt = "You are an intelligent programmer, you only ever output code, never any commentary on your code, unless in the form of code comments. You write in JavaScript, you use the P5.js library. The boilerplate html for p5js is already written. your code goes directly into a script tag. remember to always define your variables and use correct syntax. Leave comments annotating your code frequently"

stream = programmer_model.stream_model_request("make a square bounce on the screen")

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)