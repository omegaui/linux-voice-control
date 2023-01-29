from chatgpt_wrapper import ChatGPT

import command_manager
import voice_feedback

bot = ChatGPT()

def chat(text):
    if command_manager.hasText(text, command_manager.deactivateChatMode):
        voice_feedback.speak('deactivating chatgpt mode', wait=True)
        command_manager.chatMode = False
        return
    print(f"You to ChatGPT: {text}")
    resonse = bot.ask(text)
    voice_feedback.speak(resonse, wait=True)

