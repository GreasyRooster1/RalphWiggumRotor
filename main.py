import os

from DeepSeekCoderV2 import DeepSeekCoderV2
from dotenv import load_dotenv
import subprocess

load_dotenv()



def main():
    proj_path="./temp"
    main_file_name = "main.js"
    user_outline_name = "USER_OUTLINE.md"
    creator_outline_name = "CREATOR_OUTLINE.md"


    programmer_model = DeepSeekCoderV2()
    programmer_model.init_model()

    programmer_model.sys_prompt = '''
    You are an intelligent programmer, you only ever output code, never any commentary on your code, unless in the form of code comments.
    You write in JavaScript, you use the P5.js library.
    The boilerplate html for p5js is already written.
    your code goes directly into a script tag.
    remember to always define your variables and use correct syntax.
    Leave comments annotating your code frequently.
    do not output your code with markdown styling, code is directly entered into a script tag verbatim.
    you will write code for a project provided by the user, follow their project outline very closely.
    you dont take creative liberties, ever.
    '''

    creator_model = DeepSeekCoderV2()
    creator_model.init_model()

    creator_model.sys_prompt = '''
    You are a creative director.
    You will be provided with a project outline to follow, and code to review.
    Your goal is to write a new, refreshed project outline for the dev team to follow, they follow your words exactly.
    write your outline using the overall project goals, and the code provided.
    you will look for any potential bugs, and add them to to outline to be fixed.
    the project outline you write is written in markdown
    '''

    print("Starting initial creator generation...")
    generate_to_file(
        "this is the first iteration of the project, refer to the overall project outline and create the outline for the first iteration. project outline:\n "+read_file(os.path.join(proj_path, user_outline_name)),
        creator_model,
        os.path.join(proj_path, creator_outline_name))
    print("Starting coder generation...")
    generate_to_file(
        "project outline:\n "+read_file(os.path.join(proj_path, creator_outline_name)),
        creator_model,
        os.path.join(proj_path, creator_outline_name))

    while True:
        print("Starting creator generation...")
        generate_to_file(
                "----------\nproject code:\n "+read_file(os.path.join(proj_path, main_file_name))+" -----------\nproject outline:\n "+read_file(os.path.join(proj_path, user_outline_name)),
            creator_model,
            os.path.join(proj_path, creator_outline_name))
        print("Starting coder generation...")
        generate_to_file(
            "project outline:\n "+read_file(os.path.join(proj_path, creator_outline_name)),
            creator_model,
            os.path.join(proj_path, creator_outline_name))

def generate_to_file(message,model,path):
    stream = model.stream_model_request("make a square bounce on the screen")
    with open(path, 'w') as f:
        for chunk in stream:
            val = chunk['message']['content']
            f.write(val)
            print(chunk['message']['content'], end='', flush=True)

def commit(message):
    subprocess.run(["git", "add","--all"])
    subprocess.run(["git", "commit", "-m", message])

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content