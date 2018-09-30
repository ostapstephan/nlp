#Luka Lipovac and Ostap Voynarovsky
#Natural Language Processing - Project #2: Auto-Correct
#April 9th, 2018

#Run with: python Resume_Booster_Text_Edtior.py dictionary.txt
import Text_Editor
import Spell_Checker

import argparse
import time
import threading

#Parse input
parser = argparse.ArgumentParser()
parser.add_argument("dictionary")
args = parser.parse_args()

editor = Text_Editor.Text_Editor();
spell_checker = Spell_Checker.Spell_Checker(args.dictionary);

#run loop
start_time = int(time.time())
check_once_flag = 1 #used to to run spellcheck only once
while True:
    #update editor
    editor.root.update_idletasks()
    editor.root.update()

    #run spell_check every 5 seconds
    timer = (int(time.time()) - start_time) % 5
    if (timer == 0) and (check_once_flag == 1):
        check_once_flag = 0
        suggested_edits = spell_checker.spell_check(editor.text_retrieve())
        editor.highlight_misspelling(['woop', 'toot'])

    if (timer == 1):
        check_once_flag = 1
