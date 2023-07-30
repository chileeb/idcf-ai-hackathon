import os
import openai
from dotenv import load_dotenv
class Demo:
    wizard_1 = """
    请描述完整下面关于role的prompt
    role
    这个角色擅长{tech}技术以及熟读{role}的作品,您需要将这两者完美地融合在一起,创作出富有创意的作品。
    prompt
    作为一位擅长{role}式表达方式且精通{role}的写作助手,您能将{tech}技术与{role}完美地融合在一起。
    rule
    您一定会按照{role}的表达方式来表达您的观点,但是您的观点不一定要与{role}的观点一致。
    您的观点可以是{role}的观点的延伸,也可以是{role}的观点的反面,但是您的表达方式一定要与{role}的表达方式一致。

    您的技能包括但不限于：。。。
    以下是{role}表达方式的一些例子：。。。
    您的工作包括但不限于：。。。

    请严格根据<rule>, 按照{role}的表达方式，使用{tech}技术来表达您的观点。
    """

    wizard_2 = """
    设定两个角色,一个来自古代,一个来自现代。
    角色A来自古代,模仿{roleA}第一人称
    角色B来自现代,模仿{roleB}第一人称

    角色A和角色B进行一场跨越世纪的交流。交流的主题是《{topic}》
    对话中不要带角色A或者角色B,对话的时候使用角色模仿的人物进行对话,比如{roleA}:,{roleB}:
    在对话中,每个角色都可以使用他们自己时代的语言和概念来表达自己的观点。
    由ChatGPT对角色A的每一条言论来进行翻译和解释,解释放在角色A的对话后。
    请由角色A先提问,角色B回答,共{round}轮,然后由角色B提问,角色A回答,也是{round}轮。
    """

    def __init__(self):
        load_dotenv()
        openai.api_type = "azure"
        openai.api_base = os.getenv("OPENAI_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        self.OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
        self.OPENAI_GPT3_ENGINE = os.getenv("OPENAI_GPT3_ENGINE")
        self.OPENAI_GPT4_ENGINE = os.getenv("OPENAI_GPT4_ENGINE")
        self.conversation = []
    
    def get_response(self, conversation):
        response = openai.ChatCompletion.create(
            engine= self.OPENAI_GPT4_ENGINE, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
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

    def init_role_wizard_1(self, data):
        role = data["role"]
        tech = data["tech"]

        system_prompt = Demo.wizard_1.format(role=role, tech=tech)
        conversation=[{"role": "system", "content": system_prompt}]
        print("生成prompt中, 请稍等...")
        self.conversation.append({"role": "user", "content": ""})
        gpt_init = self.get_response(conversation)
        conversation.append({"role": "assistant", "content": gpt_init})
        return conversation
    
    def demo_role_wizard_1(self, data):
        # 初始化
        self.conversation = self.init_role_wizard_1(data)
        # 开始创作
        self.conversation.append({"role": "user", "content": data["need"]})
        gpt_resp = self.get_response(self.conversation)
        return gpt_resp
    
    def init_role_wizard_2(self, data):
        system_prompt = Demo.wizard_2.format(roleA=data["ancientRole"], roleB=data["todayRole"], topic=data["topic"], round=data["round"])
        conversation=[{"role": "system", "content": system_prompt}]
        print(" 正在生成prompt, 请稍等...")
        print(system_prompt)
        print(" 正在生成对话, 请稍等...")
        conversation.append({"role": "user", "content": ""})
        gpt_init = self.get_response(conversation)
        conversation.append({"role": "assistant", "content": gpt_init})
        return conversation

    def demo_role_wizard_2(self, data):
        # 初始化
        self.conversation = self.init_role_wizard_2(data)
        # 开始创作
        self.conversation.append({"role": "user", "content": data["need"]})
        gpt_resp = self.get_response(self.conversation)
        return gpt_resp