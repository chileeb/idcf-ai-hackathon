"""
演示一：注入灵魂的创作

1.输入您需要的角色
2.输入您需要的技术
3.GPT自动生成提示词
4.输入您的需求
5.GPT自动生成回复
6.循环

例如：

角色:莎士比亚 
技术:写作
需求:用莎士比亚的戏剧风格描写李白的《将进酒》

角色:杜甫
技术:航天知识
需求:用杜甫的诗词来描述现代的火星探索，这可能会产生一种古典与现代的有趣碰撞。

角色:孔子
技术:区块链
需求:用孔子的语言和思想来解释区块链技术，这可能会让人们从一个全新的角度理解这项技术。

演示二：穿越时空的对话

1.输入您需要的古代角色
2.输入您需要的现代角色
3.输入您需要交流的主题
4.输入您需要交流的轮次
5.GPT自动生成提示词
6.GPT自动生成对话
7.循环

例如:

古代角色:孔子
现代角色:马云
主题:创新
轮次:2

古代角色:曹操
现代角色:马斯克
主题:科技创新
轮次:2

"""

from utility import *

conversation = reset_role_wizard_2()

while(True):

    user_input = input('\n请输入需求: \n')      
    if 'exit' in user_input.lower():
        exit()
    if 'reset' in user_input.lower():
        conversation = reset_role_wizard_2()
        continue

    conversation.append({"role": "user", "content": user_input})
    gpt_resp = get_response(conversation)
    conversation.append({"role": "assistant", "content": gpt_resp})

