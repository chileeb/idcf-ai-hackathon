import os
import openai
from dotenv import load_dotenv
class Conversation:
    def __init__(self):
        load_dotenv()
        openai.api_type = "azure"
        openai.api_base = os.getenv("OPENAI_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        self.OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
        self.OPENAI_GPT3_ENGINE = os.getenv("OPENAI_GPT3_ENGINE")
        self.system_prompt = "You are a helpful assistant."
        self.system_message = f"<|im_start|>system\n{self.system_prompt}\n<|im_end|>"
        self.conversation=[{"role": "system", "content": self.system_prompt}]
        self.messages = []

    # defining a function to create the prompt from the system message and the conversation messages
    def create_prompt(self, system_message, messages):
        prompt = ""
        if "system" not in messages:
            prompt = system_message
        for message in messages:
            prompt += f"\n<|im_start|>{message['sender']}\n{message['text']}\n<|im_end|>"
        prompt += "\n<|im_start|>assistant\n"
        return prompt

    # 对话助手
    def aoai_conversation_chat_markedup_language(self, user_input):
        # defining the user input and the system message
        if 'exit' in user_input.lower():
            self.messages = []

        # creating a list of messages to track the conversation
        self.messages.append({"sender": "user", "text": user_input})

        response = openai.Completion.create(
            engine=self.OPENAI_GPT35_ENGINE, # The deployment name you chose when you deployed the ChatGPT model.
            prompt=self.create_prompt(self.system_message, self.messages),
            temperature=0.5,
            max_tokens=250,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['<|im_end|>']
        )

        self.messages.append({"sender": "assistant", "text": response['choices'][0]['text']})
        return response['choices'][0]['text']

    # 问答机器人
    def aoai_conversation_chat(self, user_input):
        # defining the user input and the system message
        if 'exit' in user_input.lower():
            self.messages = []
            return "Bye!"

        # creating a list of messages to track the conversation
        self.messages.append({"sender": "user", "text": user_input})

        response = openai.Completion.create(
            engine=self.OPENAI_GPT3_ENGINE, # The deployment name you chose when you deployed the ChatGPT model.
            prompt=self.create_prompt(self.system_message, self.messages),
            temperature=0.5,
            max_tokens=250,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['<|im_end|>']
        )

        self.messages.append({"sender": "assistant", "text": response['choices'][0]['text']})
        return response['choices'][0]['text']
    
    # 对话助手
    def aoai_conversation_chat_steam(self, user_input):
        # defining the user input and the system message
        if 'exit' in user_input.lower():
            self.conversation = []
            return "Bye!"

        self.conversation.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            engine = self.OPENAI_GPT35_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages = self.conversation,
            max_tokens = 1000,
            top_p = 1,
            frequency_penalty = 0.0,
            presence_penalty = 0.0,
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

        self.conversation.append({"role": "assistant", "content": gpt})
        print("\nGPT: \n" + gpt + "\n")
        return gpt