from flask import Flask, request, session, render_template
from flask_session import Session
from chat.chat import Chat
from completion.completion import Completion
from conversation.conversation import Conversation
from demo.demo import Demo

app = Flask(__name__)
# 为保证多轮会话，启用会话支持
app.config['SECRET_KEY'] = 'boathouse-ai-hackthon'  # 设置一个秘密密钥
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统保存会话数据
Session(app)

class ApiConfig:
    def __init__(self, config):
        self.config = config

@app.route('/')
def hello():
    return render_template('index.html', name='John')

@app.route('/aoai_chat_gpt35', methods=['POST'])
def aoai_chat_gpt35():
    data = request.json
    # 创建 Chat 类实例
    chat = Chat()
    return chat.aoai_chat_gpt35(data['user'])

@app.route('/aoai_chat_markedup_language_gpt35', methods=['POST'])
def aoai_chat_markedup_language_gpt35():
    data = request.json
    # 创建 Chat 类实例
    chat = Chat()
    return chat.aoai_chat_gpt35(data['user_input'])

@app.route('/aoai_completion_gpt3', methods=['POST'])
def aoai_completion_gpt3():
    data = request.json
    completion = Completion()
    return completion.aoai_completion_gpt3(data['user'])

@app.route('/aoai_completion_gpt35', methods=['POST'])
def aoai_completion_gpt35():
    data = request.json
    completion = Completion()
    return completion.aoai_completion_gpt35(data['user_input'])

@app.route('/aoai_chat_markedup_language_gpt3', methods=['POST'])
def aoai_chat_markedup_language_gpt3():
    data = request.json
    conversation = Conversation()
    if session.get("messages") is not None:
        conversation.messages = session["messages"]
    rsp = conversation.aoai_conversation_chat_markedup_language(data['user_input'])
    session["messages"] = conversation.messages
    return rsp

@app.route('/aoai_conversation_chat', methods=['POST'])
def aoai_conversation_chat():
    data = request.json
    conversation = Conversation()
    if session.get("messages") is not None:
        conversation.messages = session["messages"]
    rsp = conversation.aoai_conversation_chat(data['user_input'])
    session["messages"] = conversation.messages
    return rsp

@app.route('/aoai_conversation_chat_steam', methods=['POST'])
def aoai_conversation_chat_steam():
    data = request.json
    conversation = Conversation()
    if session.get("messages") is not None and len(session["messages"]) > 0:
        conversation.conversation = session["messages"]
    resp = conversation.aoai_conversation_chat_steam(data['user_input'])
    session["messages"] = conversation.conversation
    return resp

@app.route('/demo_role_wizard_1', methods=['POST'])
def demo_role_wizard_1():
    data = request.json
    demo = Demo()
    if session.get("messages") is not None and len(session["messages"]) > 0:
        demo.conversation = session["messages"]
    resp = demo.demo_role_wizard_1(data)
    return resp

@app.route('/demo_role_wizard_2', methods=['POST'])
def demo_role_wizard_2():
    data = request.json
    demo = Demo()
    resp = demo.demo_role_wizard_2(data)
    return resp

if __name__ == '__main__':
    app.run()
