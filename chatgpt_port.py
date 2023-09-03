# manages user and chatgpt interactions
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3
import os

import openai

import command_manager
import voice_feedback

bot = None  # the ChatGPT bot object
openai.api_key = os.environ.get('OPENAI_API_KEY')  #use export OPENAI_API_KEY='key' in terminal or hardcode it here

def chat(text):
    """
    handles user-chatgpt interactions
    """
    if command_manager.hasText(text, command_manager.deactivateChatMode):
        voice_feedback.speak('deactivating chatgpt mode', wait=True)
        command_manager.chatMode = False
        return
    global bot
    if not bot:
        try:
            bot = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text}
                ]
            )
        except Exception as e:
            print(e)
    print(f"You to ChatGPT: {text}")
    response = bot['choices'][0]['message']['content']
    voice_feedback.speak(response, wait=True)
