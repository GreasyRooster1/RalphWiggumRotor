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
    You will be provided with an outline of the project, and code from the project.
    Your goal is to write a the next creative and semi-dev instructions for the dev team to follow, they follow your words very closely.
    you will look for any potential bugs, and add them to the instructions to be fixed.
    your instructions should be short and simple for the dev team to execute.
    your response goes straight into the outline file, do not commentate or speak ever
    you do not need to worry about the details of the development, you are mainly a creative director.
    never ever write code segments ever, in any language
    '''

    commit_model = DeepSeekCoderV2()
    commit_model.init_model()

    commit_model.sys_prompt = '''
    you will be given the diff for a commit on a project. write a very short and concise commit message. you should never output anything longer than a sentence.
    '''

    generate_commit_message(commit_model,proj_path)

    print("Starting initial creator generation...")
    generate_to_file(
        "project outline:\n "+read_file(os.path.join(proj_path, user_outline_name))+"\n\nwrite the first instructions for the dev team to start on. make sure the objectives are achievable for the first iteration",
        creator_model,
        os.path.join(proj_path, creator_outline_name))
    print("Starting coder generation...")
    generate_to_file(
        "project outline:\n "+read_file(os.path.join(proj_path, creator_outline_name)),
        programmer_model,
        os.path.join(proj_path, main_file_name))

    generate_commit_message(commit_model,
                            "project code:\n "+read_file(os.path.join(proj_path, main_file_name))+"\n\nproject outline:\n "+read_file(os.path.join(proj_path, user_outline_name)),
                            proj_path)

    while True:
        print("Starting creator generation...")
        generate_to_file(
                "project code:\n "+read_file(os.path.join(proj_path, main_file_name))+"\n\nproject outline:\n "+read_file(os.path.join(proj_path, user_outline_name))+"\n\nuse the outline and the project code to suggest new changes that you would like to see. make the instructions simple for the dev team. make sure to check for bugs",
            creator_model,
            os.path.join(proj_path, creator_outline_name))
        print("Starting coder generation...")
        generate_to_file(
            "project code:\n "+read_file(os.path.join(proj_path, main_file_name))+"\n\ndev instructions:\n "+read_file(os.path.join(proj_path, creator_outline_name))+"\n\nuse the instructions to update the code and apply those changes.",

            programmer_model,
            os.path.join(proj_path, main_file_name))

def generate_to_file(message,model,path):
    stream = model.stream_model_request(message)
    with open(path, 'w') as f:
        for chunk in stream:
            val = chunk['message']['content']
            f.write(val)
            print(chunk['message']['content'], end='', flush=True)

def generate_commit_message(model,dir):
    diff = subprocess.run(["git", "diff"], capture_output=True, text=True, check=True).stdout
    print(diff)
    response = model.send_model_request(diff)['message']['content']
    print(response)
    commit(response,dir)

def commit(message,dir):
    print(subprocess.run(["git", "add","--all"],cwd=dir, capture_output=True, text=True, check=True))
    print(subprocess.run(["git", "commit", "-m", message],cwd=dir, capture_output=True, text=True, check=True))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content



if __name__ == "__main__":
    main()