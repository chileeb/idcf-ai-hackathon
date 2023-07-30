import os
import openai
from dotenv import load_dotenv
class Chat:

    # 该方法提供了以善士比亚的创作风格为某个名称的人物进行对话的功能。
    def aoai_chat_gpt35(self, user):
        load_dotenv()
        openai.api_type = "azure"
        openai.api_base = os.getenv("OPENAI_GPT4_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")

        OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
        OPENAI_GPT4_ENGINE = os.getenv("OPENAI_GPT4_ENGINE")

        """
        使用提示词，如下：
        您是莎士比亚式的写作助理，以莎士比亚的风格说话。你帮助人们想出创造性的想法和内容，比如使用莎士比亚写作风格的故事、诗歌和歌曲，包括“你”和“hath”等词。
        以下是莎士比亚风格的一些例子：
        - 罗密欧，罗密欧！你罗密欧是何在？
        - 爱不是用眼睛看，而是用头脑看;因此，有翅膀的丘比特被画成盲人。
        - 我能把你比作夏日吗？你的艺术更可爱，更温和。
        """
        system_prompt = """
        You are a Shakespearean writing assistant who speaks in a Shakespearean style. You help people come up with creative ideas and content like stories, poems, and songs that use Shakespearean style of writing style, including words like "thou" and "hath”.
        Here are some example of Shakespeare's style:
        - Romeo, Romeo! Wherefore art thou Romeo?
        - Love looks not with the eyes, but with the mind; and therefore is winged Cupid painted blind.
        - Shall I compare thee to a summer’s day? Thou art more lovely and more temperate.
        """ 

        response = openai.ChatCompletion.create(
            engine=OPENAI_GPT4_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages=[
                # 系统角色
                {"role": "system", "content": system_prompt},
                # 扮演角色姓名
                {"role": "user", "content": user}
            ]
        )
        return response['choices'][0]['message']['content']
    
    # 一个贴心的助手，可以与用户进行对话。
    def aoai_chat_markedup_language_gpt35(self, user_input):
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
        return response['choices'][0]['text']