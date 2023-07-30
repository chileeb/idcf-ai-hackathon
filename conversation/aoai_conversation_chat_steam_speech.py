#!/usr/bin/env python
# coding: utf-8
import time
import os
import openai
import json
from azure.cognitiveservices.speech import  SpeechConfig
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_GPT4_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
OPENAI_GPT4_ENGINE = os.getenv("OPENAI_GPT4_ENGINE")

try:
    import azure.cognitiveservices.speech as speechsdk 
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = AZURE_SPEECH_KEY, AZURE_SPEECH_REGION

system_message = '''你是一个智能陪伴机器人, 而且是儿童专家,尤其针对6-14岁儿童。请用孩子听得懂的话来回答。
'''

conversation=[{"role": "system", "content": system_message}]

bye = False

def callGPT3(question):
    
    conversation.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
    engine=OPENAI_GPT35_ENGINE,
    messages=conversation,
    temperature=0.9,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=None,
    stream=True
    )

    gpt_content = ""
    for chunk in response:
        delta = chunk.choices[0].delta
        
        if "role" in delta.keys():
            print(delta.role + ": ", end="\n", flush=True)

        if "content" in delta.keys():
            gpt_content += delta.content
            print(delta.content, end="", flush=True)
            
    conversation.append({"role": "assistant", "content": gpt_content})

    tts(gpt_content)

    if "再见" in question:
        exit()


def speech_recognize_once_from_mic():
    
    # <SpeechRecognitionWithMicrophone>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="zh-CN")
    # Creates a speech recognizer using microphone as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    # GPT-3 prompt
    myprompt = ""

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        # print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def get_text(evt):
        #print('RECOGNIZED: {}'.format(evt))
        nonlocal myprompt
        myprompt = myprompt + evt.result.text
        print(myprompt)
        nonlocal done
        done = True   
              
    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    #speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: get_text(evt))

    speech_recognizer.session_started.connect(lambda evt: print("\n" + "Human:"))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.1)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>

    callGPT3(myprompt)


def tts(text):

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)

    
    speech_config.speech_synthesis_language = "zh-CN" 
    speech_config.speech_synthesis_voice_name ="zh-CN-XiaoshuangNeural"

    # Creates a speech synthesizer for the specified language,
    # using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Receives a text from console input and synthesizes it to speaker.
    result = speech_synthesizer.speak_text_async(text).get()
    
    

while not bye:
    speech_recognize_once_from_mic()


