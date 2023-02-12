# manages user and chatgpt interactions
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3
from chatgpt_wrapper import ChatGPT

import command_manager
import voice_feedback

bot = None  # the ChatGPT bot object

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
            bot = ChatGPT()
        except Exception as e:
            print(e)
    print(f"You to ChatGPT: {text}")
    response = bot.ask(text)
    voice_feedback.speak(response, wait=True)

