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
    never use markdown styling.
    you will write code for a project provided by the user, follow their project outline very closely.
    you dont take creative liberties, ever.
    '''

    creator_model = DeepSeekCoderV2()
    creator_model.init_model()

    creator_model.sys_prompt = '''
    You are a creative director.
    You will be provided with an outline of the project, and code to use to help create the outline.
    Your goal is to write a the next creative and semi-dev instructions for the dev team to follow, they follow your words very closely.
    you will look for any potential bugs, and add them to the instructions to be fixed.
    your response goes straight into the outline file, do not commentate or speak ever
    The project is in JavaScript, the dev team uses the P5.js library.
    The boilerplate html for p5js is already written.
    the code goes directly into a script tag.
    never write code segments ever, in any language
    '''

    print("Starting initial creator generation...")
    generate_to_file(
        "project outline:\n "+read_file(os.path.join(proj_path, user_outline_name)),
        creator_model,
        os.path.join(proj_path, creator_outline_name))
    print("Starting coder generation...")
    generate_to_file(
        "project outline:\n "+read_file(os.path.join(proj_path, creator_outline_name)),
        programmer_model,
        os.path.join(proj_path, main_file_name))

    while True:
        print("Starting creator generation...")
        generate_to_file(
                "----------\nproject code:\n "+read_file(os.path.join(proj_path, main_file_name))+" -----------\nproject outline:\n "+read_file(os.path.join(proj_path, user_outline_name)),
            creator_model,
            os.path.join(proj_path, creator_outline_name))
        print("Starting coder generation...")
        generate_to_file(
            "project outline:\n "+read_file(os.path.join(proj_path, creator_outline_name)),
            programmer_model,
            os.path.join(proj_path, main_file_name))

def generate_to_file(message,model,path):
    stream = model.stream_model_request(message)
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



if __name__ == "__main__":
    main()