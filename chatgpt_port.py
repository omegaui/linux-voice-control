# manages user and chatgpt interactions
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3
from chatgpt_wrapper import ChatGPT

import command_manager
import voice_feedback

bot = None  # the chatGPT bot object
try:
    bot = ChatGPT()
except Exception as e:
    print(e)

def _init_bot():
    """
    tries to initialize the bot by calling ChatGPT()
    :return: nothing
    """
    global bot
    if not bot:
        return
    try:
        bot = ChatGPT()
    except Exception as ex:
        print(ex)


def chat(text):
    """
    handles user-chatgpt interactions
    """
    if command_manager.hasText(text, command_manager.deactivateChatMode):
        voice_feedback.speak('deactivating chatgpt mode', wait=True)
        command_manager.chatMode = False
        return
    _init_bot()
    print(f"You to ChatGPT: {text}")
    resonse = bot.ask(text)
    voice_feedback.speak(resonse, wait=True)

