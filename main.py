import os

from DeepSeekCoderV2 import DeepSeekCoderV2
from dotenv import load_dotenv
import git

temp_path="./temp"
main_file_name = "main.py"

load_dotenv()



def main():
    programmer_model = DeepSeekCoderV2()
    programmer_model.init_model()

    programmer_model.sys_prompt = "You are an intelligent programmer, you only ever output code, never any commentary on your code, unless in the form of code comments. You write in JavaScript, you use the P5.js library. The boilerplate html for p5js is already written. your code goes directly into a script tag. remember to always define your variables and use correct syntax. Leave comments annotating your code frequently. do not output your code with markdown styling"



def generate_to_file(message,model,path):
    stream = model.stream_model_request("make a square bounce on the screen")
    with open(path, 'w') as f:
        for chunk in stream:
            val = chunk['message']['content']
            f.write(val)
            print(chunk['message']['content'], end='', flush=True)