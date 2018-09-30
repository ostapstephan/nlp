#Luka Lipovac and Ostap Voynarovsky
#Natural Language Processing - Project #2: Auto-Correct
#April 9th, 2018

#Run with: python Coral_Text_Edtior.py dictionary.txt
import Text_Editor
import Spell_Checker

import argparse
import time
import threading

recheck_time = 2

#Parse input
parser = argparse.ArgumentParser()
parser.add_argument("dictionary")
args = parser.parse_args()

editor = Text_Editor.Text_Editor(args.dictionary);
spell_checker = Spell_Checker.Spell_Checker(args.dictionary);

#run loop
start_time = int(time.time())
check_once_flag = 1 #used to to run spellcheck only once
while True:
    #update editor
    editor.root.update_idletasks()
    editor.root.update()

    #run spell_check every 5 seconds
    timer = (int(time.time()) - start_time) % recheck_time
    if (timer == 0) and (check_once_flag == 1):
        check_once_flag = 0
        editor.suggestionDict = spell_checker.spell_check(editor.text_retrieve())

        for added in editor.addedWords:
            del editor.suggestionDict[added]
            spell_checker.dictionary[added] = 1
            editor.addedWords = []

        editor.highlight_misspelling(editor.suggestionDict.keys(), 'blue')

    if (timer == 1):
        check_once_flag = 1
