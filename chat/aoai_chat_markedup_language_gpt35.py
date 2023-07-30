import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")

# defining a function to create the prompt from the system message and the conversation messages
def create_prompt(system_message, messages):
    prompt = system_message
    for message in messages:
        prompt += f"\n<|im_start|>{message['sender']}\n{message['text']}\n<|im_end|>"
    prompt += "\n<|im_start|>assistant\n"
    return prompt

# defining the user input and the system message
system_prompt = "You are a helpful assistant."
system_message = f"<|im_start|>system\n{system_prompt}\n<|im_end|>"
user_input = input('User: \n')   

# creating a list of messages to track the conversation
messages = [{"sender": "user", "text": user_input}]

response = openai.Completion.create(
    engine=OPENAI_GPT35_ENGINE, # The deployment name you chose when you deployed the ChatGPT model.
    prompt=create_prompt(system_message, messages),
    temperature=0.5,
    max_tokens=250,
    top_p=0.9,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['<|im_end|>']
)

messages.append({"sender": "assistant", "text": response['choices'][0]['text']})
print(response['choices'][0]['text'])