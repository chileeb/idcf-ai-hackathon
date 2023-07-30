import os
import openai
from dotenv import load_dotenv
from prompts import demoprompts_wizard

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_GPT4_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")

OPENAI_GPT4_ENGINE = os.getenv("OPENAI_GPT4_ENGINE")

def get_response(conversation):
    response = openai.ChatCompletion.create(
        engine=OPENAI_GPT4_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = conversation,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        stream=True
        )

    gpt = ""
    for chunk in response:
        delta = chunk.choices[0].delta
        
        if "role" in delta.keys():
            print(delta.role + ": ", end="\n", flush=True)

        if "content" in delta.keys():
            gpt += delta.content
            print(delta.content, end="", flush=True)
    return gpt

def reset_role_wizard_1():
    role = input('请输入您需要的角色: \n')
    tech = input('请输入您需要的技术: \n')
    system_prompt = demoprompts_wizard.wizard_1.format(role=role, tech=tech)
    conversation=[{"role": "system", "content": system_prompt}]
    print("生成prompt中, 请稍等...")
    conversation.append({"role": "user", "content": ""})
    gpt_init = get_response(conversation)
    conversation.append({"role": "assistant", "content": gpt_init})
    return conversation

def reset_role_wizard_2():
    roleA = input('请输入您需要的古代角色: \n')
    roleB = input('请输入您需要的现代角色: \n')
    topic = input('请输入您需要交流的主题: \n')
    round = input('请输入您需要交流的轮次: \n')
    system_prompt = demoprompts_wizard.wizard_2.format(roleA=roleA, roleB=roleB, topic=topic, round=round)
    conversation=[{"role": "system", "content": system_prompt}]
    print(" 正在生成prompt, 请稍等...")
    print(system_prompt)
    print(" 正在生成对话, 请稍等...")
    conversation.append({"role": "user", "content": ""})
    gpt_init = get_response(conversation)
    conversation.append({"role": "assistant", "content": gpt_init})
    return conversation