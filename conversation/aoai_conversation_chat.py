import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")

system_prompt = "You are a helpful assistant."
conversation=[{"role": "system", "content": system_prompt}]

while(True):
    user_input = input('User: \n')      
    if 'exit' in user_input.lower():
        exit()

    conversation.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        engine=OPENAI_GPT35_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = conversation
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\nGPT: \n" + response['choices'][0]['message']['content'] + "\n")