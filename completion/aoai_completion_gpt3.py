import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_GPT3_ENGINE = os.getenv("OPENAI_GPT3_ENGINE")

system_prompt = "You are a helpful assistant."
prompt=input(system_prompt + "\nQuestion: ")

response = openai.Completion.create(
  engine=OPENAI_GPT3_ENGINE,
  prompt=prompt,
  temperature=1,
  max_tokens=500,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  best_of=1,
  stop=None)

print(response['choices'][0]['text'])