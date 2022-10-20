# the command management system, the idea on which the entire project depends is very much simple, a json file (
# lvc-commands.json), whose keys are your vocal commands and their values are the instruction to be executed
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import json
import os.path
import threading
from thefuzz import process
from thefuzz import fuzz
from termcolor import cprint
from notifier import notify

# stores commands from the lvc-commands.json file
commands = dict()

# stores all the keys in commands dictionary to be extracted by Fuzzy Matcher
choices = []


# initializing commands with commands specified in lvc-commands.json
def init():
    global commands, choices
    commands = get_commands_from_file()
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
        command = commands[probability[0]]
        cprint(f'>>> executing: {command}', "green", attrs=["bold"])
        notify(f'Executing: {command}', 250)
        threading.Thread(target=lambda: os.system(command)).start()
    else:
        cprint(">>> Unrecognized command", "red", attrs=["bold"])


def is_text_prediction_applicable(text, predicted_text):
    if ' ' in predicted_text:
        # Using Sort Ratio Fuzzy Match to validate if
        # the vocal and the probable command contain same words
        ratio = fuzz.token_sort_ratio(text, predicted_text)
        print("tokenizer ratio:", ratio)
        return ratio > 60  # ratio threshold must be 60 or more accurate
    return True  # No further check is performed for single word commands


# lists all the available commands to the console
def show_commands():
    print(">>> Available Commands")
    for launcher in commands:
        print(launcher, ":", commands[launcher])
    print()
