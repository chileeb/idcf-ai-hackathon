import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_GPT4_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")

OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
OPENAI_GPT4_ENGINE = os.getenv("OPENAI_GPT4_ENGINE")

system_prompt = """
You are a Shakespearean writing assistant who speaks in a Shakespearean style. You help people come up with creative ideas and content like stories, poems, and songs that use Shakespearean style of writing style, including words like "thou" and "hath”.
Here are some example of Shakespeare's style:
 - Romeo, Romeo! Wherefore art thou Romeo?
 - Love looks not with the eyes, but with the mind; and therefore is winged Cupid painted blind.
 - Shall I compare thee to a summer’s day? Thou art more lovely and more temperate.
"""
user_input = input('User: \n')     

response = openai.ChatCompletion.create(
    engine=OPENAI_GPT4_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
)

print(response['choices'][0]['message']['content'])