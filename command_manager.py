# the command management system, the idea on which the entire project depends is very much simple, a json file (
# lvc-commands.json), whose keys are your vocal commands and their values are the instruction to be executed
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import json
import os.path
import shlex
import subprocess

from termcolor import cprint
from thefuzz import fuzz
from thefuzz import process

import config_manager
import master_mode_manager
from notifier import notify
from voice_feedback import give_execution_feedback, speak, give_exiting_feedback

# stores commands from the lvc-commands.json file
commands = dict()

# built-in actions
quitCommand = "see you later"  # say this to turn off your voice control engine
activateMasterModeCommand = "activate master control mode"  # say this to turn on master control mode
deactivateMasterModeCommand = "deactivate master control mode"  # say this turn off master control mode
activateChatMode = "activate chat mode"  # say this turn off master control mode
deactivateChatMode = "deactivate chat mode"  # say this turn off master control mode

# internal-vars
self_activated_master_mode = False  # used for notifying the user if master control mode was enabled implicitly
chatMode = False  # used for working in chatGPT mode

# stores all the keys in commands dictionary to be extracted by Fuzzy Matcher
choices = []


# initializing commands with commands specified in lvc-commands.json
def init():
    global commands, choices
    commands = get_commands_from_file()
    name = config_manager.config['name']

    commands[f'see you later {name}'] = "<built-in>"
    commands[activateMasterModeCommand] = "<built-in>"
    commands[deactivateMasterModeCommand] = "<built-in>"
    commands[activateChatMode] = "<built-in>"
    commands[deactivateChatMode] = "<built-in>"

    choices = list(commands.keys())
    show_commands()


# getting json data from file
def get_commands_from_file():
    return json.load(open(os.path.join(os.getcwd(), "lvc-commands.json")))


# performing accurate match and launching any command if the vocal matches with any key (using Fuzzy Match)
def launch_if_any(text):
    # We can't only depend on this (as it may make put unwanted command in execution),
    # We need to perform further
    # precaution matching
    probability = process.extractOne(text, choices)
    print("probability:", probability)

    if probability and is_text_prediction_applicable(text, probability[0]):
        try:
            command = commands[probability[0]]['exec']
        except TypeError:
            command = commands[probability[0]]
        if not check_for_built_in_actions(probability[0]):
            if commands[probability[0]]['feedback']:
                speak(commands[probability[0]]['feedback'], commands[probability[0]]['blocking'])
            else:
                give_execution_feedback()
            cprint(f'>>> executing: {command}', "green", attrs=["bold"])
            notify(f'Executing: {command}', 250)
            subprocess.Popen(shlex.split(command), start_new_session=True)  # using subprocess will easily detach it
    else:
        cprint(">>> Unrecognized command", "red", attrs=["bold"])


# performs further fuzzy match to ensure the command to be executed is correct
def is_text_prediction_applicable(text, predicted_text):
    if ' ' in predicted_text:
        # Using Sort Ratio Fuzzy Match to validate if
        # the vocal and the probable command contain same words
        ratio = fuzz.token_sort_ratio(text, predicted_text)
        return ratio > 60  # ratio threshold must be 60 or more accurate
    return True  # No further check is performed for single word commands


# before diving further, we perform a check for in-built actions here
# @returns: True if an implicit action is invoked
def check_for_built_in_actions(text):
    global self_activated_master_mode, chatMode
    if text.startswith(quitCommand):
        give_execution_feedback()
        if self_activated_master_mode:
            speak('Deactivating Master Control Mode of this session', wait=True)
        give_exiting_feedback()
        exit(0)
    elif hasText(text, activateMasterModeCommand):
        if config_manager.config['master-mode']:
            speak('Master Control Mode is already Activated', wait=True)
            return True
        if not master_mode_manager.canEnableMasterMode():
            speak('You need to configure master control mode before using it, refer to project\'s readme', wait=True)
            return True
        config_manager.config['master-mode'] = True
        self_activated_master_mode = True
        cprint(f'MASTER CONTROL MODE: ON', "blue", attrs=['bold'])
        speak('Activated Master Control Mode', wait=True)
        return True
    elif hasText(text, deactivateMasterModeCommand):
        if not config_manager.config['master-mode']:
            speak('Master Control Mode is already Off', wait=True)
            return True
        config_manager.config['master-mode'] = False
        self_activated_master_mode = False
        cprint(f'MASTER CONTROL MODE: OFF', "blue", attrs=['bold'])
        speak('Deactivated Master Control Mode', wait=True)
        return True
    elif hasText(text, activateChatMode):
        speak('activating chatgpt mode', wait=True)
        chatMode = True
        return True
    return False


# finds if the @source actually encloses the @text in it
def hasText(source, text):
    if text in source:
        index = source.find(text)
        return index == 0 or not source[index - 1].isalpha()
    return False


# lists all the available commands to the console
def show_commands():
    if config_manager.config['show-commands-on-startup']:
        print(">>> Available Commands")
        for launcher in commands:
            print(launcher, ":", commands[launcher])
        print()
