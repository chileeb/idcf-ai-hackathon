import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")

system_prompt = """
Answer below question delimited with the same language of the question using only the data provided in the sources below. 
Question: {question}

Source:
The current temperature in Shenzhen Guangdong ProvinceChina is 94°F

Answer:
"""
input=input("\nQuestion: ")
prompt=system_prompt.format(question=input)

# prompt=system_prompt


response = openai.Completion.create(
  engine=OPENAI_GPT35_ENGINE,
  prompt=prompt,
  temperature=0.0,
  max_tokens=500,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  stop='<|im_end|>')

print(response['choices'][0]['text'])